'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const pareto = require('./car_rankings_pareto.js');
const html = fs.readFileSync(path.join(__dirname, '../projects/car-rankings/index.html'), 'utf8');
const data = JSON.parse(html.match(/<script id="ranking-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const defaults = Object.fromEntries(data.categories.map(cat => [cat.key, cat.default]));
const categories = [{ key: 'x' }, { key: 'y' }];
function car(id, x, y, five = 100, assessed = { x: true, y: true }) {
  return { id, name: id, five, scores: { x, y }, scores5: { x, y }, assessed };
}
function ids(cars) { return cars.map(car => car.id); }
function pairs(graph) { return graph.edges.map(e => [graph.groups[e.better].members[0].id, graph.groups[e.worse].members[0].id].join('>')).sort(); }

test('chains reduce transitively and equal profiles never dominate each other', () => {
  const cars = [car('a', 2, 2), car('b', 1, 1), car('b2', 1, 1), car('c', 0, 0)];
  const weights = { x: 1, y: 1 }, g = pareto.buildGraph(cars, categories, weights, 3);
  assert.equal(g.groups.length, 3);
  assert.deepEqual(pairs(g), ['a>b', 'b>c']);
  assert.deepEqual(g.layers.map(layer => layer.length), [1, 1, 1]);
  assert.deepEqual(ids(pareto.preferredPath(g, cars[3], weights, 3)), ['c', 'b', 'a']);
  assert.equal(pareto.dominates(cars[1], cars[2], ['x', 'y'], 3), false);
});

test('branching alternatives, skipped layers, score gains and deterministic ties', () => {
  const cars = [car('a', 3, 3), car('b', 2, 1), car('c', 0, 3, 90), car('d', 1, 0), car('e', 0, 0)];
  const weights = { x: 1, y: 1 }, g = pareto.buildGraph(cars, categories, weights, 3);
  assert.deepEqual(ids(pareto.upgrades(g, cars[4], weights, 3)), ['d', 'c']);
  const c = g.byCar.get('c'), e = g.byCar.get('e');
  assert.ok(e.layer - c.layer > 1);
  assert.ok(g.edges.some(edge => edge.better === c.index && edge.worse === e.index));
  const changed = { x: 3, y: 0.5 };
  assert.deepEqual(pairs(pareto.buildGraph(cars, categories, changed, 3)), pairs(g));
  assert.equal(pareto.upgrades(g, cars[4], changed, 3)[0].id, 'c');
  const ties = [car('b', 1, 0, 90), car('a', 0, 1, 90), car('c', 0, 1, 100), car('z', 0, 0)];
  assert.deepEqual(ids(pareto.upgrades(pareto.buildGraph(ties, categories, weights, 3), ties[3], weights, 3)), ['a', 'b', 'c']);
});

test('missing evidence is excluded even though its ranking contribution is zero', () => {
  const cars = [car('known', 0, 0), car('unknown', 1, 0, 50, { x: true, y: false })];
  const weights = { x: 1, y: 1 }, g = pareto.buildGraph(cars, categories, weights, 3);
  assert.deepEqual(ids(g.eligible), ['known']);
  assert.deepEqual(ids(g.incomplete), ['unknown']);
  assert.equal(pareto.dominates(cars[1], cars[0], ['x', 'y'], 3), false);
  assert.deepEqual(pareto.upgrades(g, cars[1], weights, 3), []);
  const off = pareto.buildGraph(cars, categories, { x: 1, y: 0 }, 3);
  assert.equal(off.eligible.length, 2);
  assert.equal(off.layers[0][0].members[0].id, 'unknown');
  const zero = pareto.buildGraph(cars, categories, { x: 0, y: 0 }, 3);
  assert.equal(zero.groups.length, 1); assert.equal(zero.edges.length, 0);
  assert.equal(zero.eligible.length, 2);
  assert.deepEqual(pareto.upgrades(zero, cars[0], { x: 0, y: 0 }, 3), []);
  const none = pareto.buildGraph([cars[1]], categories, weights, 3);
  assert.equal(none.layers.length, 0);
});

test('audited cohort matches both planned default graph baselines', () => {
  for (const [scale, groups, edges, relations, frontier] of [[3, 15, 18, 59, 2], [5, 19, 23, 32, 10]]) {
    const g = pareto.buildGraph(data.cars, data.categories, defaults, scale);
    assert.equal(g.eligible.length, 20); assert.equal(g.incomplete.length, 25);
    assert.equal(g.groups.length, groups); assert.equal(g.edges.length, edges);
    assert.equal(g.dominancePairs, relations);
    assert.equal(g.layers[0].reduce((sum, group) => sum + group.members.length, 0), frontier);
    const off = pareto.buildGraph(data.cars, data.categories, { ...defaults, eco: 0 }, scale);
    assert.equal(off.eligible.length, 45); assert.equal(off.incomplete.length, 0);
  }
});

test('reduced edges preserve every dominance relation and yield the lowest-score dominator', () => {
  for (const scale of [3, 5]) {
    for (let mask = 0; mask < 64; mask++) {
      const weights = Object.fromEntries(data.categories.map((cat, i) => [cat.key, mask & (1 << i) ? (i + 1) / 2 : 0]));
      const g = pareto.buildGraph(data.cars, data.categories, weights, scale);
      for (const target of g.groups) {
        const reachable = new Set();
        function visit(index) {
          for (const edge of g.edges.filter(e => e.worse === index)) {
            if (!reachable.has(edge.better)) { reachable.add(edge.better); visit(edge.better); }
          }
        }
        visit(target.index);
        for (const candidate of g.groups) {
          assert.equal(reachable.has(candidate.index), pareto.dominates(candidate.members[0], target.members[0], g.active, scale));
        }
        const car = target.members[0], next = pareto.upgrades(g, car, weights, scale)[0];
        const all = g.eligible.filter(c => pareto.dominates(c, car, g.active, scale));
        if (!all.length) { assert.equal(next, undefined); continue; }
        assert.equal(pareto.total(next, weights, scale), Math.min(...all.map(c => pareto.total(c, weights, scale))));
      }
    }
  }
});
