#!/usr/bin/env python3
"""Offline browser regression check. Requires Playwright + `playwright install chromium`.

Run: python3 scripts/test_car_rankings_browser.py
Screenshots are written to /tmp/car-rankings-preview, outside the repository.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

import build_car_rankings as build


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def check_commute_slider(page, cars):
    # Exercise actual keyboard and pointer input, rather than setting the value in JS.
    slider = page.locator('#w-commute')
    initial_order = page.locator('#ranking .car').evaluate_all('rows => rows.map(r => r.dataset.id)')
    original_pills = page.locator('#ranking .car').evaluate_all("rows => Object.fromEntries(rows.map(r => [r.dataset.id, r.querySelector('[data-category=commute]').textContent]))")
    slider.focus()
    slider.press('Home')
    check(page.locator('#v-commute').inner_text() == '0×', 'Commute keyboard Home failed')
    slider.press('ArrowRight')
    check(page.locator('#v-commute').inner_text() == '0.5×', 'Commute half-step failed')
    for car in cars:
        baseline = sum(car['scores'][key] for key in build.KEYS[:-1] if key != 'commute')
        row = page.locator(f'#ranking [data-id="{car["id"]}"]')
        check(row.locator('.total').inner_text() == build.signed(baseline + .5 * car['scores']['commute']), 'Half-weight commute total incorrect')
    slider.press('End')
    check(page.locator('#v-commute').inner_text() == '3×', 'Commute keyboard End failed')
    for car in cars:
        expected = car['total'] + 2 * car['scores']['commute']
        check(page.locator(f'#ranking [data-id="{car["id"]}"] .total').inner_text() == build.signed(expected), 'Commute weight did not change total correctly')
        check(page.locator(f'#detail-{car["id"]} [data-total]').inner_text() == build.signed(expected), 'Commute weight did not update dialog total')
    check(page.locator('#ranking .car').evaluate_all('rows => rows.map(r => r.dataset.id)') != initial_order, 'Commute slider had no effect on rankings')
    check(page.locator('#ranking .car').evaluate_all("rows => Object.fromEntries(rows.map(r => [r.dataset.id, r.querySelector('[data-category=commute]').textContent]))") == original_pills, 'Weight changed underlying category ratings')
    page.locator('#reset').click()
    page.set_viewport_size({'width': 390, 'height': 844})
    box = slider.bounding_box()
    slider.click(position={'x': box['width'] * .83, 'y': box['height'] / 2})
    actual_weight = float(slider.input_value())
    check(actual_weight > 1, 'Mobile pointer did not change commute weight')
    car = next(c for c in cars if c['id'] == 'model3')
    check(page.locator('#ranking [data-id="model3"] .total').inner_text() == build.signed(car['total'] + (actual_weight - 1) * car['scores']['commute']), 'Mobile commute contribution incorrect')
    page.locator('#reset').click()
    check(slider.input_value() == '1', 'Commute reset failed')
    page.set_viewport_size({'width': 1280, 'height': 900})


def check_pareto(page, cars, defaults, output, uri):
    byid = {c['id']: c for c in cars}

    def weights(values):
        page.evaluate('''weights => { Object.entries(weights).forEach(([key, value]) => {
            const input = document.getElementById('w-' + key); input.value = String(value);
            input.dispatchEvent(new Event('input', {bubbles: true}));
        }); }''', values)

    def network(nodes, edges):
        check(page.locator('#pareto-stage .pareto-node').count() == nodes, 'Wrong Pareto profile count')
        page.wait_for_function("n => document.querySelectorAll('#pareto-links [data-better]').length === n", arg=edges)

    page.set_viewport_size({'width': 1280, 'height': 900})
    page.goto(uri)
    page.locator('#tab-pareto').click()
    check(page.locator('#pareto').is_visible(), 'Pareto tab did not open')
    check(not page.locator('#rankings-view').is_visible(), 'Rankings did not hide')
    check('45 comparable · 5 levels' in page.locator('#pareto-coverage').inner_text(), 'Full cohort missing')
    check(page.locator('#pareto-scale,#pareto-incomplete,#pareto-without-eco').count() == 0, 'Obsolete controls remain')
    network(44, 74)
    check(page.locator('#pareto-stage .pareto-layer').count() == 5, 'Wrong default layers')
    page.locator('#pareto-car').select_option('gti')
    check(page.locator('#pareto-alternative').input_value() == 'tiguan', 'Wrong next dominator for GTI')
    check('Volkswagen Tiguan' in page.locator('.next-upgrade').inner_text(), 'Next dominator not explained')
    page.wait_for_function("document.querySelectorAll('#pareto-links .is-path').length > 0")
    positions = page.locator('.pareto-node').evaluate_all('nodes => nodes.map(n => [n.offsetLeft,n.offsetTop])')
    weights({'cost': 2})
    check(page.locator('.pareto-node').evaluate_all('nodes => nodes.map(n => [n.offsetLeft,n.offsetTop])') == positions, 'Positive weights moved nodes')
    network(44, 74)
    page.locator('#reset').click()
    page.screenshot(path=str(output / 'pareto-desktop.png'), full_page=True)

    page.locator('#pareto-car').select_option('x1')
    check(page.locator('#pareto-stage .is-selected [data-primary]').inner_text() == byid['x1']['name'], 'Equivalent member selection lost')
    page.locator('#pareto-stage .is-selected details summary').click()
    page.locator('#pareto-stage .is-selected details [data-select="cx30"]').click()
    check(page.locator('#pareto-car').input_value() == 'cx30', 'Shared node member button failed')
    page.locator('#pareto-list-button').click()
    check(page.locator('#pareto-list').is_visible(), 'Grouped list did not open')
    page.locator('#pareto-list [data-select="gti"]').first.click()
    check(page.locator('#pareto-car').input_value() == 'gti', 'List selection failed')
    page.locator('#pareto-network-button').click()

    page.locator('#pareto-car').select_option('civic')
    check(page.locator('#pareto-stage .is-selected').count() == 1, 'Proxy-scored car missing from graph')
    check('Missing active-metric evidence' not in page.locator('#pareto-comparison').inner_text(), 'Proxy excluded')
    weights({'eco': 0})
    network(40, 72)
    check(page.locator('#pareto-car').input_value() == 'civic', 'Metric toggle lost selection')
    weights({'eco': 1})
    network(44, 74)
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
    network(1, 0)
    check('No active metrics' in page.locator('#pareto-comparison').inner_text(), 'All-zero state missing')
    weights({**defaults, 'maintenance': 1})
    network(44, 59)
    page.locator('#reset').click()
    check(float(page.locator('#w-maintenance').input_value()) == 0, 'Pareto reset did not restore maintenance')
    network(44, 74)

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
    uri = (build.PAGE / 'index.html').as_uri()
    output = Path('/tmp/car-rankings-preview'); output.mkdir(exist_ok=True)
    defaults = {c['key']: c['default'] for c in data['categories']}
    cases = [defaults, {k: 0 for k in build.KEYS}]
    cases += [{k: 3 if k == chosen else 0 for k in build.KEYS} for chosen in build.KEYS]
    cases += [dict(zip(build.KEYS, (0.5, 2, 1.5, 3, 0, 2.5)))]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 900}, offline=True)
        page = context.new_page()
        errors, remote_requests = [], []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: remote_requests.append(request.url) if request.url.startswith(('http:', 'https:')) else None)
        page.goto(uri)
        check(page.locator('#indicator').inner_text() == '● Live', 'JavaScript did not start offline')
        check(page.locator('#ranking .car').count() == len(cars), 'Missing ranking rows')
        for car in cars:
            for key in build.KEYS:
                cell = page.locator(f'#ranking [data-id="{car["id"]}"] [data-category="{key}"]')
                check(cell.inner_text() == build.signed(car['scores'][key]), 'Row score mismatch')
                check(cell.get_attribute('aria-label').endswith(build.signed(car['scores'][key])), 'Accessible score mismatch')
        for weights in cases:
            page.evaluate('''weights => { Object.entries(weights).forEach(([key, value]) => {
                const input = document.getElementById('w-' + key); input.value = String(value);
                input.dispatchEvent(new Event('input', {bubbles: true}));
            }); }''', weights)
            expected = sorted(cars, key=lambda c: (-sum(c['scores'][k] * weights[k] for k in build.KEYS), c['five'], build.name_key(c)))
            actual = page.locator('#ranking .car').evaluate_all("rows => rows.map(row => ({id:row.dataset.id, total:row.querySelector('.total').textContent, rank:row.querySelector('.rank').textContent}))")
            check([c['id'] for c in actual] == [c['id'] for c in expected], f'Python/browser order mismatch: {weights}')
            for i, (a, e) in enumerate(zip(actual, expected), 1):
                score = sum(e['scores'][k] * weights[k] for k in build.KEYS)
                check(a['total'] == build.signed(score), f'Wrong row total: {e["id"]}')
                check(a['rank'] == f'{i:02}', 'Wrong displayed rank')
                check(page.locator(f'[data-total="{e["id"]}"]').inner_text() == build.signed(score), 'Dialog total drift')
            check(page.locator('#main').evaluate("el => el.classList.contains('upkeep-off')") == (weights['maintenance'] == 0), 'Upkeep state drift')
        page.locator('#reset').click()
        check(page.locator('#ranking .car').evaluate_all('rows => rows.map(r => r.dataset.id)') == [c['id'] for c in cars], 'Reset order drift')
        for key in build.KEYS:
            check(float(page.locator('#w-' + key).input_value()) == defaults[key], 'Reset weights drift')
        check(page.locator('#ranking .car.first').count() == 1, 'Leader styling drift')
        check_commute_slider(page, cars)
        check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Desktop horizontal overflow')
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
