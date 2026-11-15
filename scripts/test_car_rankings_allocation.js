const { test } = require('node:test');
const assert = require('node:assert/strict');
const allocation = require('./car_rankings_allocation.js');
const defaults = { cost: 100, eco: 100, mountain: 100, lux: 100, commute: 100, maintenance: 0 };
const sum = state => Object.values(state).reduce((a, b) => a + b, 0);

test('dragging redistributes proportionally, keeps off categories off, and preserves the source state', () => {
  assert.deepEqual(allocation.set(defaults, 'cost', 200), { ...defaults, cost: 200, eco: 75, mountain: 75, lux: 75, commute: 75 });
  assert.deepEqual(defaults, { cost: 100, eco: 100, mountain: 100, lux: 100, commute: 100, maintenance: 0 });
  assert.deepEqual(allocation.set({ a: 100, b: 100, c: 300, d: 0 }, 'a', 300), { a: 300, b: 50, c: 150, d: 0 });
});

test('zero disables every category and positive input recovers from all-off and sole-category states', () => {
  for (const key of Object.keys(defaults)) {
    let state = allocation.set(defaults, key, defaults[key] ? 0 : 83);
    assert.equal(sum(state), 500);
    assert.equal(state[key], defaults[key] ? 0 : 83);
  }
  assert.deepEqual(allocation.set(defaults, 'cost', 0), { ...defaults, cost: 0, eco: 125, mountain: 125, lux: 125, commute: 125 });
  let state = defaults;
  for (const key of Object.keys(state)) state = allocation.set(state, key, 0);
  assert.equal(sum(state), 0);
  state = allocation.set(state, 'maintenance', state.maintenance ? 0 : 100);
  assert.equal(state.maintenance, 500);
  assert.equal(allocation.set(state, 'maintenance', 12).maintenance, 500);
  assert.equal(sum(allocation.set(state, 'maintenance', state.maintenance ? 0 : 100)), 0);
});

test('extremes and rounding preserve active categories and deterministic exact budgets', () => {
  assert.deepEqual(allocation.set(defaults, 'cost', 500), { ...defaults, cost: 496, eco: 1, mountain: 1, lux: 1, commute: 1 });
  assert.deepEqual(allocation.set({ a: 100, b: 100, c: 100, d: 200 }, 'd', 100), { a: 134, b: 133, c: 133, d: 100 });
  assert.deepEqual(allocation.set({ a: 1, b: 1, c: 498 }, 'a', 498), { a: 498, b: 1, c: 1 });
  let state = defaults;
  let seed = 13;
  for (let i = 0; i < 3000; i++) {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    const key = Object.keys(state)[seed % 6];
    const before = state;
    state = i % 7 ? allocation.set(state, key, seed % 501) : allocation.set(state, key, state[key] ? 0 : 100);
    assert.ok(sum(state) === 500 || sum(state) === 0);
    for (const k of Object.keys(state)) {
      assert.ok(Number.isInteger(state[k]) && state[k] >= 0 && state[k] <= 500);
      if (k !== key) assert.equal(state[k] > 0, before[k] > 0);
    }
  }
});

test('gesture basis prevents proportional rounding drift and scores use integer arithmetic', () => {
  const basis = { a: 100, b: 133, c: 267 };
  let state = basis;
  for (let i = 101; i <= 450; i++) state = allocation.set(state, 'a', i, basis);
  assert.deepEqual(state, allocation.set(basis, 'a', 450));
  assert.equal(allocation.total({ scores: { a: 1, b: 1, c: -1 } }, { a: .1, b: .2, c: .3 }), 0);
});
