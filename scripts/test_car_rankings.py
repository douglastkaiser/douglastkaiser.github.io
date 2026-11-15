#!/usr/bin/env python3
"""Offline arithmetic, evidence contracts and generation tests (standard library only)."""
from collections import Counter
from copy import deepcopy
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
        self.assertEqual(build.tiers([3, 2, 1]), [(1, 1), (0, 2), (-1, 3)])
        self.assertEqual(build.tiers([2, 1]), [(1, 1), (-1, 2)])
        self.assertEqual(build.tiers([4]), [(0, 1)])
        self.assertEqual(build.tiers([]), [])
        for n in range(1, 20):
            result = build.tiers(list(range(n)))
            self.assertEqual(len(result), n)
            self.assertEqual([rank for _, rank in result], list(range(n, 0, -1)))

    def test_equal_values_keep_shared_tier_and_rank(self):
        self.assertEqual(build.tiers([5, 4, 4, 4, 1]), [(1, 1), (0, 2), (0, 2), (0, 2), (-1, 5)])
        self.assertEqual(build.tiers([9] * 7), [(0, 1)] * 7)

    def test_exact_third_boundaries_are_middle(self):
        self.assertEqual(build.tiers([3, 3, 2]), [(0, 1), (0, 1), (-1, 3)])
        self.assertEqual(build.tiers([3, 2, 2]), [(1, 1), (0, 2), (0, 2)])
        self.assertEqual(build.tiers([10, 9, 9, 8, 7, 6])[1:3], [(0, 2)] * 2)

    def test_unknowns_are_not_in_percentile_denominator(self):
        self.assertEqual(build.tiers([None, 3, 2, 1]), [(0, None), (1, 1), (0, 2), (-1, 3)])
        self.assertEqual(build.tiers([None, None]), [(0, None), (0, None)])


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
            self.assertTrue(set(c['scores'][key] for c in self.cars) <= {-1, 0, 1})

    def test_each_row_has_one_detail_and_no_duplicate_ids(self):
        rows = [a for tag, a in self.elements if tag == 'a' and 'car' in a.get('class', '').split()]
        modals = [a for _, a in self.elements if a.get('id', '').startswith('detail-')]
        self.assertEqual(len(rows), len(self.cars))
        self.assertEqual(len(modals), len(self.cars))
        self.assertEqual({r['href'][1:] for r in rows}, {m['id'] for m in modals})
        ids = [a['id'] for _, a in self.elements if 'id' in a]
        self.assertEqual(len(ids), len(set(ids)))

    def test_controls_and_optional_maintenance(self):
        sliders = [a for tag, a in self.elements if tag == 'input']
        self.assertEqual([s['value'] for s in sliders], ['1'] * 5 + ['0'])
        self.assertTrue(all((s['min'], s['max'], s['step']) == ('0', '3', '0.5') for s in sliders))
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

    def test_missing_eco_renders_dash_and_no_rank(self):
        missing = [c for c in self.cars if c['eco']['benchmark_score'] is None]
        self.assertTrue(missing)
        for c in missing:
            self.assertEqual(c['scores']['eco'], 0); self.assertIsNone(c['ranks']['eco'])
            html = build.assessment(self.data, c, self.data['categories'][1])
            self.assertIn('Unscored', html); self.assertIn('class="pill unscored">—', html)
            self.assertNotIn('joint #', html)
        data = deepcopy(self.data)
        for c in data['cars']:
            c['eco'].update(benchmark_score=None, benchmark_year=None, status='Unscored')
        self.assertTrue(all(c['scores']['eco'] == 0 for c in build.prepare(data)))
        self.assertIn('0/' + str(len(data['cars'])), build.render(data))

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

    def test_all_evidence_is_scoped_and_unscored_eco_is_explicit(self):
        for c in self.data['cars']:
            for key in ('cost','eco','mountain','comfort','commute','maintenance'):
                info = c[key]
                for name in ('status','source_year','configuration','note','sources'): self.assertTrue(info[name])
            e = c['eco']
            if e['benchmark_score'] is not None:
                self.assertEqual(e['benchmark_score'], e['benchmark_record']['score'])
                self.assertTrue(e['comparable']); self.assertEqual(e['benchmark_record']['year'], 2024)
                self.assertEqual(e['benchmark_record']['make'].casefold(), c['manufacturer'].casefold())
            else:
                self.assertEqual(e['status'], 'Unscored')

    def test_no_runtime_network_or_stale_method_claims(self):
        for tag, attrs in self.elements:
            if tag in ('script','img','iframe','link'):
                self.assertNotIn('src', attrs); self.assertNotIn('href', attrs)
        self.assertNotIn('fetch(', self.html); self.assertNotIn('XMLHttpRequest', self.html)
        for stale in ('exactly twelve','forced equal thirds','Factory power liftgate','36-car shortlist','Carried-forward MPG','retained planning input'):
            self.assertNotIn(stale, self.html)

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
        # Isolate registration arithmetic: five registrations, not six.
        base=build.registration(a['purchase'],False,self.a)
        self.assertEqual(a['first_registration']-base,121)
        self.assertEqual(build.dollars(a['renewals']-sum(build.registration(a['purchase']*v,False,self.a) for v in self.a['renewal_value_factors'])),484)

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
