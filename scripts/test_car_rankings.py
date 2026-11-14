#!/usr/bin/env python3
"""Dependency-free data/generation checks: python3 scripts/test_car_rankings.py."""

from collections import Counter
from copy import deepcopy
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest

import build_car_rankings as build


class PageParser(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class RankingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((build.PAGE / 'data.json').read_text())
        cls.cars = build.prepare(cls.data)
        cls.html = build.render(cls.data)
        cls.elements = PageParser(cls.html).elements

    def test_generated_page_is_current(self):
        self.assertEqual((build.PAGE / 'index.html').read_text(), self.html)

    def test_every_car_has_six_balanced_tiers(self):
        self.assertEqual(len(self.cars), 36)
        for key in build.KEYS:
            self.assertEqual(Counter(c['scores'][key] for c in self.cars), {-1: 12, 0: 12, 1: 12})
            self.assertEqual(sorted(c['ranks'][key] for c in self.cars), list(range(1, 37)))

    def test_all_rendered_vehicles_have_matching_details(self):
        rows = [a for tag, a in self.elements if tag == 'a' and 'car' in a.get('class', '').split()]
        modals = [a for tag, a in self.elements if a.get('id', '').startswith('detail-')]
        self.assertEqual(len(rows), 36)
        self.assertEqual(len(modals), 36)
        self.assertEqual({r['href'][1:] for r in rows}, {m['id'] for m in modals})
        ids = [a['id'] for _, a in self.elements if 'id' in a]
        self.assertEqual(len(ids), len(set(ids)))

    def test_defaults_and_controls_preserve_optional_maintenance(self):
        sliders = [a for tag, a in self.elements if tag == 'input']
        self.assertEqual([s['value'] for s in sliders], ['1'] * 5 + ['0'])
        self.assertTrue(all((s['min'], s['max'], s['step']) == ('0', '3', '0.5') for s in sliders))
        self.assertEqual({s['id'] for s in sliders}, {'w-' + key for key in build.KEYS})
        for car in self.cars:
            self.assertEqual(car['total'], sum(car['scores'][key] for key in build.KEYS[:-1]))

    def test_cost_and_eco_tiers_follow_their_evidence(self):
        for key, raw in [('cost', lambda c: -c['five']), ('eco', lambda c: c['eco']['benchmark_score'])]:
            ordered = sorted(self.cars, key=lambda c: c['ranks'][key])
            self.assertEqual([raw(c) for c in ordered], sorted([raw(c) for c in ordered], reverse=True))

    def test_identical_evidence_is_broken_by_name_not_old_rank(self):
        data = deepcopy(self.data)
        for car in data['cars']:
            car['eco']['benchmark_score'] = 50
        result = build.prepare(data)
        ordered = sorted(result, key=lambda c: c['ranks']['eco'])
        self.assertEqual([c['name'].casefold() for c in ordered], sorted(c['name'].casefold() for c in result))
        self.assertEqual(Counter(c['scores']['eco'] for c in result), {-1: 12, 0: 12, 1: 12})

    def test_default_totals_tie_by_ownership_cost_then_name(self):
        for a, b in zip(self.cars, self.cars[1:]):
            self.assertLessEqual((-a['total'], a['five'], a['name'].casefold()), (-b['total'], b['five'], b['name'].casefold()))

    def test_each_new_assessment_identifies_uncertainty_and_source_scope(self):
        for car in self.data['cars']:
            for key in ('eco', 'mountain', 'commute', 'maintenance'):
                info = car[key]
                self.assertIn('estimate', info['status'].lower())
                self.assertTrue(info['source_year'])
                self.assertTrue(info['configuration'])
                self.assertTrue(info['sources'])
            self.assertEqual(car['eco']['benchmark_year'], 2024)
            self.assertIn('Unmeasured', car['mountain']['interior_fit'])
            self.assertIn('unverified', car['mountain']['roof'])
            self.assertTrue(car['maintenance']['repairability'])

    def test_no_external_runtime_dependency(self):
        for tag, attrs in self.elements:
            if tag in ('script', 'img', 'iframe', 'link'):
                self.assertNotIn('src', attrs)
                self.assertNotIn('href', attrs)
        self.assertNotIn('fetch(', self.html)
        self.assertNotIn('XMLHttpRequest', self.html)
        self.assertNotIn('w-mpg', self.html)
        self.assertNotIn('w-snow', self.html)
        self.assertNotIn('w-looks', self.html)

    def test_invalid_inputs_fail_before_generating_a_misleading_page(self):
        invalid = deepcopy(self.data)
        invalid['cars'].pop()
        with self.assertRaises(ValueError):
            build.prepare(invalid)
        invalid = deepcopy(self.data)
        invalid['cars'][0]['commute']['components'][0] = 6
        with self.assertRaises(ValueError):
            build.prepare(invalid)
        invalid = deepcopy(self.data)
        invalid['cars'][0]['eco']['sources'] = ['nonexistent']
        with self.assertRaises(ValueError):
            build.prepare(invalid)

    def test_derived_scores_do_not_overwrite_research_inputs(self):
        original = deepcopy(self.data)
        build.prepare(self.data)
        self.assertEqual(self.data, original)
        self.assertTrue(all('scores' not in c for c in self.data['cars']))


if __name__ == '__main__':
    unittest.main()
