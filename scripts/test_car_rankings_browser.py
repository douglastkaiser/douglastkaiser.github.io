#!/usr/bin/env python3
"""Offline browser regression check. Requires Playwright + `playwright install chromium`.
Set CHROMIUM_EXECUTABLE to use an installed Chromium. Set CAR_RANKINGS_TEST_URL
to an allowed localhost URL to serve the HTML in-process when file URLs are blocked;
contexts remain offline and external runtime requests still fail the test.

Run: python3 scripts/test_car_rankings_browser.py
Screenshots are written to /tmp/car-rankings-preview, outside the repository.
"""
import json
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

import build_car_rankings as build


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def read_weights(page):
    return page.locator('.range-wrap input').evaluate_all("inputs => Object.fromEntries(inputs.map(i => [i.id.slice(2), Number(i.value)]))")


def score(car, weights):
    return sum(car['scores'][key] * round(weights[key] * 100) for key in build.KEYS) / 100


def signed(value):
    value = round(value, 2)
    return ('+' if value > 0 else '−' if value < 0 else '') + f'{abs(value):g}'


def verify_allocation(page, cars):
    weights = read_weights(page)
    check(all(0 <= value <= 2 for value in weights.values()), f'Allocation exceeds slider cap: {weights}')
    units = sum(round(w * 100) for w in weights.values())
    check(units == sum(value > 0 for value in weights.values()) * 100, f'Budget drift: {weights}')
    check(page.locator('#allocation-caption').inner_text() == (f'{units // 100} point' + ('s' if units != 100 else '') if units else 'No priorities · sorted by cost'), 'Budget caption drift')
    expected = sorted(cars, key=lambda car: (-score(car, weights), car['five'], build.name_key(car)))
    check(page.locator('#ranking .car').evaluate_all('rows => rows.map(r => r.dataset.id)') == [c['id'] for c in expected], 'Allocation ranking mismatch')
    for car in cars:
        total = signed(score(car, weights))
        check(page.locator(f'#ranking [data-id="{car["id"]}"] .total').inner_text() == total, 'Allocation row total incorrect')
        check(page.locator(f'#detail-{car["id"]} [data-total]').inner_text() == total, 'Allocation dialog total incorrect')
    for key, value in weights.items():
        check(page.locator('#unit-' + key).evaluate("(el, off) => el.classList.contains('is-off') === off", value == 0), 'Off styling mismatch')
        check(page.locator('#unit-' + key).evaluate("(el, value) => Math.abs(parseFloat(el.style.getPropertyValue('--share')) - value * 50) < .001", value), 'Slider thumb does not match its value')
        check(page.locator('#segment-' + key).evaluate('(el, value) => Math.abs(parseFloat(el.style.width) - value * 100 / 6) < .001', value), 'Overview share mismatch')
    return weights


def check_commute_slider(page, cars, output):
    slider = page.locator('#w-commute')
    box = slider.bounding_box()
    thumb_x = box['x'] + 10 + (box['width'] - 20) / 2
    center_y = box['y'] + box['height'] / 2
    page.mouse.move(thumb_x, center_y); page.mouse.down()
    page.mouse.move(box['x'] + box['width'] * .65, center_y, steps=8)
    check(read_weights(page)['commute'] > 1, 'Real dragging did not move the direct slider')
    check(read_weights(page)['cost'] < 1, 'Real dragging did not move linked sliders')
    check(page.locator('#unit-cost').evaluate("el => Math.abs(parseFloat(el.style.getPropertyValue('--previous')) - 50) < .001"), 'Ghost marker lost interaction start')
    check(page.locator('#unit-commute').evaluate("el => el.classList.contains('is-direct')"), 'Direct manipulation indicator missing')
    page.screenshot(path=str(output / 'allocation-dragging.png'))
    page.mouse.up()
    verify_allocation(page, cars)
    page.locator('#reset').click()
    slider.focus(); slider.press('Home')
    check(page.locator('#v-commute').inner_text() == 'Off', 'Zero did not turn category off')
    check(read_weights(page)['cost'] == 1, 'Disabling an equal-weight category changed remaining allocations')
    verify_allocation(page, cars)
    slider.press('ArrowRight')
    check(read_weights(page)['commute'] == .01, 'Fine keyboard step failed')
    slider.press('End')
    # Feedback clears after 650 ms; inspect it before the full-cohort score checks.
    check(page.locator('#unit-cost').evaluate("el => el.classList.contains('is-adjusted')"), 'Automatic-change feedback missing')
    page.screenshot(path=str(output / 'allocation-adjusted.png'))
    weights = verify_allocation(page, cars)
    check(weights['commute'] == 2 and weights['cost'] == .75, 'Upper bound silently disabled categories')
    check(weights['sporty'] == 0, 'Redistribution enabled an off category')
    # Category values themselves must remain intact even as rows reorder.
    for car in cars:
        for key in build.KEYS:
            check(page.locator(f'#ranking [data-id="{car["id"]}"] [data-category="{key}"] .pill').inner_text() == build.signed(car['scores'][key]), 'Allocation changed underlying rating')
    page.locator('#reset').click()
    sporty = page.locator('#w-sporty')
    sporty.focus(); sporty.press('End')
    weights = verify_allocation(page, cars)
    check(weights['sporty'] == 2 and weights['cost'] == .8, 'Dragging an off category did not reactivate it')
    page.screenshot(path=str(output / 'allocation-six-active.png'))
    for key in build.KEYS:
        control = page.locator('#w-' + key)
        control.focus(); control.press('Home')
    verify_allocation(page, cars)
    check('No priorities' in page.locator('#allocation-caption').inner_text(), 'All-off caption missing')
    page.screenshot(path=str(output / 'allocation-all-off.png'))
    sporty.focus(); sporty.press('ArrowRight')
    check(read_weights(page)['sporty'] == 1, 'Sole active category does not fill pool')
    verify_allocation(page, cars)
    page.screenshot(path=str(output / 'allocation-one-active.png'))
    page.locator('#reset').click()
    page.set_viewport_size({'width': 390, 'height': 844})
    box = slider.bounding_box()
    slider.click(position={'x': box['width'] * .7, 'y': box['height'] / 2})
    check(read_weights(page)['commute'] > 1, 'Mobile pointer did not change allocation')
    verify_allocation(page, cars)
    page.screenshot(path=str(output / 'allocation-mobile-adjusted.png'))
    page.locator('#reset').click()
    check(slider.input_value() == '1', 'Allocation reset failed')
    page.emulate_media(reduced_motion='reduce')
    slider.focus(); slider.press('ArrowRight')
    check(page.locator('#unit-cost .slider-previous').evaluate("el => getComputedStyle(el).display") == 'none', 'Reduced motion retained ghost markers')
    check(page.locator('#unit-cost .slider-thumb').evaluate("el => getComputedStyle(el).transitionDuration") == '0s', 'Reduced motion retained transitions')
    page.locator('#reset').click()
    page.emulate_media(reduced_motion='no-preference')
    page.set_viewport_size({'width': 1280, 'height': 900})


def check_slider_snapping(page, cars):
    slider = page.locator('#w-commute')
    box = slider.bounding_box()
    center_y = box['y'] + box['height'] / 2

    def move_to(value):
        page.mouse.move(box['x'] + 10 + (box['width'] - 20) * value / 2, center_y)
        return read_weights(page)

    # Moving from a previously focused slider should still start a pointer gesture.
    page.locator('#w-cost').focus()
    move_to(1)
    page.mouse.down()
    for requested, snapped in ((.53, .5), (1.03, 1), (1.47, 1.5), (1.97, 2)):
        check(move_to(requested)['commute'] == snapped, f'Pointer did not snap near {snapped}')
    weights = move_to(1.07)
    check(1.05 <= weights['commute'] <= 1.09, 'Dragging out of the snap range did not restore fine movement')
    check(.96 <= weights['cost'] < 1, 'Redistribution snapped a linked slider near one point')
    page.mouse.up()
    verify_allocation(page, cars)
    page.locator('#reset').click()
    slider.focus(); slider.press('ArrowRight')
    check(read_weights(page)['commute'] == 1.01, 'Snapping prevented a fine keyboard step away from one point')
    page.locator('#reset').click()


def check_sorting(page, cars, output):
    def verify(key, direction):
        weights = read_weights(page)
        totals = {c['id']: score(c, weights) for c in cars}
        weighted = sorted(cars, key=lambda c: (-totals[c['id']], c['five'], build.name_key(c)))
        ranks = {c['id']: i for i, c in enumerate(weighted, 1)}
        def value(c):
            if key == 'name': return build.name_key(c)
            if key == 'rank': return ranks[c['id']]
            if key == 'total': return totals[c['id']]
            return c['scores'][key]
        # Stable tie ordering is independent of the selected direction.
        expected = sorted(weighted, key=value, reverse=direction == 'desc')
        actual = page.locator('#ranking .car').evaluate_all('rows => rows.map(r => ({id:r.dataset.id, rank:r.querySelector(".rank").textContent}))')
        check([r['id'] for r in actual] == [c['id'] for c in expected], f'{key} {direction} order mismatch')
        check(all(int(r['rank']) == ranks[r['id']] for r in actual), 'Column sort changed weighted ranks')
        check(page.locator('#leader').inner_text() == f'Leader: {weighted[0]["name"]} ({signed(totals[weighted[0]["id"]])})', 'Column sort changed leader')
        check(page.locator('[data-sort][aria-pressed="true"]').count() == 1, 'Sort selection is not unique')
        check(page.locator(f'[data-sort="{key}"]').get_attribute('aria-pressed') == 'true', 'Wrong active sort')
        check(('ascending' if direction == 'asc' else 'descending') in page.locator('#sort-status').inner_text(), 'Direction not announced')

    for key in ('rank', 'name', 'total', *build.KEYS):
        page.locator('#reset').click()
        first = 'asc' if key in ('rank', 'name', 'total') else 'desc'
        button = page.locator(f'[data-sort="{key}"]')
        button.click(); verify(key, first)
        button.click(); verify(key, 'desc' if first == 'asc' else 'asc')
    page.locator('[data-sort="eco"]').click()
    verify('eco', 'desc')
    page.locator('#w-cost').focus(); page.locator('#w-cost').press('End')
    verify('eco', 'desc')
    # Sorting remains usable with all priorities off, including the inactive metric.
    for key in build.KEYS:
        page.locator('#w-' + key).focus(); page.locator('#w-' + key).press('Home')
    verify('eco', 'desc')
    page.locator('#reset').click(); verify('total', 'desc')
    for width in (390, 320):
        page.set_viewport_size({'width': width, 'height': 844})
        for key in ('name', 'total', *build.KEYS):
            button = page.locator(f'[data-sort="{key}"]')
            check(button.is_visible(), f'{width}px {key} sort unavailable')
        page.locator('[data-sort="cost"]').focus(); page.keyboard.press('Enter'); verify('cost', 'desc')
        page.keyboard.press('Space'); verify('cost', 'asc')
        check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{width}px sort header overflow')
        page.screenshot(path=str(output / f'sorting-{width}.png'))
        page.locator('#reset').click()
    page.set_viewport_size({'width': 1280, 'height': 900})


def check_pareto(page, cars, defaults, output, uri):
    byid = {c['id']: c for c in cars}
    top_pick = 'sportage'

    def weights(values):
        page.evaluate('''weights => { Object.entries(weights).forEach(([key, value]) => {
            const input = document.getElementById('w-' + key); input.value = String(value);
            input.dispatchEvent(new Event('input', {bubbles: true}));
        }); }''', values)

    def network():
        active = [key for key in build.KEYS if float(page.locator('#w-' + key).input_value()) > 0]
        profiles = {tuple(c['scores'][key] for key in active) for c in cars if c['id'] != top_pick}
        def dominates(a, b):
            return all(x >= y for x, y in zip(a, b)) and any(x > y for x, y in zip(a, b))
        edges = [(a, b) for a in profiles for b in profiles if dominates(a, b)
                 and not any(dominates(a, middle) and dominates(middle, b) for middle in profiles)]
        frontier_size = sum(not any(dominates(other, p) for other in profiles) for p in profiles)
        remaining, layers = set(profiles), 0
        while remaining:
            front = {p for p in remaining if not any(dominates(other, p) for other in remaining)}
            remaining -= front
            layers += 1
        check(page.locator('#pareto-stage .pareto-node').count() == len(profiles) + 1, 'Wrong Pareto profile count')
        page.wait_for_function("n => document.querySelectorAll('#pareto-links [data-better]').length === n", arg=len(edges) + frontier_size)
        check(page.locator('#pareto-stage .pareto-layer').count() == layers + 1, 'Wrong Pareto layer count')
        top_tier = page.locator('#pareto-stage .pareto-layer').first
        check(top_tier.locator('h3').inner_text() == 'S+ Tier', 'Network lacks the S+ Tier label')
        check(top_tier.locator('[data-primary]').evaluate_all('buttons => buttons.map(b => b.dataset.select)') == [top_pick], 'S+ Tier is not exclusive')

    page.set_viewport_size({'width': 1280, 'height': 900})
    page.goto(uri)
    page.locator('#tab-pareto').click()
    check(page.locator('#pareto').is_visible(), 'Pareto tab did not open')
    check(not page.locator('#rankings-view').is_visible(), 'Rankings did not hide')
    check(f'{len(cars)} comparable · 5 levels' in page.locator('#pareto-coverage').inner_text(), 'Full cohort missing')
    check(page.locator('#pareto-scale,#pareto-incomplete,#pareto-without-eco').count() == 0, 'Obsolete controls remain')
    network()
    check(page.locator('#pareto-car').input_value() == top_pick, 'S+ champion is not selected initially')
    check(page.locator('#pareto-comparison .selected-total').inner_text() == build.signed(byid[top_pick]['total']), 'S+ champion score changed')
    page.locator('#pareto-car').select_option('gti')
    active = [key for key in build.KEYS if defaults[key] > 0]
    target = byid['gti']
    dominators = [c for c in cars if c['id'] != top_pick and all(c['scores'][k] >= target['scores'][k] for k in active)
                  and any(c['scores'][k] > target['scores'][k] for k in active)]
    expected = min(dominators, key=lambda c: (sum(c['scores'][k] * defaults[k] for k in build.KEYS), c['five'], build.name_key(c)))
    check(page.locator('#pareto-alternative').input_value() == expected['id'], 'Wrong next dominator for GTI')
    check(expected['name'] in page.locator('.next-upgrade').inner_text(), 'Next dominator not explained')
    page.wait_for_function("document.querySelectorAll('#pareto-links .is-path').length > 0")
    positions = page.locator('.pareto-node').evaluate_all('nodes => nodes.map(n => [n.offsetLeft,n.offsetTop])')
    weights({'cost': 2})
    check(page.locator('.pareto-node').evaluate_all('nodes => nodes.map(n => [n.offsetLeft,n.offsetTop])') == positions, 'Positive weights moved nodes')
    network()
    page.locator('#reset').click()
    page.screenshot(path=str(output / 'pareto-desktop.png'), full_page=True)

    profiles = {}
    for car in cars:
        if car['id'] == top_pick:
            continue
        profiles.setdefault(tuple(car['scores'][k] for k in active), []).append(car)
    members = next(group for group in profiles.values() if len(group) > 1)
    primary, other = members[:2]
    page.locator('#pareto-car').select_option(primary['id'])
    check(page.locator('#pareto-stage .is-selected [data-primary]').inner_text() == primary['name'], 'Equivalent member selection lost')
    page.locator('#pareto-stage .is-selected details summary').click()
    page.locator(f'#pareto-stage .is-selected details [data-select="{other["id"]}"]').click()
    check(page.locator('#pareto-car').input_value() == other['id'], 'Shared node member button failed')
    page.locator('#pareto-list-button').click()
    check(page.locator('#pareto-list').is_visible(), 'Grouped list did not open')
    top_tier = page.locator('#pareto-list .pareto-layer-list').first
    check(top_tier.locator('h3').inner_text() == 'S+ Tier', 'Grouped list lacks the S+ Tier label')
    check(top_tier.locator('[data-select]').evaluate_all('buttons => buttons.map(b => b.dataset.select)') == [top_pick], 'Grouped list lacks an exclusive S+ Tier')
    page.locator('#pareto-list [data-select="gti"]').first.click()
    check(page.locator('#pareto-car').input_value() == 'gti', 'List selection failed')
    page.locator('#pareto-network-button').click()

    page.locator('#pareto-car').select_option('civic')
    check(page.locator('#pareto-stage .is-selected').count() == 1, 'Proxy-scored car missing from graph')
    check('Missing active-metric evidence' not in page.locator('#pareto-comparison').inner_text(), 'Proxy excluded')
    weights({'eco': 0})
    network()
    check(page.locator('#pareto-car').input_value() == 'civic', 'Metric toggle lost selection')
    weights({'eco': 1})
    network()
    page.locator('#pareto-comparison a').first.click()
    check(page.locator('#detail-civic [data-total]').inner_text() == build.signed(byid['civic']['total']), 'Pareto dialog total drift')
    check('Estimated lifecycle assessment:' in page.locator('#detail-civic').inner_text(), 'Proxy rationale missing')
    for key in build.KEYS:
        check(page.locator(f'#detail-civic [data-assessment="{key}"] .pill').inner_text() == build.signed(byid['civic']['scores'][key]), 'Dialog pill drift')
    page.keyboard.press('Escape')
    page.wait_for_function("!document.getElementById('main').inert")
    check(page.locator('#pareto').is_visible(), 'Dialog close lost Pareto tab')
    check(page.locator('#pareto-comparison a').first.evaluate('el => document.activeElement === el'), 'Pareto dialog focus not restored')

    page.locator('#tab-rankings').click()
    check(page.locator('#ranking .car').evaluate_all('rows => rows.map(r => r.dataset.id)') == [c['id'] for c in cars], 'Tab switch changed ranking')
    page.locator('#ranking [data-id="civic"]').click()
    page.wait_for_function("document.activeElement.closest('#detail-civic') !== null")
    check(page.locator('#detail-civic [data-total]').inner_text() == build.signed(byid['civic']['total']), 'Rankings dialog total drift')
    page.keyboard.press('Escape')
    page.wait_for_function("!document.getElementById('main').inert")
    page.locator('#tab-pareto').click()
    check(page.locator('#pareto-car').input_value() == 'civic', 'Tab switch lost selection')
    page.locator('#pareto-car').select_option('seltos')

    for width, height in ((390, 844), (320, 700)):
        page.set_viewport_size({'width': width, 'height': height})
        page.wait_for_function("document.getElementById('pareto-network').scrollWidth <= document.getElementById('pareto-stage').offsetWidth + 2")
        page.evaluate('scrollTo(0,0)')
        check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Pareto {width}px body overflow')
        check(page.locator('#pareto-network').evaluate('el => el.scrollWidth > el.clientWidth'), 'Mobile graph is not scrollable')
        check(page.locator('#pareto-network').evaluate('el => el.clientHeight <= 480'), 'Mobile graph pushes comparison too far down')
        page.locator('#pareto-network').evaluate('el => el.scrollLeft = el.scrollWidth')
        check(page.locator('#pareto-network').evaluate('el => el.scrollLeft > 0'), 'Mobile graph did not scroll')
        check(page.locator('#pareto-stage .pareto-layer').last.evaluate('el => { const r = el.getBoundingClientRect(), s = document.getElementById("pareto-network").getBoundingClientRect(); return r.left < s.right && r.right > s.left; }'), 'Graph scrolled into a blank tail')
        page.screenshot(path=str(output / f'pareto-mobile-{width}.png'), full_page=True)
        page.locator('#pareto-list-button').click()
        check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Grouped list overflow')
        page.locator('#pareto-network-button').click()

    weights({key: 0 for key in build.KEYS})
    network()
    check('No active metrics' in page.locator('#pareto-comparison').inner_text(), 'All-zero state missing')
    check(page.locator('.next-upgrade [data-select]').get_attribute('data-select') == top_pick, 'S+ champion disappeared with all metrics off')
    weights({**defaults, 'sporty': 1})
    network()
    page.locator('#reset').click()
    check(float(page.locator('#w-sporty').input_value()) == 0, 'Pareto reset did not restore sporty')
    network()

    # Both old scale query values must preserve view/dialog and use five-level scores.
    for scale in (3, 5):
        page.goto(uri + f'?view=pareto&scale={scale}#detail-civic')
        check(page.locator('#detail-civic').is_visible(), 'Legacy Pareto detail deep link failed')
        check(page.locator('#detail-civic [data-total]').inner_text() == build.signed(byid['civic']['total']), 'Legacy link changed scale')
        page.locator('#detail-civic .close').click()
        page.wait_for_function("!document.getElementById('main').inert")
        check(page.locator('#pareto').is_visible(), 'Deep-linked close lost tab')
        check('5 levels' in page.locator('#pareto-comparison').inner_text(), 'Legacy link did not use five levels')
        page.locator('#tab-pareto').focus()
        page.keyboard.press('ArrowLeft')
        check(page.locator('#tab-rankings').get_attribute('aria-selected') == 'true', 'Keyboard tabs failed')
        page.keyboard.press('ArrowRight')
        check(page.locator('#tab-pareto').get_attribute('aria-selected') == 'true', 'Keyboard return failed')
        check('scale=' not in page.url, 'Obsolete scale persisted in generated links')


def main():
    data = json.loads((build.PAGE / 'data.json').read_text())
    cars = build.prepare(data)
    uri = os.environ.get('CAR_RANKINGS_TEST_URL', (build.PAGE / 'index.html').as_uri())
    output = Path('/tmp/car-rankings-preview'); output.mkdir(exist_ok=True)
    defaults = {c['key']: c['default'] for c in data['categories']}
    cases = [defaults, {k: 0 for k in build.KEYS}]
    cases += [{k: 2 if k == chosen else 0 for k in build.KEYS} for chosen in build.KEYS]
    cases += [dict(zip(build.KEYS, (0.5, 2, 1.5, 2, 0, 1.75)))]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=os.environ.get('CHROMIUM_EXECUTABLE'))
        context = browser.new_context(viewport={'width': 1280, 'height': 900}, offline=True)
        if os.environ.get('CAR_RANKINGS_TEST_URL'):
            context.route(uri.split('#')[0].split('?')[0] + '*', lambda route: route.fulfill(path=str(build.PAGE / 'index.html'), content_type='text/html'))
        page = context.new_page()
        errors, remote_requests = [], []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: remote_requests.append(request.url) if request.url.startswith(('http:', 'https:')) and not request.url.startswith(uri) else None)
        page.goto(uri)
        check(page.locator('#indicator').inner_text() == '● Live', 'JavaScript did not start offline')
        check(page.locator('#ranking .car').count() == len(cars), 'Missing ranking rows')
        for car in cars:
            for key in build.KEYS:
                cell = page.locator(f'#ranking [data-id="{car["id"]}"] [data-category="{key}"]')
                check(cell.inner_text() == build.signed(car['scores'][key]), 'Row score mismatch')
                basis = 'relative to this comparison group' if key in ('cost', 'eco') else 'on the fixed capability rubric'
                check(cell.get_attribute('aria-label').startswith(f'{next(cat["label"] for cat in data["categories"] if cat["key"] == key)}: {build.signed(car["scores"][key])} {basis}'), 'Accessible score mismatch')
        for requested in cases:
            page.locator('#reset').click()
            page.evaluate('''weights => { Object.entries(weights).forEach(([key, value]) => {
                const input = document.getElementById('w-' + key); input.value = String(value);
                input.dispatchEvent(new Event('input', {bubbles: true}));
            }); }''', requested)
            weights = read_weights(page)
            verify_allocation(page, cars)
            expected = sorted(cars, key=lambda c: (-score(c, weights), c['five'], build.name_key(c)))
            actual = page.locator('#ranking .car').evaluate_all("rows => rows.map(row => ({id:row.dataset.id, total:row.querySelector('.total').textContent, rank:row.querySelector('.rank').textContent}))")
            check([c['id'] for c in actual] == [c['id'] for c in expected], f'Python/browser order mismatch: {weights}')
            for i, (a, e) in enumerate(zip(actual, expected), 1):
                total = score(e, weights)
                check(a['total'] == signed(total), f'Wrong row total: {e["id"]}')
                check(a['rank'] == f'{i:02}', 'Wrong displayed rank')
                check(page.locator(f'[data-total="{e["id"]}"]').inner_text() == signed(total), 'Dialog total drift')
            check(page.locator('#main').evaluate("el => el.classList.contains('sporty-off')") == (weights['sporty'] == 0), 'Fun state drift')
        page.locator('#reset').click()
        check(page.locator('#ranking .car').evaluate_all('rows => rows.map(r => r.dataset.id)') == [c['id'] for c in cars], 'Reset order drift')
        for key in build.KEYS:
            check(float(page.locator('#w-' + key).input_value()) == defaults[key], 'Reset weights drift')
        check(page.locator('#ranking .car.first').count() == 1, 'Leader styling drift')
        check_commute_slider(page, cars, output)
        check_slider_snapping(page, cars)
        check_sorting(page, cars, output)
        fun_slider = page.locator('#w-sporty')
        fun_slider.focus(); fun_slider.press('End')
        weights = verify_allocation(page, cars)
        for car in cars:
            expected = signed(score(car, weights))
            check(page.locator(f'#ranking [data-id="{car["id"]}"] .total').inner_text() == expected, 'Sporty/Fun contribution incorrect')
            check(page.locator(f'#detail-{car["id"]} [data-total]').inner_text() == expected, 'Sporty/Fun dialog contribution incorrect')
        # Order changes with weighting, but every vehicle retains its category assessment.
        for car in cars:
            check(page.locator(f'#ranking [data-id="{car["id"]}"] [data-category=sporty] .pill').inner_text() == build.signed(car['scores']['sporty']), 'Sporty/Fun weight changed category score')
        page.locator('#reset').click()
        page.goto(uri + '#detail-tucsonphev')
        eco_text = page.locator('#detail-tucsonphev [data-assessment=eco]').inner_text()
        check('60/100' in eco_text and 'relative to this comparison group' in eco_text, 'Eco raw assessment or relative explanation missing')
        check('Fun score = rating − 3' in page.locator('#detail-tucsonphev [data-assessment=sporty]').inner_text(), 'Fun rationale missing')
        page.keyboard.press('Escape')
        page.wait_for_function("!document.getElementById('main').inert")
        check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Desktop horizontal overflow')
        page.evaluate('scrollTo(0,0)')
        page.screenshot(path=str(output / 'desktop.png'))
        opener = page.locator('#ranking [data-id="civic"]')
        opener.click()
        page.wait_for_function("document.activeElement.closest('#detail-civic') !== null")
        panel = page.locator('#detail-civic .modal-panel')
        check(panel.is_visible(), 'Detail did not open')
        check(page.locator('#main').evaluate('el => el.inert'), 'Background not inert')
        check('Power liftgate 0/5 (10%)' in panel.inner_text(), 'Liftgate evidence missing')
        check('Estimated lifecycle assessment:' in panel.inner_text(), 'Proxy estimate missing')
        page.keyboard.press('Shift+Tab')
        check(page.evaluate("document.activeElement.closest('#detail-civic') !== null"), 'Reverse focus trap failed')
        page.keyboard.press('Tab')
        check(page.evaluate("document.activeElement.closest('#detail-civic') !== null"), 'Forward focus trap failed')
        page.keyboard.press('Escape')
        page.wait_for_function("!document.getElementById('main').inert")
        check(opener.evaluate('el => document.activeElement === el'), 'Opener focus not restored')
        for width, height in ((390, 844), (320, 700)):
            page.set_viewport_size({'width': width, 'height': height})
            page.evaluate('scrollTo(0,0)')
            check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{width}px horizontal overflow')
            page.screenshot(path=str(output / f'mobile-{width}.png'))
            page.locator('#ranking [data-id="civic"]').click()
            check(page.locator('#detail-civic').is_visible(), 'Mobile dialog failed')
            check(page.locator('#detail-civic .modal-panel').evaluate('el => el.getBoundingClientRect().width <= innerWidth'), 'Mobile dialog overflow')
            page.screenshot(path=str(output / f'detail-{width}.png'))
            page.locator('#detail-civic .close').click()
        page.goto(uri + '#method')
        check(page.locator('#method').is_visible(), 'Deep-linked method failed')
        check(f'all {len(cars)} cars' in page.locator('#method').inner_text(), 'Full-cohort method text missing')
        check_pareto(page, cars, defaults, output, uri)
        check(not errors, f'Browser errors: {errors}')
        check(not remote_requests, f'Runtime requested network: {remote_requests}')
        context.close()
        fallback = browser.new_context(java_script_enabled=False, offline=True, viewport={'width':390,'height':844})
        if os.environ.get('CAR_RANKINGS_TEST_URL'):
            fallback.route(uri.split('#')[0].split('?')[0] + '*', lambda route: route.fulfill(path=str(build.PAGE / 'index.html'), content_type='text/html'))
        page = fallback.new_page(); page.goto(uri)
        check(page.locator('#ranking .car').count() == len(cars), 'No-JS rows missing')
        check(page.locator('#ranking .car').evaluate_all('rows => rows.map(r => r.dataset.id)') == [c['id'] for c in cars], 'Static fallback order mismatch')
        page.locator('#ranking [data-id="civic"]').click()
        check(page.locator('#detail-civic').is_visible(), 'No-JS detail failed')
        page.locator('#detail-civic .close').click()
        check(not page.locator('#detail-civic').is_visible(), 'No-JS close failed')
        fallback.close(); browser.close()
    print(f'Browser passed: {len(cars)} cars, {len(cases)} ranking weight scenarios, Pareto networks/full coverage/selection/legacy links, reset, offline/no-JS, desktop/mobile, dialogs/focus; screenshots: {output}')


if __name__ == '__main__':
    main()
