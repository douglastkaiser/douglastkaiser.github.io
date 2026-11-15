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
    check('20 comparable · 25 missing' in page.locator('#pareto-coverage').inner_text(), 'Default coverage drift')
    network(15, 18)
    check(page.locator('#pareto-stage .pareto-layer').count() == 6, 'Wrong default layers')
    page.locator('#pareto-car').select_option('gti')
    check(page.locator('#pareto-alternative').input_value() == 'seltos', 'Wrong next dominator for GTI')
    check('Kia Seltos' in page.locator('.next-upgrade').inner_text(), 'Next dominator not explained')
    check(page.locator('#pareto-links .is-path').count() > 0, 'Preferred path not highlighted')
    positions = page.locator('.pareto-node').evaluate_all('nodes => nodes.map(n => [n.offsetLeft,n.offsetTop])')
    weights({'cost': 2})
    check(page.locator('.pareto-node').evaluate_all('nodes => nodes.map(n => [n.offsetLeft,n.offsetTop])') == positions, 'Positive weights moved nodes')
    network(15, 18)
    page.locator('#reset').click()
    page.screenshot(path=str(output / 'pareto-desktop.png'), full_page=True)

    page.locator('#pareto-car').select_option('x1')
    check(page.locator('#pareto-stage .is-selected [data-primary]').inner_text() == byid['x1']['name'], 'Equivalent member selection lost')
    page.locator('#pareto-stage .is-selected details summary').click()
    page.locator('#pareto-stage .is-selected details [data-select="cx30"]').click()
    check(page.locator('#pareto-car').input_value() == 'cx30', 'Shared node member button did not select car')
    page.locator('#pareto-list-button').click()
    check(page.locator('#pareto-list').is_visible(), 'Grouped list did not open')
    page.locator('#pareto-list [data-select="gti"]').first.click()
    check(page.locator('#pareto-car').input_value() == 'gti', 'List selection did not update car')
    page.locator('#pareto-network-button').click()

    page.locator('#pareto-car').select_option('civic')
    check('Missing active-metric evidence' in page.locator('#pareto-comparison').inner_text(), 'Unknown Eco was classified')
    check('No dominating alternative' not in page.locator('#pareto-comparison').inner_text(), 'Unknown was shown as frontier')
    check(page.locator('#pareto-stage .is-selected').count() == 0, 'Unknown appeared in graph')
    page.locator('#pareto-without-eco').click()
    check(float(page.locator('#w-eco').input_value()) == 0, 'Compare without Eco did not update shared slider')
    check('45 comparable · 0 missing' in page.locator('#pareto-coverage').inner_text(), 'Eco-off coverage drift')
    check(page.locator('#pareto-car').input_value() == 'civic', 'Selected car lost after becoming comparable')
    network(26, 45)
    weights({'eco': 1})
    check('Missing active-metric evidence' in page.locator('#pareto-comparison').inner_text(), 'Selection did not become incomplete')
    page.locator('#pareto-scale').select_option('5')
    network(19, 23)
    check(page.locator('#pareto-car').input_value() == 'civic', 'Scale change lost selected car')
    check(page.locator('#pareto-scale-note').is_visible(), 'Experimental explanation missing')
    page.locator('#pareto-comparison a').first.click()
    check(page.locator('#detail-civic [data-total]').inner_text() == build.signed(sum(byid['civic']['scores5'][k] * defaults[k] for k in build.KEYS)), 'Experimental dialog total drift')
    check('5 levels' in page.locator('#detail-civic .statrow').inner_text(), 'Dialog did not label scale')
    check(page.locator('#detail-civic [data-assessment="eco"] .pill').inner_text() == '—', 'Experimental unknown became zero')
    for key in build.KEYS:
        if byid['civic']['assessed'][key]:
            check(page.locator(f'#detail-civic [data-assessment="{key}"] .pill').inner_text() == build.signed(byid['civic']['scores5'][key]), 'Experimental dialog pill drift')
    page.keyboard.press('Escape')
    page.wait_for_function("!document.getElementById('main').inert")
    check(page.locator('#pareto').is_visible(), 'Dialog close lost Pareto tab')
    check(page.locator('#pareto-comparison a').first.evaluate('el => document.activeElement === el'), 'Pareto dialog did not restore focus')

    page.locator('#tab-rankings').click()
    check(page.locator('#ranking .car').evaluate_all('rows => rows.map(r => r.dataset.id)') == [c['id'] for c in cars], 'Experiment changed baseline ranking')
    page.locator('#ranking [data-id="civic"]').click()
    page.wait_for_function("document.activeElement.closest('#detail-civic') !== null")
    check(page.locator('#detail-civic [data-total]').inner_text() == build.signed(byid['civic']['total']), 'Rankings retained experimental total')
    check('5 levels' not in page.locator('#detail-civic .statrow').inner_text(), 'Rankings retained experimental label')
    page.keyboard.press('Escape')
    page.wait_for_function("!document.getElementById('main').inert")
    page.locator('#tab-pareto').click()
    check(page.locator('#pareto-scale').input_value() == '5', 'Tab switch forgot experiment')
    page.locator('#pareto-car').select_option('seltos')
    page.locator('#pareto-incomplete').evaluate('el => el.open = false')
    page.screenshot(path=str(output / 'pareto-five-levels.png'), full_page=True)

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
    check(page.locator('#pareto-incomplete').is_hidden(), 'All-zero state excluded unknown cars')
    weights({**defaults, 'maintenance': 1})
    network(19, 24)
    page.locator('#reset').click()
    check(float(page.locator('#w-maintenance').input_value()) == 0, 'Pareto reset did not restore maintenance')
    network(19, 23)

    page.goto(uri + '?view=pareto&scale=5#detail-civic')
    check(page.locator('#detail-civic').is_visible(), 'Pareto detail deep link failed')
    page.locator('#detail-civic .close').click()
    page.wait_for_function("!document.getElementById('main').inert")
    check(page.locator('#pareto').is_visible(), 'Deep-linked close lost tab')
    check(page.locator('#pareto-scale').input_value() == '5', 'Deep-linked scale lost')
    page.locator('#tab-pareto').focus()
    page.keyboard.press('ArrowLeft')
    check(page.locator('#tab-rankings').get_attribute('aria-selected') == 'true', 'Keyboard tabs failed')
    page.keyboard.press('ArrowRight')
    check(page.locator('#tab-pareto').get_attribute('aria-selected') == 'true', 'Keyboard return failed')


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
        check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Desktop horizontal overflow')
        page.screenshot(path=str(output / 'desktop.png'))
        opener = page.locator('#ranking [data-id="civic"]')
        opener.click()
        page.wait_for_function("document.activeElement.closest('#detail-civic') !== null")
        panel = page.locator('#detail-civic .modal-panel')
        check(panel.is_visible(), 'Detail did not open')
        check(page.locator('#main').evaluate('el => el.inert'), 'Background not inert')
        check('Power liftgate 0/5 (10%)' in panel.inner_text(), 'Liftgate evidence missing')
        check('class="pill unscored"' in panel.inner_html(), 'Missing eco presented as an ordinary tier')
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
        coverage = f'{sum(c["eco"]["benchmark_score"] is not None for c in cars)}/{len(cars)}'
        check(coverage in page.locator('#method').inner_text(), 'Coverage text drift')
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
    print(f'Browser passed: {len(cars)} cars, {len(cases)} ranking weight scenarios, Pareto networks/scales/coverage/selection, reset, offline/no-JS, desktop/mobile, dialogs/focus; screenshots: {output}')


if __name__ == '__main__':
    main()
