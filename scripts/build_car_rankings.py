#!/usr/bin/env python3
"""Generate the self-contained ranking page. Run with --check to detect drift.

Edit projects/car-rankings/data.json for research/scoring inputs and template.html
for presentation. The generated index.html needs no build tool or network at use.
"""

import argparse
from collections import Counter
from copy import deepcopy
from html import escape
import json
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'projects/car-rankings'
KEYS = ('cost', 'eco', 'mountain', 'lux', 'commute', 'maintenance')
COMPONENTS = {
    'mountain': (('Carrying', 'Winter access', 'Trip practicality'), (40, 35, 25)),
    'commute': (('Stop/go', 'Lane centering', 'Monitoring/usability'), (40, 35, 25)),
    'maintenance': (('Less disruption', 'Less routine upkeep', 'Service access'), (50, 30, 20)),
}


def name_key(car):
    return car['name'].casefold()


def value(car, key):
    """Values only order this cohort. No custom lifecycle formula is used."""
    if key == 'cost':
        return -car['five']
    if key == 'eco':
        return car['eco']['benchmark_score']
    if key == 'lux':
        return -car['comfort']['rank']
    return sum(x * w for x, w in zip(car[key]['components'], COMPONENTS[key][1]))


def validate(data):
    if tuple(c['key'] for c in data['categories']) != KEYS:
        raise ValueError('Category order must match the six-category contract')
    if [c['default'] for c in data['categories']] != [1, 1, 1, 1, 1, 0]:
        raise ValueError('Five core defaults must be 1; optional maintenance must be 0')
    cars = data['cars']
    if not cars or len(cars) % 3:
        raise ValueError('Equal thirds require a nonempty cohort divisible by three')
    if len({c['id'] for c in cars}) != len(cars):
        raise ValueError('Vehicle IDs must be unique')
    if len({name_key(c) for c in cars}) != len(cars):
        raise ValueError('Vehicle names must be unique for deterministic tie-breaking')
    if sorted(c['comfort']['rank'] for c in cars) != list(range(1, len(cars) + 1)):
        raise ValueError('Cabin ordinals must cover the cohort exactly once')
    for sid, src in data['sources'].items():
        if not src['url'].startswith('https://') or not all(src.get(k) for k in ('title', 'year', 'scope', 'checked')):
            raise ValueError(f'Incomplete source: {sid}')
    for car in cars:
        if car['five'] <= 0 or car['otd'] <= 0:
            raise ValueError('Costs must be positive')
        if not 0 <= car['eco']['benchmark_score'] <= 100 or car['eco']['benchmark_year'] != 2024:
            raise ValueError('Eco anchors must be identified historical 2024 Green Scores')
        for key in COMPONENTS:
            components = car[key]['components']
            if len(components) != 3 or any(type(v) is not int or not 0 <= v <= 5 for v in components):
                raise ValueError(f'Invalid editorial components: {car["id"]}/{key}')
        for key in ('cost', 'eco', 'mountain', 'comfort', 'commute', 'maintenance'):
            assessment = car[key]
            if not all(assessment.get(k) for k in ('status', 'source_year', 'configuration')):
                raise ValueError(f'Missing evidence metadata: {car["id"]}/{key}')
            if any(s not in data['sources'] for s in assessment['sources']):
                raise ValueError(f'Unknown source in {car["id"]}/{key}')


def prepare(data):
    validate(data)
    cars = deepcopy(data['cars'])
    third = len(cars) // 3
    for car in cars:
        car['scores'], car['ranks'] = {}, {}
    for key in KEYS:
        ordered = sorted(cars, key=lambda c: (-value(c, key), name_key(c)))
        for i, car in enumerate(ordered):
            car['ranks'][key] = i + 1
            car['scores'][key] = 1 if i < third else 0 if i < 2 * third else -1
        if Counter(c['scores'][key] for c in cars) != {-1: third, 0: third, 1: third}:
            raise ValueError('Tier imbalance')
    defaults = {cat['key']: cat['default'] for cat in data['categories']}
    for car in cars:
        car['total'] = sum(car['scores'][key] * defaults[key] for key in KEYS)
    return sorted(cars, key=lambda c: (-c['total'], c['five'], name_key(c)))


def signed(n):
    return f'+{n:g}' if n > 0 else f'−{abs(n):g}' if n < 0 else '0'


def money(n):
    return f'${n / 1000:.1f}k'


def pill(n):
    style = 'positive' if n > 0 else 'negative' if n < 0 else 'neutral'
    return f'<span class="pill {style}">{signed(n)}</span>'


def link(src):
    title = escape(src['title'])
    context = escape(f"Source: {src['year']}. {src['scope']}. Checked {src['checked']}.", quote=True)
    return f'<a class="source" href="{escape(src["url"], quote=True)}" target="_blank" rel="noopener noreferrer" title="{context}">{title} ↗</a>'


def evidence(data, info):
    links = ' · '.join(link(data['sources'][s]) for s in info['sources'])
    return (f'<p class="evidence">Evidence: {escape(str(info["source_year"]))} · '
            f'{escape(info["configuration"])}.</p>'
            + (f'<p class="source-list">{links}</p>' if links else '<p class="evidence">No independently researched ownership quote; retained planning input.</p>'))


def component_text(car, key):
    names, weights = COMPONENTS[key]
    parts = ' · '.join(f'{name} {x}/5 ({w}%)' for name, x, w in zip(names, car[key]['components'], weights))
    return f'<p class="component">Editorial inputs: {escape(parts)}. Composite {value(car, key) / 100:g}/5.</p>'


def assessment(data, car, cat):
    key = cat['key']
    info = car['comfort' if key == 'lux' else key]
    raw = car['scores'][key]
    tier = 'Top third' if raw == 1 else 'Middle third' if raw == 0 else 'Bottom third'
    count = len(data['cars'])
    head = (f'<section class="assessment" data-assessment="{key}"><div class="assess-head">'
            f'<h3>{escape(cat["label"])}</h3>{pill(raw)}<span class="tiernote">{tier} · '
            f'#{car["ranks"][key]} of {count}</span></div><p class="status">{escape(info["status"])}</p>')
    if key == 'cost':
        body = f'<p>{money(car["five"])} estimated over five years, excluding financing. Lower is better. Includes depreciation and operating costs; purchase price is not counted twice.</p>'
    elif key == 'eco':
        body = (f'<p><b>2024 comparison anchor: {info["benchmark_score"]}/100 Green Score</b> — '
                f'{escape(info["benchmark_model"])}. This is the historical benchmark’s score, not a measured '
                f'{car["year"]} {escape(car["name"])} score.</p><p>{escape(info["note"])}</p>'
                '<p>The tier uses this anchor unchanged. Manufacturing and battery impacts are included in the source method; no invented current-year lifecycle calculation is applied.</p>')
    elif key == 'mountain':
        body = (f'<p><b>Three adults + ski/snowboard gear.</b> {escape(info["cargo"])}</p>'
                f'<p><b>Interior fit:</b> {escape(info["interior_fit"])}</p>'
                f'<p><b>Roof option:</b> {escape(info["roof"])}</p>'
                '<p>A carrier, compatible bars/feet and possibly a roof box cost extra; obtain a fitted quote. '
                'Accessory costs are not added to the carried-forward OTD/TCO estimates. Roof loads add drag, height and loading effort.</p>'
                f'<p><b>Winter:</b> {escape(info["winter"])}</p><p><b>Trip:</b> {escape(info["trip"])}</p>'
                + component_text(car, key))
    elif key == 'lux':
        body = f'<p>{escape(info["note"])}</p><p>Cabin, seating, ride and noise only; commute assistance is scored separately.</p>'
    elif key == 'commute':
        body = (f'<p>{escape(info["note"])}</p><p><b>Equipment and subscriptions:</b> {escape(info["package"])}</p>'
                '<p>Speed limits, restart timing, hands-on requirements and monitoring performance need an exact-build manual/test-drive check. These are editorial capability estimates, not independent performance test scores.</p>'
                + component_text(car, key))
    else:
        body = (f'<p>{escape(info["note"])}</p><p>{escape(info["upkeep"])}</p>'
                f'<p><b>Repairability:</b> {escape(info["repairability"])}</p>'
                '<p>No exact-build failure rate, local shop census or numerical fixability rating is claimed. RepairPal informs the historical evidence approach; these are not RepairPal ratings. Dollar upkeep expenses remain in ownership cost.</p>'
                + component_text(car, key))
    ties = sum(value(other, key) == value(car, key) for other in data['cars'])
    tie_note = (f'<p class="evidence">Same underlying value as {ties - 1} other vehicle(s). '
                'Alphabetical ordering fixes the required tier split; these positions are not a measured difference.</p>' if ties > 1 else '')
    return head + body + tie_note + evidence(data, info) + '</section>'


def row(car, cats, rank):
    cells = ''.join(
        f'<span class="cell" data-category="{cat["key"]}" data-label="{escape(cat["short"])}" '
        f'title="{escape(cat["label"])}: {signed(car["scores"][cat["key"]])} (relative estimate)" '
        f'aria-label="{escape(cat["label"])}: {signed(car["scores"][cat["key"]])}">{pill(car["scores"][cat["key"]])}</span>'
        for cat in cats)
    warning = '<small class="availability">CA eligibility unresolved</small>' if car.get('eligibility_note') else ''
    return (f'<a class="car{" first" if rank == 1 else ""}" data-id="{car["id"]}" href="#detail-{car["id"]}" aria-label="Details for {escape(car["name"])}">'
            f'<span class="rank">{rank:02}</span><span class="name">{escape(car["name"])}{warning}</span>'
            f'<strong class="total">{signed(car["total"])}</strong><span class="cells">{cells}</span><span class="arrow" aria-hidden="true">›</span></a>')


def modal(data, car):
    cid = car['id']
    warning = ''
    if car.get('eligibility_note'):
        warning = f'<p class="notice">{escape(car["eligibility_note"])}</p>' + ''.join(link(data['sources'][s]) for s in car['eligibility_sources'])
    return (f'<section class="modal" id="detail-{cid}" aria-labelledby="title-{cid}">'
            '<a class="scrim" href="#ranking" aria-label="Close details"></a>'
            f'<div class="modal-panel" role="dialog" aria-modal="true" aria-labelledby="title-{cid}" tabindex="-1">'
            '<div class="modal-header"><div><small>Provisional comparison</small>'
            f'<h2 id="title-{cid}">{escape(car["name"])}</h2><p class="modal-trim">{car["year"]} · {escape(car["trim"])}</p></div>'
            '<a class="close" href="#ranking" aria-label="Close details">×</a></div>'
            f'{warning}<div class="statrow"><div><small>Weighted score</small><b data-total="{cid}">{signed(car["total"])}</b></div>'
            f'<div><small>Est. OTD</small><b>{money(car["otd"])}</b></div><div><small>Est. 5-year cost</small><b>{money(car["five"])}</b></div>'
            f'<div><small>Energy reference*</small><b>{escape(car["efficiency"])}</b></div></div>'
            '<p class="evidence">*Carried-forward MPG/MPGe estimate, not the eco score. New model-year figures and exact equipment need verification.</p>'
            '<div class="details">' + ''.join(assessment(data, car, cat) for cat in data['categories']) + '</div>'
            '<div class="modal-foot">Relative tiers include estimates · Upkeep starts at 0× · '
            '<a class="source" href="#method">Method and source limitations</a></div></div></section>')


def render(data):
    cars = prepare(data)
    cats = data['categories']
    controls = []
    for cat in cats:
        key = cat['key']
        controls.append(f'<div class="slider-unit"><div class="line"><label for="w-{key}">{escape(cat["label"])}</label>'
                        f'<output id="v-{key}" for="w-{key}">{cat["default"]}×</output></div>'
                        f'<input id="w-{key}" type="range" value="{cat["default"]}" min="0" max="3" step="0.5" '
                        f'aria-label="{escape(cat["label"])} weight"></div>')
    payload = dict(categories=cats, cars=[{k: c[k] for k in ('id', 'name', 'five', 'scores')} for c in cars])
    # Script-safe even if future research text contains HTML-like strings.
    runtime_json = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('&', '\\u0026')
    handoff = (f'Generated {data["updated"]}. Edit data.json + template.html; run python3 scripts/build_car_rankings.py.\n'
               '36-car new-vehicle shortlist retained; compact-ish, factory power hatch, estimated <= $60k OTD in Orange County.\n'
               'All research estimates are provisional. No current quote/eligibility audit. CA Corsair issue is flagged.\n'
               'Keys: cost, eco, mountain, lux, commute, maintenance. First five default 1; maintenance default 0.\n'
               'Scores: forced equal thirds, ties by case-insensitive vehicle name. Totals tie by five-year cost then name.\n'
               'Eco: named 2024 ACEEE benchmark, not an exact 2026 score. No cross-provider numerical mixing.\n'
               'Mountain: three adults and gear, roof route conditional; no measured board fit asserted.\n'
               'Commute: only named equipment; no unselected upgrade credit. Cabin assistance credit excluded.\n'
               'Maintenance: low-confidence disruption/upkeep/access estimate, not a RepairPal or fixability rating.\n'
               'Keep offline static fallback, CSS hash modals, mobile simplicity and source/estimate metadata.\n'
               'Do not edit generated index.html directly; --check verifies consistency.\n')
    return Template((PAGE / 'template.html').read_text()).substitute(
        handoff=handoff, count=len(cars), updated=escape(data['updated']),
        controls='\n'.join(controls),
        headers=''.join(f'<span data-category="{c["key"]}" title="{escape(c["label"])}">{escape(c["short"])}</span>' for c in cats),
        rows='\n'.join(row(car, cats, i + 1) for i, car in enumerate(cars)),
        leader=f'Leader: {escape(cars[0]["name"])} ({signed(cars[0]["total"])})',
        modals='\n'.join(modal(data, car) for car in cars),
        runtime_json=runtime_json,
        source_aceee=link(data['sources']['aceee_method']),
        source_coverage=link(data['sources']['aceee_coverage']),
        source_ncap=link(data['sources']['ncap']),
        source_cr=link(data['sources']['cr_adas']), source_iihs=link(data['sources']['iihs_adas']),
        source_repairpal=link(data['sources']['repairpal']),
        source_roof=link(data['sources']['roof']), source_chains=link(data['sources']['chains']),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if the tracked HTML differs from generated output')
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
