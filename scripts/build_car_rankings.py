#!/usr/bin/env python3
"""Generate the offline comparison from researched inputs; --check detects drift."""
import argparse
from collections import Counter
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
from html import escape
import json
import math
from pathlib import Path
import re
from string import Template

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'projects/car-rankings'
KEYS = ('cost', 'eco', 'mountain', 'lux', 'commute', 'maintenance')
COMPONENTS = {
    'mountain': (('Carrying', 'Winter access', 'Trip practicality'), (40, 35, 25)),
    'lux': (('Ride/noise', 'Seating', 'Cabin ergonomics', 'Power liftgate'), (40, 30, 20, 10)),
    'commute': (('Traffic/speed control', 'Steering coverage', 'Driver supervision'), (40, 35, 25)),
    'maintenance': (('Less disruption', 'Less routine upkeep', 'Service access'), (50, 30, 20)),
}


def name_key(car):
    return car['name'].casefold()


def dollars(number):
    return float(Decimal(str(number)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def registration(value, ev, assumptions, *, initial=False, weight_fee=0):
    # Current DMV schedules; county fees are a disclosed allowance, not a DMV quote.
    tif = 33 if value < 5000 else 66 if value < 25000 else 132 if value < 35000 else 198 if value < 60000 else 231
    return dollars(76 + 34 + tif + value * .0065 + assumptions['county_fee_allowance'] + (121 if ev and not initial else 0) + weight_fee)


def calculate_cost(car, assumptions):
    price, energy = car['price'], car['energy']
    purchase = dollars(price['msrp'] + price['destination'] + sum(o['price'] for o in price['options']))
    taxable = dollars(purchase + assumptions['document_fee'])
    sales_tax = dollars(Decimal(str(taxable)) * Decimal(str(assumptions['sales_tax_rate'])))
    weight_fee = car['cost'].get('annual_weight_fee', 0)
    first_registration = registration(purchase, car['powertrain'] == 'EV', assumptions, initial=True, weight_fee=weight_fee)
    otd = dollars(taxable + sales_tax + first_registration)
    miles = assumptions['annual_miles'] * assumptions['years']
    electric_share = energy.get('electric_mile_share', 1 if car['powertrain'] == 'EV' else 0)
    kwh = miles * electric_share * energy.get('kwh_per_100_miles', 0) / 100
    # EPA AC consumption already includes charging losses. Never add them again.
    gallons = miles * (1 - electric_share) / energy['mpg'] if electric_share < 1 else 0
    gas_price = assumptions['premium_per_gallon'] if energy['fuel_grade'] == 'premium' else assumptions['regular_per_gallon']
    fuel = dollars(gallons * gas_price)
    electricity = dollars(kwh * assumptions['electricity_per_kwh'])
    resale = dollars(purchase * (1 - car['cost']['depreciation_fraction']))
    renewals = sum(registration(purchase * factor, car['powertrain'] == 'EV', assumptions, weight_fee=weight_fee) for factor in assumptions['renewal_value_factors'])
    insurance = assumptions['insurance_per_year'] * assumptions['years']
    upkeep = assumptions['routine_upkeep_per_mile'][car['powertrain']] * miles
    repair_reserve = assumptions['repair_reserve_per_year'] * assumptions['years']
    subscriptions = car['commute'].get('subscription_per_year', 0) * assumptions['years']
    five = dollars(otd - resale + fuel + electricity + renewals + insurance + upkeep + repair_reserve + subscriptions)
    return dict(purchase=purchase, document_fee=assumptions['document_fee'], sales_tax=sales_tax,
                first_registration=first_registration, otd=otd, resale=resale, fuel=fuel, electricity=electricity,
                renewals=dollars(renewals), insurance=dollars(insurance), routine_upkeep=dollars(upkeep),
                repair_reserve=dollars(repair_reserve), subscriptions=dollars(subscriptions), five=five,
                gallons=round(gallons, 2), kwh=round(kwh, 2), electric_mile_share=electric_share)


def value(car, key):
    if key == 'cost':
        return -car['five']
    if key == 'eco':
        return car['eco']['assessment_score']
    info = car['comfort' if key == 'lux' else key]
    return sum(x * w for x, w in zip(info['components'], COMPONENTS[key][1]))


def tiers(values):
    """Five midpoint-percentile bands with shared competition ranks."""
    if any(not finite(v, -math.inf) for v in values):
        raise ValueError('Every assessment needs a finite numeric value')
    counts = Counter(values)
    n, better, result = len(values), 0, {}
    for raw in sorted(counts, reverse=True):
        group = counts[raw]
        # Exact 20/40/60/80 percent boundaries go toward zero.
        p = 5 * (2 * better + group)
        score = 2 if p < 2 * n else 1 if p < 4 * n else 0 if p <= 6 * n else -1 if p <= 8 * n else -2
        result[raw] = (score, better + 1)
        better += group
    return [result[v] for v in values]


def finite(number, minimum=0, maximum=math.inf):
    return type(number) in (int, float) and math.isfinite(number) and minimum <= number <= maximum


def capability_band(composite):
    """Fixed rubric anchors; an ordinary 3/5 remains neutral in any cohort."""
    if not finite(composite, 0, 500):
        raise ValueError('Invalid capability composite')
    return -2 if composite < 150 else -1 if composite < 250 else 0 if composite < 350 else 1 if composite < 450 else 2


def validate(data):
    if tuple(c['key'] for c in data['categories']) != KEYS or [c['default'] for c in data['categories']] != [1, 1, 1, 1, 1, 0]:
        raise ValueError('Preserve six categories, five one-point defaults and upkeep initially off')
    a, cars = data['assumptions'], data['cars']
    if a['years'] != 5 or not finite(a['annual_miles'], 1) or len(a['renewal_value_factors']) != a['years'] - 1:
        raise ValueError('Invalid ownership period')
    for key in ('sales_tax_rate', 'electricity_per_kwh', 'regular_per_gallon', 'premium_per_gallon', 'insurance_per_year', 'repair_reserve_per_year', 'document_fee', 'county_fee_allowance', 'budget_otd'):
        if not finite(a[key]):
            raise ValueError(f'Invalid assumption: {key}')
    if not 0 <= a['sales_tax_rate'] <= 1 or any(not finite(v, 0, 1) for v in a['renewal_value_factors']):
        raise ValueError('Invalid tax/value factor')
    if any(not finite(a['routine_upkeep_per_mile'].get(k)) for k in ('Gas', 'Hybrid', 'PHEV', 'EV')):
        raise ValueError('Invalid routine upkeep allowance')
    if not cars or len({c['id'] for c in cars}) != len(cars) or len({name_key(c) for c in cars}) != len(cars):
        raise ValueError('A nonempty cohort needs unique IDs and names')
    for sid, src in data['sources'].items():
        if not src['url'].startswith('https://') or not all(src.get(k) for k in ('title', 'year', 'scope', 'checked')):
            raise ValueError(f'Incomplete source: {sid}')
    def source_refs(info):
        refs = info.get('sources', [])
        if not refs or any(s not in data['sources'] for s in refs):
            raise ValueError('Evidence must reference known sources')
    for candidate in data['screened']:
        source_refs(candidate)
        if not all(candidate.get(k) for k in ('id', 'name', 'decision', 'reason')):
            raise ValueError('Incomplete screening decision')
    for car in cars:
        if any(k in car for k in ('five', 'otd', 'scores', 'ranks')):
            raise ValueError('Derived costs/scores must not be stored in research inputs')
        if not re.fullmatch(r'[a-z0-9-]+', car['id']) or car['powertrain'] not in ('Gas', 'Hybrid', 'PHEV', 'EV'):
            raise ValueError('Invalid ID or powertrain')
        source_refs(car['price']); source_refs(car['energy']); source_refs(car['equipment'])
        if car['equipment']['california_eligible'] is not True or not car['equipment']['configuration']:
            raise ValueError('Only California-eligible configurations belong in rankings')
        for key in ('msrp', 'destination'):
            if not finite(car['price'][key]):
                raise ValueError('Invalid price')
        if any(not o.get('name') or not finite(o['price']) for o in car['price']['options']):
            raise ValueError('Invalid selected option')
        if any(type(car['equipment'][k]) is not bool for k in ('power_liftgate', 'adaptive_cruise', 'lane_centering')):
            raise ValueError('Equipment needs a verified or estimated boolean assessment')
        e = car['energy']
        if e['epa_year'] != car['year'] or e['epa_make'] != car['manufacturer']:
            raise ValueError('Energy reference model year/manufacturer mismatch')
        if e.get('epa_id') and (not e['epa_model'].startswith(car['epa_model_family']) or e['epa_powertrain'] != {'Gas': 'Gas', 'Hybrid': 'Hybrid', 'PHEV': 'Plug-in Hybrid', 'EV': 'EV'}[car['powertrain']]):
            raise ValueError('Energy reference model/powertrain mismatch')
        if not finite(e.get('electric_mile_share', 1 if car['powertrain'] == 'EV' else 0), 0, 1):
            raise ValueError('Invalid electric-mile share')
        if car['powertrain'] != 'EV' and not finite(e.get('mpg'), 1, 150):
            raise ValueError('Missing gas-mode MPG')
        if car['powertrain'] in ('EV', 'PHEV') and not finite(e.get('kwh_per_100_miles'), 1, 150):
            raise ValueError('Missing electrical consumption')
        if car['powertrain'] == 'PHEV' and 'electric_mile_share' not in e:
            raise ValueError('PHEV costs require an explicit electric-mile assumption')
        if car['powertrain'] == 'EV' and e.get('electric_mile_share', 1) != 1:
            raise ValueError('EV miles must all be electric')
        if car['powertrain'] in ('Gas', 'Hybrid') and e.get('electric_mile_share', 0) != 0:
            raise ValueError('Non-plug-in miles cannot be assigned to the grid')
        if e['fuel_grade'] not in ('regular', 'premium', 'electricity'):
            raise ValueError('Invalid fuel grade')
        if not finite(car['cost']['depreciation_fraction'], 0, 1):
            raise ValueError('Invalid depreciation assumption')
        if not finite(car['cost'].get('annual_weight_fee', 0)) or (car['body_style'] == 'Pickup' and 'annual_weight_fee' not in car['cost']):
            raise ValueError('Pickup registration requires an explicit nonnegative weight-fee allowance')
        if not finite(car['commute'].get('subscription_per_year', 0)):
            raise ValueError('Invalid subscription cost')
        for key, (names, _) in COMPONENTS.items():
            info = car['comfort' if key == 'lux' else key]
            components = info['components']
            if len(components) != len(names) or any(type(v) is not int or not 0 <= v <= 5 for v in components):
                raise ValueError(f'Invalid components: {car["id"]}/{key}')
        if car['comfort']['components'][3] != (5 if car['equipment']['power_liftgate'] is True else 0):
            raise ValueError('Liftgate component must match the selected equipment assessment')
        if car['equipment']['lane_centering'] is not True and car['commute']['components'][1] != 0:
            raise ValueError('Absent/corrective-only steering cannot receive centering credit')
        if car['equipment']['adaptive_cruise'] is not True and car['commute']['components'][0] != 0:
            raise ValueError('Absent adaptive cruise cannot receive stop/go credit')
        commute = car['commute']
        if not commute.get('system') or len(commute.get('component_notes', [])) != 3 or any(not isinstance(note, str) or not note.strip() for note in commute['component_notes']):
            raise ValueError('Commute assessments need a selected system and three component rationales')
        mountain = car['mountain']
        if len(mountain.get('component_notes', [])) != 3 or any(not isinstance(note, str) or not note.strip() for note in mountain['component_notes']):
            raise ValueError('Mountain assessments need three component rationales')
        if not mountain.get('review_note'):
            raise ValueError('Mountain assessments need a review note')
        if car['powertrain'] == 'EV' and mountain['components'][2] > 3 and not mountain.get('trip_route_evidence', '').strip():
            raise ValueError('An EV trip upgrade needs loaded winter range, reserve and charging-plan evidence for the route')
        maintenance = car['maintenance']
        if not isinstance(maintenance.get('confidence'), str) or not maintenance['confidence'].strip():
            raise ValueError('Maintenance needs a separate evidence-confidence description')
        if len(maintenance.get('component_notes', [])) != 3 or any(not isinstance(note, str) or not note.strip() for note in maintenance['component_notes']):
            raise ValueError('Maintenance needs three component rationales')
        comfort = car['comfort']
        if len(comfort.get('component_notes', [])) != 4 or any(not isinstance(note, str) or not note.strip() for note in comfort['component_notes']) or not comfort.get('review_note'):
            raise ValueError('Comfort needs four component rationales and a review note')
        if comfort['components'][0] != 3 and not comfort.get('ride_test_evidence', '').strip():
            raise ValueError('A ride/noise departure from baseline needs comparable road-test evidence')
        audit = car.get('score_audit', {})
        if not all(audit.get(k) for k in ('checked', 'review_source', 'scope', 'energy_check', 'confidence')) or audit['review_source'] not in data['sources']:
            raise ValueError('Every car needs a complete score-audit record and review source')
        if not car['commute'].get('review_note'):
            raise ValueError('Assistance needs a capability/execution distinction')
        eco = car['eco']
        if not isinstance(eco.get('review_note'), str) or not eco['review_note'].strip():
            raise ValueError('Eco needs a configuration-specific review note')
        if not finite(eco.get('assessment_score'), 0, 100) or eco.get('basis') not in ('historical', 'proxy'):
            raise ValueError('Eco needs a finite assessment score and historical/proxy basis')
        if eco['basis'] == 'historical':
            if not finite(eco.get('benchmark_score'), 0, 100) or eco['benchmark_year'] != 2024 or not eco.get('benchmark_record') or not eco.get('comparable'):
                raise ValueError('Historical eco needs a comparable source record')
            if eco['benchmark_record']['year'] != eco['benchmark_year'] or eco['benchmark_record']['make'].casefold() != car['manufacturer'].casefold():
                raise ValueError('Eco anchor must match the manufacturer and historical year')
            if float(eco['benchmark_record']['score']) != eco['benchmark_score'] or eco['assessment_score'] != eco['benchmark_score']:
                raise ValueError('Historical assessment must match its source record')
        else:
            if eco.get('benchmark_score') is not None or eco.get('benchmark_record') is not None or eco.get('comparable'):
                raise ValueError('Proxy estimates must not masquerade as published same-model benchmarks')
            proxies = eco.get('proxy_records', [])
            if not proxies or not eco.get('adjustment_note'):
                raise ValueError('Proxy eco needs source records and an adjustment rationale')
            for proxy in proxies:
                if not all(proxy.get(k) for k in ('model', 'year', 'source')) or not finite(proxy.get('score'), 0, 100) or proxy['source'] not in eco['sources']:
                    raise ValueError('Invalid lifecycle proxy record')
                record = proxy.get('record', {})
                if not all(record.get(k) for k in ('make', 'model', 'engine', 'drive', 'emissions', 'city', 'highway', 'weight')) or record.get('year') != proxy['year'] or record.get('score') != proxy['score']:
                    raise ValueError('Lifecycle proxies must preserve a consistent historical source record')
                if proxy['model'] != f'{record["make"]} {record["model"]} · {record["engine"]} · {record["drive"]}':
                    raise ValueError('Lifecycle proxy label must identify its exact historical record')
            if eco.get('proxy_method') != 'unadjusted_anchor_mean' or not math.isclose(eco['assessment_score'], sum(p['score'] for p in proxies) / len(proxies), abs_tol=1e-9):
                raise ValueError('Eco proxy must use the disclosed unadjusted anchor mean')
        for key, note in car['equipment'].get('estimates', {}).items():
            if key not in ('power_liftgate', 'adaptive_cruise', 'lane_centering') or not isinstance(note, str) or not note.strip():
                raise ValueError('Equipment estimates need a capability and rationale')
        for key in ('cost', 'eco', 'mountain', 'comfort', 'commute', 'maintenance'):
            info = car[key]
            if not all(info.get(k) for k in ('status', 'source_year', 'configuration', 'note')):
                raise ValueError(f'Missing evidence context: {car["id"]}/{key}')
            source_refs(info)
        computed = calculate_cost(car, a)
        if computed['purchase'] <= 0 or computed['five'] <= 0 or computed['otd'] > a['budget_otd']:
            raise ValueError(f'Nonpositive cost or over-budget configuration: {car["id"]}')


def prepare(data):
    validate(data)
    cars = deepcopy(data['cars'])
    for car in cars:
        car['calculated_cost'] = calculate_cost(car, data['assumptions'])
        car['otd'], car['five'] = car['calculated_cost']['otd'], car['calculated_cost']['five']
        car['scores'] = {}
        car['ranks'], car['assessed_counts'] = {}, {}
    for key in KEYS:
        vals = [value(c, key) for c in cars]
        count = len(cars)
        for car, (score, rank) in zip(cars, tiers(vals)):
            car['scores'][key] = score if key in ('cost', 'eco') else capability_band(value(car, key))
            car['ranks'][key], car['assessed_counts'][key] = rank, count
    for car in cars:
        car['total'] = sum(car['scores'][cat['key']] * cat['default'] for cat in data['categories'])
    return sorted(cars, key=lambda c: (-c['total'], c['five'], name_key(c)))


def signed(n):
    return f'+{n:g}' if n > 0 else f'−{abs(n):g}' if n < 0 else '0'


def money(n):
    return f'${n / 1000:.1f}k'


def exact_money(n):
    return f'${n:,.2f}'


def pill(n):
    style = 'positive' if n > 0 else 'negative' if n < 0 else 'neutral'
    return f'<span class="pill {style}">{signed(n)}</span>'


def link(src):
    context = escape(f"Source: {src['year']}. {src['scope']}. Checked {src['checked']}.", quote=True)
    return f'<a class="source" href="{escape(src["url"], quote=True)}" target="_blank" rel="noopener noreferrer" title="{context}">{escape(src["title"])} ↗</a>'


def evidence(data, info):
    return (f'<p class="evidence">Evidence: {escape(str(info["source_year"]))} · {escape(info["configuration"])}.</p>'
            + '<p class="source-list">' + ' · '.join(link(data['sources'][s]) for s in info['sources']) + '</p>')


def component_text(car, key):
    names, weights = COMPONENTS[key]
    info = car['comfort' if key == 'lux' else key]
    parts = ' · '.join(f'{name} {x}/5 ({w}%)' for name, x, w in zip(names, info['components'], weights))
    return f'<p class="component">Editorial inputs: {escape(parts)}. Composite {value(car, key) / 100:g}/5.</p>'


def cost_details(car, assumptions):
    c, p = car['calculated_cost'], car['price']
    rows = [('MSRP (destination excluded)', p['msrp']), ('Destination', p['destination'])]
    rows += [(o['name'], o['price']) for o in p['options']]
    rows += [('Document fee', c['document_fee']), ('Sales tax', c['sales_tax']), ('First registration', c['first_registration']),
             ('Estimated OTD', c['otd']), ('Less estimated resale', -c['resale']), ('Gasoline', c['fuel']),
             ('Electricity', c['electricity']), ('Four renewals', c['renewals']), ('Insurance allowance', c['insurance']),
             ('Routine upkeep allowance', c['routine_upkeep']), ('Repair reserve', c['repair_reserve']),
             ('Assistance subscriptions', c['subscriptions']), ('Estimated five-year cost', c['five'])]
    table = '<dl class="cost-breakdown">' + ''.join(f'<dt>{escape(k)}</dt><dd>{exact_money(v)}</dd>' for k, v in rows) + '</dl>'
    share = f' Electric-mile share {c["electric_mile_share"]:.0%} is a scenario assumption, not a measured driving pattern.' if car['powertrain'] == 'PHEV' else ''
    return (f'<p>{money(car["five"])} over five years / {assumptions["annual_miles"] * assumptions["years"]:,} miles, excluding financing. '
            f'{escape(car["price"]["note"])} {escape(car["cost"]["note"])}</p>' + table
            + f'<p class="evidence">Energy: {c["gallons"]:,.2f} gallons + {c["kwh"]:,.2f} kWh.{share} '
            'EPA AC consumption includes charging losses. Resale, insurance, upkeep and repairs are planning assumptions; no dealer, insurer or future resale quote is claimed.</p>')


def assessment(data, car, cat):
    key = cat['key']; info = car['comfort' if key == 'lux' else key]
    relative = key in ('cost', 'eco')
    tier = ({2: 'Highest band', 1: 'Upper band', 0: 'Middle band', -1: 'Lower band', -2: 'Lowest band'} if relative else
            {2: 'Strong capability', 1: 'Useful capability', 0: 'Workable baseline', -1: 'Constrained', -2: 'Very constrained'})[car['scores'][key]]
    rank_text = f' · #{car["ranks"][key]} of {car["assessed_counts"][key]} assessed'
    head = (f'<section class="assessment" data-assessment="{key}"><div class="assess-head"><h3>{escape(cat["label"])}</h3>'
            f'{pill(car["scores"][key])}<span class="tiernote">{tier}{rank_text}</span></div>'
            f'<p class="status">{escape(info["status"])}</p>')
    if key == 'cost':
        body = cost_details(car, data['assumptions'])
    elif key == 'eco':
        if info['basis'] == 'historical':
            body = (f'<p><b>Historical 2024 Green Score: {info["benchmark_score"]}/100</b> — {escape(info["benchmark_model"])}. '
                    'This is a comparison anchor, not a current-model test rating.</p>')
        else:
            body = (f'<p><b>Estimated lifecycle assessment: {info["assessment_score"]}/100</b>. '
                    'Editorial proxy estimate on the historical Green Score scale; not a published ACEEE rating for this car.</p>')
            body += '<p>Lifecycle proxies: ' + '; '.join(
                f'{escape(str(p["year"]))} {escape(p["model"])} ({p["score"]}/100)'
                for p in info['proxy_records']) + '.</p>'
            body += f'<p>{escape(info["adjustment_note"])}</p>'
        body += (f'<p>{escape(info["note"])}</p><p class="evidence">{escape(info["review_note"])}</p>'
                 '<p class="evidence">The −2 to +2 band is relative to this comparison group. Zero means middle band, not zero environmental benefit. Adding vehicles can change the band without changing the underlying lifecycle assessment.</p>')
    elif key == 'mountain':
        rationale = ''.join(f'<p><b>{escape(name)}:</b> {escape(note)}</p>'
                            for name, note in zip(COMPONENTS[key][0], info['component_notes']))
        body = (f'<p><b>Three adults + gear:</b> {escape(info["note"])}</p>'
                f'<p><b>Interior:</b> {escape(info["interior_fit"])}</p><p><b>Roof route:</b> {escape(info["roof"])}</p>'
                f'<p><b>Winter:</b> {escape(info["winter"])}</p><p><b>Trip:</b> {escape(info["trip"])}</p>'
                + rationale + f'<p class="evidence">{escape(info["review_note"])}</p>'
                '<p class="evidence">Rack/box and winter tires cost extra and are excluded from the base cost comparison for every vehicle. Exact gear fit, roof load and hatch/trunk clearance remain unmeasured.</p>' + component_text(car, key))
    elif key == 'lux':
        lift = 'Selected configuration has a verified power liftgate.' if car['equipment']['power_liftgate'] is True else 'Selected configuration is assessed as a manual rear opening.'
        rationale = ''.join(f'<p><b>{escape(name)}:</b> {escape(note)}</p>'
                            for name, note in zip(COMPONENTS[key][0], info['component_notes']))
        body = (f'<p>{escape(info["note"])}</p><p>{lift} Liftgate is 10% of Comfort only; body style never determines eligibility. Assistance is separate.</p>'
                + rationale + f'<p class="evidence">{escape(info["review_note"])}</p>' + component_text(car, key))
    elif key == 'commute':
        rationale = ''.join(f'<p><b>{escape(name)}:</b> {escape(note)}</p>'
                            for name, note in zip(COMPONENTS[key][0], info['component_notes']))
        body = (f'<p>{escape(info["note"])}</p><p><b>Selected equipment:</b> {escape(info["package"])}</p>'
                + rationale + f'<p class="evidence">{escape(info["review_note"])}</p>'
                + '<p class="evidence">Component values compare supported tasks and editorial usefulness. Road conditions, restart limits, software and driver supervision still matter. A higher capability score is not a safety certification.</p>' + component_text(car, key))
    else:
        rationale = ''.join(f'<p><b>{escape(name)}:</b> {escape(note)}</p>'
                            for name, note in zip(COMPONENTS[key][0], info['component_notes']))
        body = (f'<p>{escape(info["note"])}</p><p><b>Evidence confidence (not scored):</b> {escape(info["confidence"])}</p>'
                + rationale + f'<p>{escape(info["upkeep"])}</p><p><b>Repairability:</b> {escape(info["repairability"])}</p>'
                '<p class="evidence">No current-model failure rate or numeric repairability rating is claimed. Dollar upkeep is already in Cost; this dimension concerns time and disruption.</p>' + component_text(car, key))
    ties = sum(value(other, key) == value(car, key) for other in prepare_values(data, key))
    if ties > 1:
        body += f'<p class="evidence">{ties} vehicles share this underlying value and receive the same tier and category rank.</p>'
    return head + body + evidence(data, info) + '</section>'


def prepare_values(data, key):
    if key != 'cost':
        return data['cars']
    return [dict(c, five=calculate_cost(c, data['assumptions'])['five']) for c in data['cars']]


def row(car, cats, rank):
    cells = []
    for cat in cats:
        key = cat['key']
        basis = 'relative to this comparison group' if key in ('cost', 'eco') else 'on the fixed capability rubric'
        label = f'{cat["label"]}: {signed(car["scores"][key])} {basis}'
        if key == 'eco':
            label += f'; lifecycle assessment {car["eco"]["assessment_score"]}/100; {car["eco"]["status"]}'
        cells.append(f'<span class="cell" data-category="{key}" data-label="{escape(cat["short"])}" title="{escape(label)}" aria-label="{escape(label)}">{pill(car["scores"][key])}</span>')
    return (f'<a class="car{" first" if rank == 1 else ""}" data-id="{car["id"]}" href="#detail-{car["id"]}" aria-label="Details for {escape(car["name"])}">'
            f'<span class="rank">{rank:02}</span><span class="name">{escape(car["name"])}</span><strong class="total">{signed(car["total"])}</strong>'
            f'<span class="cells">{"".join(cells)}</span><span class="arrow" aria-hidden="true">›</span></a>')


def modal(data, car):
    cid, e = car['id'], car['energy']
    audit = car['score_audit']
    review = ('<details class="rubric"><summary>Review evidence and confidence</summary>'
              f'<p class="evidence">{escape(audit["scope"])} {escape(audit["energy_check"])}</p>'
              f'<p class="evidence">{escape(audit["confidence"])}</p>'
              f'<p class="source-list">{link(data["sources"][audit["review_source"]])}</p></details>')
    energy_label = f'{e["kwh_per_100_miles"]:g} kWh/100 mi' if car['powertrain'] == 'EV' else f'{e["mpg"]:g} MPG'
    return (f'<section class="modal" id="detail-{cid}" aria-labelledby="title-{cid}"><a class="scrim" href="#ranking" aria-label="Close details"></a>'
            f'<div class="modal-panel" role="dialog" aria-modal="true" aria-labelledby="title-{cid}" tabindex="-1">'
            f'<div class="modal-header"><div><small>Evidence and planning estimates</small><h2 id="title-{cid}">{escape(car["name"])}</h2>'
            f'<p class="modal-trim">{car["year"]} · {escape(car["trim"])}</p></div><a class="close" href="#ranking" aria-label="Close details">×</a></div>'
            f'<div class="statrow"><div><small>Weighted score</small><b data-total="{cid}">{signed(car["total"])}</b></div><div><small>Est. OTD</small><b>{money(car["otd"])}</b></div>'
            f'<div><small>Est. five-year cost</small><b>{money(car["five"])}</b></div><div><small>Energy reference</small><b>{escape(energy_label)}</b></div></div>'
            f'<p class="evidence">{escape(e["note"])} {escape(car["equipment"]["note"])}</p>' + evidence(data, e)
            + review + '<div class="details">' + ''.join(assessment(data, car, cat) for cat in data['categories']) + '</div>'
            '<div class="modal-foot">Maintenance starts off · <a class="source" href="#method">Method and assumptions</a></div></div></section>')


def render(data):
    cars, cats = prepare(data), data['categories']
    controls, segments = [], []
    accents = ('#3978a8', '#7465ac', '#b47737', '#ac6084', '#41888b', '#737c96')
    for cat, accent in zip(cats, accents):
        key, value = cat['key'], cat['default']
        share = value * 100 / len(cats)
        slider_share = value * 100 / 2
        off = ' is-off' if not value else ''
        controls.append(f'<div class="slider-unit{off}" id="unit-{key}" style="--accent:{accent};--share:{slider_share:g}%;--previous:{slider_share:g}%">'
                        f'<div class="line"><label for="w-{key}"><i class="category-swatch" aria-hidden="true"></i>{escape(cat["label"])}</label>'
                        f'</div><output id="v-{key}" for="w-{key}" aria-live="off">{str(value) + " pt" if value else "Off"}</output>'
                        f'<div class="range-wrap"><div class="slider-rail" aria-hidden="true"><span class="slider-fill"></span><span class="slider-default"></span><span class="slider-previous"></span><span class="slider-stop"></span><span class="slider-thumb"></span></div>'
                        f'<input id="w-{key}" type="range" value="{value}" min="0" max="2" step="0.01" aria-label="{escape(cat["label"])} allocation" aria-valuetext="{str(value) + " points" if value else "Off"}">'
                        '<div class="slider-scale" aria-hidden="true"><span>Off</span><span>1 pt</span><span>2 pt</span></div></div></div>')
        segments.append(f'<span id="segment-{key}" style="--accent:{accent};width:{share:g}%" aria-hidden="true"></span>')
    payload = dict(categories=cats, cars=[{k: c[k] for k in ('id', 'name', 'five', 'scores')} for c in cars])
    runtime_json = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('&', '\\u0026')
    handoff = (f'Generated {data["updated"]}. Edit data.json + template.html; run python3 scripts/build_car_rankings.py.\n'
               f'{len(cars)} new-car configurations; all body styles; <= $60k estimated OTD, Orange County/Irvine tax baseline.\n'
               'Keys: cost, eco, mountain, lux, commute, maintenance. First five default 1; maintenance 0.\n'
               'Sliders span 0–2 points, with 1 centered; direct and redistributed allocations are capped at 2.\n'
               'Cost/Eco use full-cohort midpoint percentiles; capability scores use fixed bands around the 3/5 baseline.\n'
               'Comfort = 40% ride/noise + 30% seating + 20% ergonomics + 10% verified power liftgate.\n'
               'Cost calculated from sourced inputs and disclosed allowances; 12k miles/year, five years; no financing.\n'
               'Nearby charging at ordinary OC electricity rate by user assumption; no home installation or retail charging markup.\n'
               'Keep offline fallback, accessible hash dialogs, source context and equally optional categories.\n'
               'Pareto paths includes every car, equivalent groups and direct dominance links.\n'
               'Rankings, Pareto and dialogs share one five-level scores object.\n'
               'Edit scripts/car_rankings_pareto.js for the embedded network engine and interface.\n'
               'Edit scripts/car_rankings_allocation.js for the one-point-per-active-category allocation engine.\n'
               'See audit.md for screened candidates, old/new ranks and outstanding evidence gaps.\n')
    counts = ' · '.join(f'{n} {label}' for label, n in sorted(Counter(c['powertrain'] for c in cars).items()))
    body_counts = ' · '.join(f'{n} {label}' for label, n in sorted(Counter(c['body_style'] for c in cars).items()))
    historical_count = sum(c['eco']['basis'] == 'historical' for c in cars)
    return Template((PAGE / 'template.html').read_text()).substitute(
        allocation_segments=''.join(segments), allocation_script=(ROOT / 'scripts/car_rankings_allocation.js').read_text(),
        handoff=handoff, count=len(cars), updated=escape(data['updated']), controls='\n'.join(controls),
        annual_miles=f'{data["assumptions"]["annual_miles"]:,}', tax_rate=f'{data["assumptions"]["sales_tax_rate"] * 100:g}',
        document_fee=f'{data["assumptions"]["document_fee"]:g}', county_fee=f'{data["assumptions"]["county_fee_allowance"]:g}',
        electricity_rate=f'{data["assumptions"]["electricity_per_kwh"]:g}', regular_rate=f'{data["assumptions"]["regular_per_gallon"]:g}', premium_rate=f'{data["assumptions"]["premium_per_gallon"]:g}',
        insurance_year=f'{data["assumptions"]["insurance_per_year"]:,}', repair_year=f'{data["assumptions"]["repair_reserve_per_year"]:,}',
        gas_upkeep=f'{data["assumptions"]["routine_upkeep_per_mile"]["Gas"] * 100:g}', hybrid_upkeep=f'{data["assumptions"]["routine_upkeep_per_mile"]["Hybrid"] * 100:g}', ev_upkeep=f'{data["assumptions"]["routine_upkeep_per_mile"]["EV"] * 100:g}',
        headers=''.join(f'<button type="button" data-category="{c["key"]}" data-sort="{c["key"]}" data-label="{escape(c["short"])}" title="Sort by {escape(c["label"])} score">{escape(c["short"])}<span class="sort-arrow" aria-hidden="true">↕</span></button>' for c in cats),
        rows='\n'.join(row(c, cats, i + 1) for i, c in enumerate(cars)), leader=f'Leader: {escape(cars[0]["name"])} ({signed(cars[0]["total"])})',
        modals='\n'.join(modal(data, c) for c in cars), runtime_json=runtime_json,
        pareto_script=(ROOT / 'scripts/car_rankings_pareto.js').read_text(),
        sort_script=(ROOT / 'scripts/car_rankings_sort.js').read_text(),
        lineup=counts, body_lineup=body_counts, historical_count=historical_count,
        proxy_count=len(cars) - historical_count, screened_count=len(data['screened']),
        **{'source_' + k: link(data['sources'][v]) for k, v in dict(aceee='aceee_method', coverage='aceee_coverage', ncap='ncap',
            cr='cr_adas', iihs='iihs_adas', repairpal='repairpal', roof='roof', chains='chains', sce='sce', tax='tax', dmv='dmv', resale='resale', gas='gas', doe='doe').items()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if tracked HTML differs from generated output')
    args = parser.parse_args()
    result = render(json.loads((PAGE / 'data.json').read_text()))
    output = PAGE / 'index.html'
    if args.check:
        if not output.exists() or output.read_text() != result:
            parser.exit(1, 'Car rankings HTML is stale; run python3 scripts/build_car_rankings.py\n')
        print('Car rankings HTML matches its data and template.')
    else:
        output.write_text(result)
        print(f'Generated {output.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
