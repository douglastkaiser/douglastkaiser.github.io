#!/usr/bin/env python3
"""Offline arithmetic, evidence contracts and generation tests (standard library only)."""
from collections import Counter
from copy import deepcopy
from html import escape
from html.parser import HTMLParser
from decimal import Decimal, ROUND_HALF_UP
import json
import math
import random
import unittest

import build_car_rankings as build


class PageParser(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.elements = []; self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class TierTests(unittest.TestCase):
    def test_distinct_values_and_arbitrary_sizes(self):
        self.assertEqual(build.tiers([5, 4, 3, 2, 1]), [(2, 1), (1, 2), (0, 3), (-1, 4), (-2, 5)])
        self.assertEqual(build.tiers([3, 2, 1]), [(2, 1), (0, 2), (-2, 3)])
        self.assertEqual(build.tiers([2, 1]), [(1, 1), (-1, 2)])
        self.assertEqual(build.tiers([4]), [(0, 1)])
        self.assertEqual(build.tiers([]), [])
        for n in range(1, 20):
            result = build.tiers(list(range(n)))
            self.assertEqual(len(result), n)
            self.assertEqual([rank for _, rank in result], list(range(n, 0, -1)))

    def test_equal_values_keep_shared_tier_and_rank(self):
        self.assertEqual(build.tiers([5, 4, 4, 4, 1]), [(2, 1), (0, 2), (0, 2), (0, 2), (-2, 5)])
        self.assertEqual(build.tiers([9] * 7), [(0, 1)] * 7)

    def test_fifth_boundaries_go_toward_neutral(self):
        self.assertEqual(build.tiers([5, 5, 3, 1, 1]), [(1, 1), (1, 1), (0, 3), (-1, 4), (-1, 4)])
        self.assertEqual([s for s, _ in build.tiers([5, 4, 4, 3, 2])], [2, 0, 0, -1, -2])
        self.assertEqual([s for s, _ in build.tiers([5, 4, 3, 3, 2])], [2, 1, 0, 0, -2])

    def test_incomplete_and_nonfinite_values_are_rejected(self):
        for invalid in (None, float('nan'), float('inf'), -float('inf'), True, '3'):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                build.tiers([5, invalid, 1])


class RankingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((build.PAGE / 'data.json').read_text())
        cls.cars = build.prepare(cls.data)
        cls.html = build.render(cls.data)
        cls.elements = PageParser(cls.html).elements

    def test_generated_page_is_current(self):
        self.assertEqual((build.PAGE / 'index.html').read_text(), self.html)

    def test_projects_page_matches_the_ranked_cohort(self):
        projects = (build.ROOT / 'projects/index.html').read_text()
        self.assertIn(f'Compare {len(self.cars)} new-car configurations', projects)
        self.assertIn('src="car-rankings/"', projects)

    def test_each_value_group_has_same_score_and_rank(self):
        for key in build.KEYS:
            groups = {}
            for car in self.cars:
                raw = build.value(car, key)
                pair = (car['scores'][key], car['ranks'][key])
                if raw in groups:
                    self.assertEqual(groups[raw], pair)
                groups[raw] = pair
            self.assertTrue(set(c['scores'][key] for c in self.cars) <= {-2, -1, 0, 1, 2})

    def test_each_row_has_one_detail_and_no_duplicate_ids(self):
        rows = [a for tag, a in self.elements if tag == 'a' and 'car' in a.get('class', '').split()]
        modals = [a for _, a in self.elements if a.get('id', '').startswith('detail-')]
        self.assertEqual(len(rows), len(self.cars))
        self.assertEqual(len(modals), len(self.cars))
        self.assertEqual({r['href'][1:] for r in rows}, {m['id'] for m in modals})
        ids = [a['id'] for _, a in self.elements if 'id' in a]
        self.assertEqual(len(ids), len(set(ids)))

    def test_controls_and_optional_sporty(self):
        sliders = [a for tag, a in self.elements if tag == 'input' and a.get('type') == 'range']
        self.assertEqual([s['value'] for s in sliders], ['1'] * 5 + ['0'])
        self.assertTrue(all((s['min'], s['max'], s['step']) == ('0', '2', '0.01') for s in sliders))
        self.assertEqual({s['id'] for s in sliders}, {'w-' + key for key in build.KEYS})
        for c in self.cars:
            self.assertEqual(c['total'], sum(c['scores'][k] for k in build.KEYS[:-1]))

    def test_default_sort_and_payload_agree_with_static_rows(self):
        for a, b in zip(self.cars, self.cars[1:]):
            self.assertLessEqual((-a['total'], a['five'], a['name'].casefold()), (-b['total'], b['five'], b['name'].casefold()))
        payload = self.html.split('<script id="ranking-data" type="application/json">')[1].split('</script>')[0]
        runtime = json.loads(payload)
        self.assertEqual([c['id'] for c in runtime['cars']], [c['id'] for c in self.cars])
        for c, r in zip(self.cars, runtime['cars']):
            self.assertEqual(c['scores'], r['scores']); self.assertEqual(c['five'], r['five'])

    def test_one_complete_score_payload(self):
        runtime = json.loads(self.html.split('<script id="ranking-data" type="application/json">')[1].split('</script>')[0])
        for car in runtime['cars']:
            self.assertEqual(set(car), {'id', 'name', 'five', 'scores'})
            self.assertEqual(set(car['scores']), set(build.KEYS))
            self.assertTrue(all(type(v) is int and -2 <= v <= 2 for v in car['scores'].values()))
        for car in self.cars:
            self.assertTrue(all(car['ranks'][k] is not None for k in build.KEYS))
            self.assertEqual(set(car['assessed_counts'].values()), {len(self.cars)})
        for stale in ('scores5', 'experimental', 'Current 3 levels', 'pareto-scale', 'pareto-incomplete'):
            self.assertNotIn(stale, self.html)

    def test_selected_commute_capabilities_affect_ratings(self):
        byid = {c['id']: c for c in self.cars}
        # Selected paid/advanced features must not collapse into the basic profile.
        for enhanced, basic in (('model3', 'mache'), ('modely', 'mache'),
                                ('ioniq5', 'tucson'), ('cx5', 'cx30'),
                                ('niro', 'k4'), ('ev6', 'k4'), ('gti', 'mache')):
            self.assertGreater(build.value(byid[enhanced], 'commute'), build.value(byid[basic], 'commute'))
            # Additional capability can share a fixed band; it must not score worse.
            self.assertGreaterEqual(byid[enhanced]['scores']['commute'], byid[basic]['scores']['commute'])
        self.assertLess(byid['bolt']['scores']['commute'], byid['mache']['scores']['commute'])
        self.assertLess(build.value(byid['rdx'], 'commute'), build.value(byid['crv'], 'commute'))
        self.assertEqual(byid['model3']['calculated_cost']['subscriptions'], 99 * 12 * 5)
        self.assertEqual(byid['mache']['calculated_cost']['subscriptions'], 0)

    def test_fixed_bands_keep_baselines_neutral_and_ignore_cohort_changes(self):
        self.assertEqual([build.capability_band(v) for v in (0, 149, 150, 249, 250, 300, 320, 349, 350, 449, 450, 500)],
                         [-2, -2, -1, -1, 0, 0, 0, 0, 1, 1, 2, 2])
        for invalid in (None, True, float('nan'), -1, 501):
            with self.assertRaises(ValueError): build.capability_band(invalid)
        full = {c['id']: c for c in self.cars}
        data = deepcopy(self.data); data['cars'] = data['cars'][:3]
        for car in build.prepare(data):
            for key in ('mountain', 'lux', 'commute', 'sporty'):
                self.assertEqual(car['scores'][key], full[car['id']]['scores'][key])
        data = deepcopy(self.data)
        for car in data['cars']:
            car['comfort']['components'] = [3, 3, 3, 5 if car['equipment']['power_liftgate'] else 0]
        self.assertEqual({c['scores']['lux'] for c in build.prepare(data)}, {0})

    def test_comfort_boundaries_and_full_cohort_score_range(self):
        self.assertEqual([build.capability_band(v, 'lux') for v in (0, 199, 200, 249, 250, 300, 349, 350, 399, 400, 500)],
                         [-2, -2, -1, -1, 0, 0, 0, 1, 1, 2, 2])
        for invalid in (None, True, float('nan'), -1, 501):
            with self.assertRaises(ValueError): build.capability_band(invalid, 'lux')
        self.assertEqual({c['scores']['lux'] for c in self.cars}, {-2, -1, 0, 1, 2})
        byid = {c['id']: c for c in self.cars}
        self.assertEqual(byid['prius']['scores']['lux'], -2)
        self.assertEqual(byid['priusphev']['scores']['lux'], -2)
        self.assertEqual(byid['outback']['scores']['lux'], 2)
        for car in self.cars:
            for key in ('mountain', 'commute'):
                self.assertEqual(car['scores'][key], build.capability_band(build.value(car, key)))

    def test_full_audit_coverage_and_selected_assistance_corrections(self):
        evidence = json.loads((build.PAGE / 'evidence-audit.json').read_text())
        ids = {c['id'] for c in self.cars}
        self.assertEqual({r['id'] for r in evidence['epa_records']}, ids)
        self.assertEqual({r['id'] for r in evidence['review_coverage']}, ids)
        byid = {c['id']: c for c in self.cars}
        for record in evidence['epa_records']:
            car = byid[record['id']]
            if record['status'] == 'retrieved':
                raw = record['record']
                self.assertEqual(str(car['year']), raw['year'])
                self.assertEqual(str(car['energy']['epa_id']), raw['id'])
                self.assertEqual(car['manufacturer'], raw['make'])
                self.assertEqual(car['energy']['epa_model'], raw['model'])
                self.assertEqual(car['energy']['drive'], raw['drive'])
                key, rawkey = ('kwh_per_100_miles', 'combE') if car['powertrain'] == 'EV' else ('mpg', 'comb08')
                self.assertAlmostEqual(car['energy'][key], float(raw[rawkey]), places=3)
        for car in self.cars:
            self.assertIn(car['score_audit']['review_source'], car['comfort']['sources'])
            self.assertIn('Review evidence and confidence', build.modal(self.data, car))
        self.assertEqual(byid['seltos']['commute']['components'], [5, 4, 3])
        self.assertEqual(byid['tucsonphev']['commute']['components'], [5, 4, 4])
        self.assertEqual(byid['sportagephev']['commute']['components'], [4, 4, 3])

    def test_trip_rationales_and_unsupported_upgrade_validation(self):
        for car in self.cars:
            html = build.assessment(self.data, car, self.data['categories'][2])
            for note in car['mountain']['component_notes']:
                self.assertIn(escape(note), html)
        data = deepcopy(self.data)
        solterra = next(c for c in data['cars'] if c['id'] == 'solterra')
        solterra['mountain']['components'][2] = 4
        with self.assertRaisesRegex(ValueError, 'EV trip upgrade'):
            build.prepare(data)
        # Verified route evidence can support an upgrade; this is not an EV cap.
        solterra['mountain']['trip_route_evidence'] = 'Example evidence supplied by a future route study: loaded winter range, arrival reserve and charger-stop plan.'
        build.prepare(data)
        solterra['mountain']['component_notes'] = []
        with self.assertRaisesRegex(ValueError, 'three component rationales'):
            build.prepare(data)

    def test_trip_strengths_do_not_substitute_for_replenishment(self):
        cars = {c['id']: c for c in self.cars}
        self.assertEqual(cars['solterra']['scores']['mountain'], 1)
        self.assertGreater(build.value(cars['forester'], 'mountain'), build.value(cars['solterra'], 'mountain'))
        self.assertGreater(build.value(cars['outback'], 'mountain'), build.value(cars['solterra'], 'mountain'))
        # Fast refueling does not turn a restricted sedan into a top trip choice.
        self.assertEqual(cars['corolla']['mountain']['components'][2], 5)
        self.assertLess(cars['corolla']['scores']['mountain'], 0)

    def test_unsupported_comfort_and_eco_adjustments_are_rejected(self):
        data = deepcopy(self.data)
        data['cars'][0]['comfort']['components'][0] = 4
        with self.assertRaisesRegex(ValueError, 'road-test evidence'):
            build.prepare(data)
        data = deepcopy(self.data)
        data['cars'][0]['comfort']['component_notes'] = []
        with self.assertRaisesRegex(ValueError, 'four component rationales'):
            build.prepare(data)
        data = deepcopy(self.data)
        data['cars'][0]['eco']['assessment_score'] += 1
        with self.assertRaisesRegex(ValueError, 'unadjusted anchor mean'):
            build.prepare(data)

    def test_equipment_and_same_model_references_are_credited(self):
        cars = {c['id']: c for c in self.cars}
        equinox = cars['equinoxev']['eco']
        self.assertEqual(equinox['assessment_score'], 52)
        self.assertEqual(equinox['proxy_records'][0]['record']['model'], 'EQUINOX EV FWD')
        solterra = cars['solterra']
        self.assertTrue(solterra['equipment']['power_liftgate'])
        self.assertEqual(solterra['comfort']['components'][3], 5)
        self.assertEqual(solterra['commute']['components'], [4, 5, 4])
        for car in self.cars:
            html = build.assessment(self.data, car, self.data['categories'][3])
            for note in car['comfort']['component_notes']:
                self.assertIn(escape(note), html)

    def test_commute_components_have_specific_rendered_rationales(self):
        for car in self.cars:
            info = car['commute']
            self.assertTrue(info['system'])
            self.assertEqual(len(info['component_notes']), 3)
            html = build.assessment(self.data, car, self.data['categories'][4])
            for value, note in zip(info['components'], info['component_notes']):
                self.assertTrue(note.startswith(f'{value}/5:'))
                self.assertIn(escape(note), html)
            self.assertIn(escape(info['system']), html)
        for cid, excluded in (('mache', 'BlueCruise unselected'), ('bolt', 'Super Cruise unselected')):
            car = next(c for c in self.cars if c['id'] == cid)
            self.assertIn(excluded, car['commute']['system'])

    def test_input_order_and_names_do_not_change_category_scores(self):
        data = deepcopy(self.data); random.Random(42).shuffle(data['cars'])
        for i, c in enumerate(data['cars']): c['name'] = f'Renamed {i:03}'
        expected = {c['id']: (c['scores'], c['ranks']) for c in self.cars}
        self.assertEqual(expected, {c['id']: (c['scores'], c['ranks']) for c in build.prepare(data)})

    def test_identical_evidence_never_forces_thirds(self):
        data = deepcopy(self.data)
        for c in data['cars']:
            c['comfort']['components'] = [3, 3, 3, 0]
            c['equipment']['power_liftgate'] = False
        result = build.prepare(data)
        self.assertEqual({c['scores']['lux'] for c in result}, {0})
        self.assertEqual({c['ranks']['lux'] for c in result}, {1})

    def test_proxy_eco_has_a_score_rank_and_explained_sources(self):
        proxies = [c for c in self.cars if c['eco']['basis'] == 'proxy']
        self.assertTrue(proxies)
        self.assertIn(f'The other {len(proxies)} assessments', self.html)
        for car in proxies:
            html = build.assessment(self.data, car, self.data['categories'][1])
            self.assertIn('Estimated lifecycle assessment:', html)
            self.assertIn('not a published ACEEE rating', html)
            self.assertIn(car['eco']['adjustment_note'], html)
            self.assertNotIn('—</span>', html)
            self.assertIsNotNone(car['ranks']['eco'])
            for proxy in car['eco']['proxy_records']:
                self.assertIn(str(proxy['score']) + '/100', html)
                self.assertIn(self.data['sources'][proxy['source']]['url'], html)

    def test_any_cohort_size_works(self):
        for n in (1, 2, 5, 7, 11):
            data = deepcopy(self.data); data['cars'] = data['cars'][:n]
            self.assertEqual(len(build.prepare(data)), n)
            self.assertIn(f'count">{n}</span>', build.render(data))

    def test_liftgate_is_only_a_comfort_input(self):
        data = deepcopy(self.data)
        car = next(c for c in data['cars'] if c['id'] == 'civic')
        self.assertIs(car['equipment']['power_liftgate'], False)
        original = {c['id']: c for c in self.cars}
        car['equipment']['power_liftgate'] = True; car['comfort']['components'][3] = 5
        result = {c['id']: c for c in build.prepare(data)}
        for cid, changed in result.items():
            for key in build.KEYS:
                if key != 'lux': self.assertEqual(original[cid]['scores'][key], changed['scores'][key])
        self.assertEqual(build.value(result['civic'], 'lux') - build.value(original['civic'], 'lux'), 50)
        self.assertEqual(result['civic']['five'], original['civic']['five'])

    def test_lineup_has_manual_hatch_sedan_and_screening_decisions(self):
        byid = {c['id']: c for c in self.cars}
        self.assertIn('civic', byid); self.assertNotIn('mini', byid); self.assertNotIn('corsair', byid)
        self.assertTrue(any(c['body_style'] == 'Sedan' for c in self.cars))
        self.assertTrue(any(c['body_style'] == 'Hatchback' and c['equipment']['power_liftgate'] is False for c in self.cars))
        self.assertEqual(set(c['powertrain'] for c in self.cars), {'Gas', 'Hybrid', 'PHEV', 'EV'})
        screened = {c['id']: c for c in self.data['screened']}
        self.assertTrue(set(byid) <= set(screened)); self.assertIn('ioniq6', screened)
        self.assertTrue(all(c['reason'] and c['sources'] for c in screened.values()))
        self.assertTrue(all(c['otd'] <= self.data['assumptions']['budget_otd'] for c in self.cars))

    def test_energy_reference_matches_year_make_and_powertrain(self):
        for c in self.data['cars']:
            e = c['energy']
            self.assertEqual(e['epa_year'], c['year'])
            self.assertEqual(e['epa_make'], c['manufacturer'])
            if e['epa_id']:
                self.assertTrue(e['epa_model'].startswith(c['epa_model_family']))
                self.assertEqual(e['epa_powertrain'], {'Gas':'Gas', 'Hybrid':'Hybrid', 'PHEV':'Plug-in Hybrid', 'EV':'EV'}[c['powertrain']])
        y = next(c for c in self.data['cars'] if c['id'] == 'modely')
        self.assertEqual(y['energy']['epa_model'], 'Model Y Standard RWD (18in Wheels)')

    def test_all_evidence_is_scoped_and_estimates_are_distinct(self):
        historical = 0
        for car in self.data['cars']:
            for key in ('cost','eco','mountain','comfort','commute','sporty'):
                info = car[key]
                for name in ('status','source_year','configuration','note','sources'): self.assertTrue(info[name])
            eco = car['eco']
            self.assertTrue(build.finite(eco['assessment_score'], 0, 100))
            if eco['basis'] == 'historical':
                historical += 1
                self.assertEqual(eco['assessment_score'], eco['benchmark_record']['score'])
                self.assertEqual(eco['benchmark_score'], eco['benchmark_record']['score'])
                self.assertTrue(eco['comparable'])
            else:
                self.assertIsNone(eco['benchmark_score'])
                self.assertTrue(eco['proxy_records'])
                self.assertTrue(eco['adjustment_note'])
            self.assertTrue(all(type(car['equipment'][k]) is bool for k in ('power_liftgate','adaptive_cruise','lane_centering')))
        self.assertIn(f'{historical} retained assessments', self.html)
        for cid in ('cx50', 'equinoxev'):
            car = next(c for c in self.cars if c['id'] == cid)
            self.assertIn('estimated fitment', car['equipment']['estimates']['lane_centering'])
            html = build.assessment(self.data, car, self.data['categories'][4])
            self.assertIn('estimated fitment', html)

    def test_no_runtime_network_or_stale_method_claims(self):
        for tag, attrs in self.elements:
            if tag in ('script','img','iframe','link'):
                self.assertNotIn('src', attrs); self.assertNotIn('href', attrs)
        self.assertNotIn('fetch(', self.html); self.assertNotIn('XMLHttpRequest', self.html)
        for stale in ('exactly twelve','forced equal thirds','Factory power liftgate','36-car shortlist','Carried-forward MPG','retained planning input'):
            self.assertNotIn(stale, self.html)

    def test_sporty_confidence_does_not_change_scores(self):
        data = deepcopy(self.data)
        for c in data['cars']:
            c['sporty']['confidence'] = 'Different uncertainty description; no numeric adjustment'
            c['audit_note'] = 'New generation and new powertrain'
        expected = {c['id']: c['scores'] for c in self.cars}
        self.assertEqual(expected, {c['id']: c['scores'] for c in build.prepare(data)})

    def test_fun_anchors_rationales_and_cohort_independence(self):
        byid = {c['id']: c for c in self.cars}
        self.assertEqual(byid['gr86']['scores']['sporty'], 2)
        self.assertEqual(byid['miata']['scores']['sporty'], 2)
        self.assertEqual(byid['gti']['scores']['sporty'], 2)  # A manual is not required.
        self.assertTrue(all(c['scores']['sporty'] == -2 for c in self.cars if c['body_style'] == 'Minivan'))
        for c in self.cars:
            self.assertNotIn('maintenance', c)
            html = build.assessment(self.data, c, self.data['categories'][5])
            self.assertIn(escape(c['sporty']['note']), html)
            self.assertIn('Fun score = rating − 3', html)
            data = deepcopy(self.data); data['cars'] = [next(x for x in data['cars'] if x['id'] == c['id'])]
            self.assertEqual(build.prepare(data)[0]['scores']['sporty'], c['scores']['sporty'])

    def test_new_lineup_and_cost_preservation(self):
        byid = {c['id']: c for c in self.cars}
        self.assertTrue({'gr86', 'miata', 'civicsi', 'id4', 'ioniq5sel', 'tacoma'} <= set(byid))
        self.assertIn('6MT', byid['gr86']['trim'])
        self.assertIn('two seats', byid['miata']['mountain']['note'])
        self.assertIn('19inch', byid['ioniq5sel']['energy']['epa_model'])
        self.assertEqual(byid['ioniq5sel']['energy']['epa_range_miles'], 290)
        self.assertEqual(byid['tacoma']['cost']['annual_weight_fee'], 80)
        self.assertEqual(byid['tacoma']['energy']['mpg'], 21)
        self.assertFalse(byid['miata']['equipment']['adaptive_cruise'])
        self.assertFalse(byid['gr86']['equipment']['lane_centering'])
        self.assertLess(byid['civicsi']['commute']['components'][0], 4)
        self.assertEqual(byid['crv']['five'], 45091.0)
        self.assertEqual(byid['ioniq5']['five'], 49744.49)
        screened = {c['id']: c for c in self.data['screened']}
        self.assertNotIn('ariya', byid)
        self.assertIn('Held out', screened['ariya']['decision'])

    def test_eco_preserves_published_anchors_and_explains_relative_bands(self):
        byid = {c['id']: c for c in self.cars}
        self.assertEqual(byid['tucsonphev']['eco']['assessment_score'], 60)
        self.assertEqual(byid['sportagephev']['eco']['assessment_score'], 61)
        for cid, score, model in [('model3', 55, 'Model 3 RWD'), ('modely', 57, 'Model Y Long Range AWD'), ('solterra', 66, 'SOLTERRA AWD')]:
            self.assertEqual(byid[cid]['eco']['assessment_score'], score)
            self.assertEqual(byid[cid]['eco']['proxy_records'][0]['record']['model'], model)
        for c in self.cars:
            html = build.assessment(self.data, c, self.data['categories'][1])
            self.assertIn('relative to this comparison group', html)
            self.assertIn('Zero means middle band, not zero environmental benefit', html)
            self.assertIn(f'/100', html)
            self.assertIn(f'#{c["ranks"]["eco"]} of {len(self.cars)} assessed', html)
            for p in c['eco'].get('proxy_records', []):
                self.assertEqual(p['score'], p['record']['score'])

    def test_expansion_covers_missing_segments_without_mislabeling_wagons(self):
        byid = {c['id']: c for c in self.cars}
        self.assertTrue({'sienna', 'odyssey', 'carnivalhybrid', 'maverickhybrid', 'santacruz', 'outback', 'crownsignia', 'santafehybrid', 'sorentohybrid', 'highlanderhybrid', 'pilot', 'palisade'} <= byid.keys())
        self.assertEqual(byid['sienna']['body_style'], 'Minivan')
        self.assertEqual(byid['maverickhybrid']['body_style'], 'Pickup')
        self.assertEqual(byid['outback']['body_style'], 'Crossover')
        self.assertEqual(byid['crownsignia']['body_style'], 'Crossover')
        self.assertEqual(byid['maverickhybrid']['energy']['epa_id'], '50086')
        self.assertEqual(byid['maverickhybrid']['energy']['mpg'], 36)
        self.assertTrue({'ranger', 'pacificaphev', 'v60'} <= {c['id'] for c in self.data['screened']} - byid.keys())
        for kind, count in Counter(c['body_style'] for c in self.cars).items():
            self.assertIn(f'{count} {kind}', self.html)

    def test_shared_assumptions_render_from_inputs(self):
        data = deepcopy(self.data)
        data['assumptions'].update(electricity_per_kwh=.444, annual_miles=15000, insurance_per_year=3000)
        rendered = build.render(data)
        self.assertIn('$0.444/kWh', rendered)
        self.assertIn('15,000 miles/year', rendered)
        self.assertIn('75,000 miles', rendered)
        self.assertIn('$3,000/year', rendered)

    def test_names_and_runtime_data_are_escaped(self):
        data = deepcopy(self.data)
        data['cars'][0]['name'] = '<script>alert("car")</script> & Car'
        rendered = build.render(data)
        self.assertNotIn('<script>alert("car")</script>', rendered)
        self.assertIn('&lt;script&gt;', rendered)
        payload = rendered.split('<script id="ranking-data" type="application/json">')[1].split('</script>')[0]
        self.assertNotIn('<', payload)
        self.assertIn(data['cars'][0]['name'], [c['name'] for c in json.loads(payload)['cars']])

    def test_preparation_does_not_modify_research(self):
        original = deepcopy(self.data); build.prepare(self.data)
        self.assertEqual(self.data, original)
        self.assertTrue(all('scores' not in c and 'five' not in c and 'otd' not in c for c in self.data['cars']))

    def test_invalid_inputs_are_rejected(self):
        def rejects(change):
            data = deepcopy(self.data); change(data)
            with self.assertRaises(ValueError): build.prepare(data)
        for invalid in (None, float('nan'), float('inf'), -1, 101, True):
            rejects(lambda d, invalid=invalid: d['cars'][0]['eco'].update(assessment_score=invalid))
        rejects(lambda d: d['cars'][0]['eco'].pop('assessment_score'))
        rejects(lambda d: d['cars'][0]['eco'].update(basis='unscored'))
        rejects(lambda d: d['cars'][0]['eco'].update(proxy_records=[]))
        rejects(lambda d: d['cars'][0]['eco'].update(adjustment_note=''))
        rejects(lambda d: d['cars'][0]['eco']['proxy_records'][0].update(source='nonexistent'))
        rejects(lambda d: d['cars'][0]['eco'].update(benchmark_score=50))
        rejects(lambda d: next(c for c in d['cars'] if c['eco']['basis'] == 'historical')['eco'].update(assessment_score=0))
        rejects(lambda d: d['cars'][0]['equipment'].update(power_liftgate=None))
        rejects(lambda d: d['cars'][0]['equipment'].update(lane_centering=None))
        rejects(lambda d: d['cars'][0]['commute'].update(system=''))
        rejects(lambda d: d['cars'][0]['commute'].update(component_notes=[]))
        rejects(lambda d: d['cars'][0]['commute'].update(component_notes=['valid', None, 'valid']))
        for rating in (None, True, 0, 6, 3.5, '5'):
            rejects(lambda d, rating=rating: d['cars'][0]['sporty'].update(rating=rating))
        rejects(lambda d: d['cars'][0]['sporty'].update(note=''))
        rejects(lambda d: d['cars'][0]['sporty'].update(sources=[]))
        rejects(lambda d: d['cars'][0].update(maintenance={}))
        rejects(lambda d: d['cars'][0]['eco'].update(review_note=''))
        rejects(lambda d: d['cars'][0]['eco']['proxy_records'][0]['record'].update(score=1))
        rejects(lambda d: d['cars'][0]['eco']['proxy_records'][0].update(model='Unrelated model'))
        rejects(lambda d: d['cars'].clear())
        rejects(lambda d: d['cars'].append(deepcopy(d['cars'][0])))
        rejects(lambda d: d['cars'][0]['price'].update(msrp=100000))
        rejects(lambda d: d['cars'][0]['energy'].update(mpg=0))
        rejects(lambda d: d['cars'][0]['energy'].update(epa_year=2024))
        rejects(lambda d: d['cars'][0]['energy'].update(epa_model='Unrelated model'))
        rejects(lambda d: d['cars'][0].update(five=1))
        rejects(lambda d: d['cars'][0]['commute']['components'].__setitem__(0, 6))
        rejects(lambda d: d['cars'][0]['comfort']['components'].__setitem__(3, 0))
        rejects(lambda d: d['cars'][0]['eco'].update(sources=['nonexistent']))
        rejects(lambda d: d['cars'][0]['price'].update(destination=float('nan')))
        rejects(lambda d: d['cars'][0]['equipment'].update(california_eligible=False))
        rejects(lambda d: d['assumptions'].update(annual_miles=True))
        rejects(lambda d: d['assumptions'].update(sales_tax_rate=2))
        rejects(lambda d: d['assumptions']['routine_upkeep_per_mile'].update(EV=-1))
        rejects(lambda d: d['cars'][0]['equipment'].update(adaptive_cruise=None))
        rejects(lambda d: next(c for c in d['cars'] if c['id']=='priusphev')['energy'].pop('electric_mile_share'))
        c = next(c for c in self.data['cars'] if c['id']=='civic')
        rejects(lambda d: next(c for c in d['cars'] if c['id']=='civic')['energy'].update(electric_mile_share=.5))
        rejects(lambda d: next(c for c in d['cars'] if c['id']=='bolt')['commute']['components'].__setitem__(1,4))


class CostTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((build.PAGE/'data.json').read_text())
        cls.a = cls.data['assumptions']
        cls.byid = {c['id']:c for c in cls.data['cars']}

    def test_otd_and_total_are_exact_sum_without_double_counting(self):
        for car in self.data['cars']:
            c = build.calculate_cost(car,self.a); p = car['price']
            self.assertEqual(c['purchase'],p['msrp']+p['destination']+sum(o['price'] for o in p['options']))
            expected_tax = (Decimal(str(c['purchase'] + self.a['document_fee'])) * Decimal(str(self.a['sales_tax_rate']))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            self.assertEqual(c['sales_tax'],float(expected_tax))
            self.assertEqual(c['otd'],build.dollars(c['purchase']+c['document_fee']+c['sales_tax']+c['first_registration']))
            expected = c['otd']-c['resale']+sum(c[k] for k in ('fuel','electricity','renewals','insurance','routine_upkeep','repair_reserve','subscriptions'))
            self.assertEqual(c['five'],build.dollars(expected))

    def test_energy_units_and_no_extra_charging_loss(self):
        car = deepcopy(self.byid['civic']);car['energy']['mpg']=50
        c = build.calculate_cost(car,self.a)
        self.assertEqual(c['gallons'],1200);self.assertEqual(c['kwh'],0)
        self.assertEqual(c['fuel'],build.dollars(1200*5.5049))
        car=deepcopy(self.byid['bolt']);car['energy']['kwh_per_100_miles']=30
        c = build.calculate_cost(car,self.a)
        self.assertEqual(c['gallons'],0);self.assertEqual(c['kwh'],18000)
        self.assertEqual(c['electricity'],6192)

    def test_toyota_phev_reference_is_the_selected_trim(self):
        for cid,mpg,mpge,erange in (('priusphev',52,127,44),('rav4phev',40,101,54)):
            e=self.byid[cid]['energy']
            self.assertEqual((e['mpg'],e['mpge'],e['electric_range_miles']),(mpg,mpge,erange))
            self.assertAlmostEqual(e['kwh_per_100_miles'],3370/mpge,places=5)

    def test_phev_counts_electric_and_gas_miles_separately(self):
        car=deepcopy(self.byid['priusphev']);car['energy'].update(mpg=40,kwh_per_100_miles=30,electric_mile_share=.6)
        c = build.calculate_cost(car,self.a)
        self.assertEqual(c['gallons'],600);self.assertEqual(c['kwh'],10800)
        self.assertEqual(c['fuel'],build.dollars(600*5.5049));self.assertEqual(c['electricity'],3715.2)
        for share in (0,1):
            car['energy']['electric_mile_share']=share
            c=build.calculate_cost(car,self.a)
            self.assertEqual(c['gallons'],1500*(1-share));self.assertEqual(c['kwh'],18000*share)

    def test_current_registration_brackets_and_ev_surcharge(self):
        for value,tif in ((4999,33),(5000,66),(24999,66),(25000,132),(34999,132),(35000,198),(59999,198),(60000,231)):
            self.assertEqual(build.registration(value,False,self.a),build.dollars(76+34+tif+value*.0065+30))
            self.assertEqual(build.dollars(build.registration(value,True,self.a)-build.registration(value,False,self.a)),121)
        car=deepcopy(self.byid['bolt']);a=build.calculate_cost(car,self.a);car['powertrain']='Gas'
        # New dealer-purchased EVs are exempt initially; only four renewals pay RIF.
        base=build.registration(a['purchase'],False,self.a)
        self.assertEqual(a['first_registration'],base)
        self.assertEqual(build.dollars(a['renewals']-sum(build.registration(a['purchase']*v,False,self.a) for v in self.a['renewal_value_factors'])),484)

    def test_pickup_weight_fees_apply_to_initial_registration_and_renewals(self):
        for cid, fee in [('maverickhybrid', 24), ('santacruz', 80)]:
            car = deepcopy(self.byid[cid])
            with_fee = build.calculate_cost(car, self.a)
            car['cost']['annual_weight_fee'] = 0
            without = build.calculate_cost(car, self.a)
            self.assertAlmostEqual(with_fee['otd'] - without['otd'], fee, places=2)
            self.assertAlmostEqual(with_fee['five'] - without['five'], 5 * fee, places=2)

    def test_selected_package_and_subscriptions_are_charged(self):
        bmw=self.byid['x1'];c=build.calculate_cost(bmw,self.a)
        self.assertEqual(sum(o['price'] for o in bmw['price']['options']),500)
        for cid in ('modely','model3'):
            c=build.calculate_cost(self.byid[cid],self.a)
            self.assertEqual(c['subscriptions'],99*12*5)
        self.assertEqual(build.calculate_cost(self.byid['mache'],self.a)['subscriptions'],0)

    def test_cost_moves_with_rates_without_changing_equipment(self):
        a=deepcopy(self.a);a['electricity_per_kwh']+=.1
        car=self.byid['bolt'];before=build.calculate_cost(car,self.a);after=build.calculate_cost(car,a)
        self.assertEqual(after['otd'],before['otd'])
        self.assertAlmostEqual(after['five']-before['five'],before['kwh']*.1,delta=.02)
        self.assertEqual(build.calculate_cost(self.byid['civic'],a)['five'],build.calculate_cost(self.byid['civic'],self.a)['five'])


if __name__=='__main__': unittest.main()
