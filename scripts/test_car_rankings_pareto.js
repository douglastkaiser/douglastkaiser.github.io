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
function car(id, x, y, five = 100) {
  return { id, name: id, five, scores: { x, y } };
}
function ids(cars) { return cars.map(car => car.id); }
function pairs(graph) { return graph.edges.map(e => [graph.groups[e.better].members[0].id, graph.groups[e.worse].members[0].id].join('>')).sort(); }

test('chains reduce transitively and equal profiles never dominate each other', () => {
  const cars = [car('a', 2, 2), car('b', 1, 1), car('b2', 1, 1), car('c', 0, 0)];
  const weights = { x: 1, y: 1 }, g = pareto.buildGraph(cars, categories, weights);
  assert.equal(g.groups.length, 3);
  assert.deepEqual(pairs(g), ['a>b', 'b>c']);
  assert.deepEqual(g.layers.map(layer => layer.length), [1, 1, 1]);
  assert.deepEqual(ids(pareto.preferredPath(g, cars[3], weights)), ['c', 'b', 'a']);
  assert.equal(pareto.dominates(cars[1], cars[2], ['x', 'y']), false);
});

test('branching alternatives, skipped layers, score gains and deterministic ties', () => {
  const cars = [car('a', 2, 2), car('b', 1, 0), car('c', -1, 2, 90), car('d', 0, -1), car('e', -1, -1)];
  const weights = { x: 1, y: 1 }, g = pareto.buildGraph(cars, categories, weights);
  assert.deepEqual(ids(pareto.upgrades(g, cars[4], weights)), ['d', 'c']);
  const c = g.byCar.get('c'), e = g.byCar.get('e');
  assert.ok(e.layer - c.layer > 1);
  assert.ok(g.edges.some(edge => edge.better === c.index && edge.worse === e.index));
  const changed = { x: 3, y: 0.5 };
  assert.deepEqual(pairs(pareto.buildGraph(cars, categories, changed)), pairs(g));
  assert.equal(pareto.upgrades(g, cars[4], changed)[0].id, 'c');
  const ties = [car('b', 1, 0, 90), car('a', 0, 1, 90), car('c', 0, 1, 100), car('z', 0, 0)];
  assert.deepEqual(ids(pareto.upgrades(pareto.buildGraph(ties, categories, weights), ties[3], weights)), ['a', 'b', 'c']);
});

test('all cars participate with proxy scores, including when metrics are off', () => {
  for (let mask = 0; mask < 64; mask++) {
    const weights = Object.fromEntries(data.categories.map((cat, i) => [cat.key, mask & (1 << i) ? 1 : 0]));
    const g = pareto.buildGraph(data.cars, data.categories, weights);
    assert.equal(g.eligible.length, data.cars.length);
    assert.equal(g.byCar.size, data.cars.length);
    assert.equal(g.groups.reduce((sum, group) => sum + group.members.length, 0), data.cars.length);
    if (!mask) {
      assert.equal(g.groups.length, 1);
      assert.equal(g.edges.length, 0);
      assert.deepEqual(pareto.upgrades(g, data.cars[0], weights), []);
    }
  }
});

test('five-level totals and dominance use the canonical scores', () => {
  const a = car('a', 2, -1), b = car('b', 1, -2);
  const weights = { x: .5, y: 2 };
  assert.equal(pareto.total(a, weights), -1);
  assert.equal(pareto.total(b, weights), -3.5);
  assert.equal(pareto.dominates(a, b, ['x', 'y']), true);
  assert.deepEqual(pairs(pareto.buildGraph([a, b], categories, weights)), ['a>b']);
  for (const c of data.cars) {
    assert.equal(pareto.total(c, defaults), data.categories.reduce((sum, cat) => sum + c.scores[cat.key] * cat.default, 0));
    assert.ok(!('scores5' in c));
  }
});

test('reduced edges preserve every dominance relation and yield the lowest-score dominator', () => {
  for (let mask = 0; mask < 64; mask++) {
    const weights = Object.fromEntries(data.categories.map((cat, i) => [cat.key, mask & (1 << i) ? (i + 1) / 2 : 0]));
    const g = pareto.buildGraph(data.cars, data.categories, weights);
    for (const target of g.groups) {
      const reachable = new Set();
      function visit(index) {
        for (const edge of g.edges.filter(e => e.worse === index)) {
          if (!reachable.has(edge.better)) { reachable.add(edge.better); visit(edge.better); }
        }
      }
      visit(target.index);
      for (const candidate of g.groups) {
        assert.equal(reachable.has(candidate.index), pareto.dominates(candidate.members[0], target.members[0], g.active));
      }
      const car = target.members[0], next = pareto.upgrades(g, car, weights)[0];
      const all = g.eligible.filter(c => pareto.dominates(c, car, g.active));
      if (!all.length) { assert.equal(next, undefined); continue; }
      assert.equal(pareto.total(next, weights), Math.min(...all.map(c => pareto.total(c, weights))));
    }
  }
});
