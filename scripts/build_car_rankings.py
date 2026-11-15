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
    'commute': (('Stop/go', 'Continuous centering', 'Monitoring/usability'), (40, 35, 25)),
    'maintenance': (('Less disruption', 'Less routine upkeep', 'Service access'), (50, 30, 20)),
}


def name_key(car):
    return car['name'].casefold()


def dollars(number):
    return float(Decimal(str(number)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def registration(value, ev, assumptions):
    # Current DMV schedules; county fees are a disclosed allowance, not a DMV quote.
    tif = 33 if value < 5000 else 66 if value < 25000 else 132 if value < 35000 else 198 if value < 60000 else 231
    return dollars(76 + 34 + tif + value * .0065 + assumptions['county_fee_allowance'] + (121 if ev else 0))


def calculate_cost(car, assumptions):
    price, energy = car['price'], car['energy']
    purchase = dollars(price['msrp'] + price['destination'] + sum(o['price'] for o in price['options']))
    taxable = dollars(purchase + assumptions['document_fee'])
    sales_tax = dollars(Decimal(str(taxable)) * Decimal(str(assumptions['sales_tax_rate'])))
    first_registration = registration(purchase, car['powertrain'] == 'EV', assumptions)
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
    renewals = sum(registration(purchase * factor, car['powertrain'] == 'EV', assumptions) for factor in assumptions['renewal_value_factors'])
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
        return car['eco']['benchmark_score']
    info = car['comfort' if key == 'lux' else key]
    return sum(x * w for x, w in zip(info['components'], COMPONENTS[key][1]))


def tiers(values, levels=3):
    """Competition ranks and midpoint tiers. None is absent evidence, never a rank."""
    if levels not in (3, 5):
        raise ValueError('Only three or five scoring levels are supported')
    counts = Counter(v for v in values if v is not None)
    n, better, result = sum(counts.values()), 0, {None: (0, None)}
    for raw in sorted(counts, reverse=True):
        group = counts[raw]
        # Integer comparisons avoid rounding at exactly 1/3 and 2/3.
        midpoint_twice = 2 * better + group
        if levels == 3:
            score = 1 if 3 * midpoint_twice < 2 * n else -1 if 3 * midpoint_twice > 4 * n else 0
        else:
            # Exact fifth boundaries go toward zero, symmetrically.
            p = 5 * midpoint_twice
            score = 2 if p < 2 * n else 1 if p < 4 * n else 0 if p <= 6 * n else -1 if p <= 8 * n else -2
        result[raw] = (score, better + 1)
        better += group
    return [result[v] for v in values]


def finite(number, minimum=0, maximum=math.inf):
    return type(number) in (int, float) and math.isfinite(number) and minimum <= number <= maximum


def validate(data):
    if tuple(c['key'] for c in data['categories']) != KEYS or [c['default'] for c in data['categories']] != [1, 1, 1, 1, 1, 0]:
        raise ValueError('Preserve six categories, five 1× defaults and optional upkeep at 0×')
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
        if any(type(car['equipment'][k]) not in (bool, type(None)) for k in ('power_liftgate', 'adaptive_cruise', 'lane_centering')):
            raise ValueError('Equipment status must be true, false or explicitly unknown')
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
        if not finite(car['commute'].get('subscription_per_year', 0)):
            raise ValueError('Invalid subscription cost')
        for key, (names, _) in COMPONENTS.items():
            info = car['comfort' if key == 'lux' else key]
            components = info['components']
            if len(components) != len(names) or any(type(v) is not int or not 0 <= v <= 5 for v in components):
                raise ValueError(f'Invalid components: {car["id"]}/{key}')
        if car['comfort']['components'][3] != (5 if car['equipment']['power_liftgate'] is True else 0):
            raise ValueError('Only verified selected power liftgates receive comfort credit')
        if car['equipment']['lane_centering'] is not True and car['commute']['components'][1] != 0:
            raise ValueError('Unconfirmed/corrective-only steering cannot receive centering credit')
        if car['equipment']['adaptive_cruise'] is not True and car['commute']['components'][0] != 0:
            raise ValueError('Unconfirmed adaptive cruise cannot receive stop/go credit')
        eco = car['eco']
        if eco['benchmark_score'] is not None:
            if not finite(eco['benchmark_score'], 0, 100) or eco['benchmark_year'] != 2024 or not eco.get('benchmark_record') or not eco.get('comparable'):
                raise ValueError('Scored eco needs a comparable historical source record')
            if eco['benchmark_record']['year'] != eco['benchmark_year'] or eco['benchmark_record']['make'].casefold() != car['manufacturer'].casefold():
                raise ValueError('Eco anchor must match the manufacturer and historical year')
            if float(eco['benchmark_record']['score']) != eco['benchmark_score']:
                raise ValueError('Eco value must match its source record')
        elif eco['status'] != 'Unscored':
            raise ValueError('Missing evidence must be explicitly unscored')
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
        car['scores'], car['scores5'], car['assessed'] = {}, {}, {}
        car['ranks'], car['assessed_counts'] = {}, {}
    for key in KEYS:
        vals = [value(c, key) for c in cars]
        count = sum(v is not None for v in vals)
        for car, (score, rank) in zip(cars, tiers(vals)):
            car['scores'][key], car['ranks'][key], car['assessed_counts'][key] = score, rank, count
            car['assessed'][key] = rank is not None
        for car, (score, _) in zip(cars, tiers(vals, levels=5)):
            car['scores5'][key] = score
    for car in cars:
        car['total'] = sum(car['scores'][cat['key']] * cat['default'] for cat in data['categories'])
    return sorted(cars, key=lambda c: (-c['total'], c['five'], name_key(c)))


def signed(n):
    return f'+{n:g}' if n > 0 else f'−{abs(n):g}' if n < 0 else '0'


def money(n):
    return f'${n / 1000:.1f}k'


def exact_money(n):
    return f'${n:,.2f}'


def pill(n, missing=False):
    style = 'unscored' if missing else 'positive' if n > 0 else 'negative' if n < 0 else 'neutral'
    return f'<span class="pill {style}">{"—" if missing else signed(n)}</span>'


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
    missing = car['ranks'][key] is None
    tier = 'Unscored · contributes 0; evidence missing' if missing else {1: 'Upper tier', 0: 'Middle tier', -1: 'Lower tier'}[car['scores'][key]]
    rank_text = '' if missing else f' · #{car["ranks"][key]} of {car["assessed_counts"][key]} assessed'
    head = (f'<section class="assessment" data-assessment="{key}"><div class="assess-head"><h3>{escape(cat["label"])}</h3>'
            f'{pill(car["scores"][key], missing)}<span class="tiernote">{tier}{rank_text}</span></div>'
            f'<p class="status">{escape(info["status"])}</p>')
    if key == 'cost':
        body = cost_details(car, data['assumptions'])
    elif key == 'eco':
        if missing:
            body = '<p>No comparable published lifecycle score verified. This is missing evidence, not an average environmental rating. Other category weights are not increased to compensate.</p>'
        else:
            body = (f'<p><b>Historical 2024 Green Score: {info["benchmark_score"]}/100</b> — {escape(info["benchmark_model"])}. '
                    'This is a comparison anchor, not a current-model test rating.</p>')
        body += f'<p>{escape(info["note"])}</p>'
    elif key == 'mountain':
        body = (f'<p><b>Three adults + gear:</b> {escape(info["note"])}</p>'
                f'<p><b>Interior:</b> {escape(info["interior_fit"])}</p><p><b>Roof route:</b> {escape(info["roof"])}</p>'
                f'<p><b>Winter:</b> {escape(info["winter"])}</p><p><b>Trip:</b> {escape(info["trip"])}</p>'
                '<p class="evidence">Rack/box and winter tires cost extra and are excluded from the base cost comparison for every vehicle. Exact gear fit, roof load and hatch/trunk clearance remain unmeasured.</p>' + component_text(car, key))
    elif key == 'lux':
        lift = 'Selected configuration has a verified power liftgate.' if car['equipment']['power_liftgate'] is True else 'No power-liftgate credit: manual opening or unverified selected fitment.'
        body = f'<p>{escape(info["note"])}</p><p>{lift} Liftgate is 10% of Comfort only; body style never determines eligibility. Assistance is separate.</p>' + component_text(car, key)
    elif key == 'commute':
        body = (f'<p>{escape(info["note"])}</p><p><b>Selected equipment:</b> {escape(info["package"])}</p>'
                '<p class="evidence">Component values compare credited capabilities, not tested system performance. Check speed limits, restart behavior, driver supervision and operating conditions in the exact-build manual.</p>' + component_text(car, key))
    else:
        body = (f'<p>{escape(info["note"])}</p><p>{escape(info["upkeep"])}</p><p><b>Repairability:</b> {escape(info["repairability"])}</p>'
                '<p class="evidence">No current-model failure rate or numeric repairability rating is claimed. Dollar upkeep is already in Cost; this optional dimension concerns time and disruption.</p>' + component_text(car, key))
    if not missing:
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
        key = cat['key']; missing = car['ranks'][key] is None
        label = f'{cat["label"]}: ' + ('unscored; missing evidence; contributes zero' if missing else signed(car['scores'][key]))
        cells.append(f'<span class="cell" data-category="{key}" data-label="{escape(cat["short"])}" title="{escape(label)}" aria-label="{escape(label)}">{pill(car["scores"][key], missing)}</span>')
    warning = '<small class="availability">Eco unscored · see evidence</small>' if car['eco']['benchmark_score'] is None else ''
    return (f'<a class="car{" first" if rank == 1 else ""}" data-id="{car["id"]}" href="#detail-{car["id"]}" aria-label="Details for {escape(car["name"])}">'
            f'<span class="rank">{rank:02}</span><span class="name">{escape(car["name"])}{warning}</span><strong class="total">{signed(car["total"])}</strong>'
            f'<span class="cells">{"".join(cells)}</span><span class="arrow" aria-hidden="true">›</span></a>')


def modal(data, car):
    cid, e = car['id'], car['energy']
    energy_label = f'{e["kwh_per_100_miles"]:g} kWh/100 mi' if car['powertrain'] == 'EV' else f'{e["mpg"]:g} MPG'
    return (f'<section class="modal" id="detail-{cid}" aria-labelledby="title-{cid}"><a class="scrim" href="#ranking" aria-label="Close details"></a>'
            f'<div class="modal-panel" role="dialog" aria-modal="true" aria-labelledby="title-{cid}" tabindex="-1">'
            f'<div class="modal-header"><div><small>Evidence and planning estimates</small><h2 id="title-{cid}">{escape(car["name"])}</h2>'
            f'<p class="modal-trim">{car["year"]} · {escape(car["trim"])}</p></div><a class="close" href="#ranking" aria-label="Close details">×</a></div>'
            f'<div class="statrow"><div><small>Weighted score</small><b data-total="{cid}">{signed(car["total"])}</b></div><div><small>Est. OTD</small><b>{money(car["otd"])}</b></div>'
            f'<div><small>Est. five-year cost</small><b>{money(car["five"])}</b></div><div><small>Energy reference</small><b>{escape(energy_label)}</b></div></div>'
            f'<p class="evidence">{escape(e["note"])} {escape(car["equipment"]["note"])}</p>' + evidence(data, e)
            + '<div class="details">' + ''.join(assessment(data, car, cat) for cat in data['categories']) + '</div>'
            '<div class="modal-foot">Upkeep starts at 0× · <a class="source" href="#method">Method and assumptions</a></div></div></section>')


def render(data):
    cars, cats = prepare(data), data['categories']
    controls = []
    for cat in cats:
        key = cat['key']
        controls.append(f'<div class="slider-unit"><div class="line"><label for="w-{key}">{escape(cat["label"])}</label><output id="v-{key}" for="w-{key}">{cat["default"]}×</output></div>'
                        f'<input id="w-{key}" type="range" value="{cat["default"]}" min="0" max="3" step="0.5" aria-label="{escape(cat["label"])} weight"></div>')
    payload = dict(categories=cats, cars=[{k: c[k] for k in ('id', 'name', 'five', 'scores', 'scores5', 'assessed')} for c in cars])
    runtime_json = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('&', '\\u0026')
    handoff = (f'Generated {data["updated"]}. Edit data.json + template.html; run python3 scripts/build_car_rankings.py.\n'
               f'{len(cars)} new-car configurations; all body styles; <= $60k estimated OTD, Orange County/Irvine tax baseline.\n'
               'Keys: cost, eco, mountain, lux, commute, maintenance. First five default 1; maintenance 0.\n'
               'Tiers use equal-value midpoint percentiles; ties share scores/ranks. Missing eco is unscored, contributes 0.\n'
               'Comfort = 40% ride/noise + 30% seating + 20% ergonomics + 10% verified power liftgate.\n'
               'Cost calculated from sourced inputs and disclosed allowances; 12k miles/year, five years; no financing.\n'
               'Nearby charging at ordinary OC electricity rate by user assumption; no home installation or retail charging markup.\n'
               'Keep offline fallback, accessible hash dialogs, source context and optional maintenance.\n'
               'Pareto paths uses complete active-metric coverage, equivalent groups and direct dominance links.\n'
               'Experimental five-level scores preserve ties; only the Pareto view uses them.\n'
               'Edit scripts/car_rankings_pareto.js for the embedded network engine and interface.\n'
               'See audit.md for screened candidates, old/new ranks and outstanding evidence gaps.\n')
    coverage = sum(c['eco']['benchmark_score'] is not None for c in cars)
    counts = ' · '.join(f'{n} {label}' for label, n in sorted(Counter(c['powertrain'] for c in cars).items()))
    return Template((PAGE / 'template.html').read_text()).substitute(
        handoff=handoff, count=len(cars), updated=escape(data['updated']), controls='\n'.join(controls),
        annual_miles=f'{data["assumptions"]["annual_miles"]:,}', tax_rate=f'{data["assumptions"]["sales_tax_rate"] * 100:g}',
        document_fee=f'{data["assumptions"]["document_fee"]:g}', county_fee=f'{data["assumptions"]["county_fee_allowance"]:g}',
        electricity_rate=f'{data["assumptions"]["electricity_per_kwh"]:g}', regular_rate=f'{data["assumptions"]["regular_per_gallon"]:g}', premium_rate=f'{data["assumptions"]["premium_per_gallon"]:g}',
        insurance_year=f'{data["assumptions"]["insurance_per_year"]:,}', repair_year=f'{data["assumptions"]["repair_reserve_per_year"]:,}',
        gas_upkeep=f'{data["assumptions"]["routine_upkeep_per_mile"]["Gas"] * 100:g}', hybrid_upkeep=f'{data["assumptions"]["routine_upkeep_per_mile"]["Hybrid"] * 100:g}', ev_upkeep=f'{data["assumptions"]["routine_upkeep_per_mile"]["EV"] * 100:g}',
        headers=''.join(f'<span data-category="{c["key"]}" title="{escape(c["label"])}">{escape(c["short"])}</span>' for c in cats),
        rows='\n'.join(row(c, cats, i + 1) for i, c in enumerate(cars)), leader=f'Leader: {escape(cars[0]["name"])} ({signed(cars[0]["total"])})',
        modals='\n'.join(modal(data, c) for c in cars), runtime_json=runtime_json,
        pareto_script=(ROOT / 'scripts/car_rankings_pareto.js').read_text(),
        eco_coverage=f'{coverage}/{len(cars)}', lineup=counts,
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
