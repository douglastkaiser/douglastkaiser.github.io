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
    print(f'Browser passed: {len(cars)} cars, {len(cases)} weight scenarios, reset, offline/no-JS, desktop/mobile, dialogs/focus; screenshots: {output}')


if __name__ == '__main__':
    main()
