const { test } = require('node:test');
const assert = require('node:assert/strict');
const allocation = require('./car_rankings_allocation.js');
const defaults = { cost: 100, eco: 100, mountain: 100, lux: 100, commute: 100, sporty: 0 };
const sum = state => Object.values(state).reduce((a, b) => a + b, 0);

test('dragging redistributes proportionally, keeps off categories off, and preserves the source state', () => {
  assert.deepEqual(allocation.set(defaults, 'cost', 200), { ...defaults, cost: 200, eco: 75, mountain: 75, lux: 75, commute: 75 });
  assert.deepEqual(defaults, { cost: 100, eco: 100, mountain: 100, lux: 100, commute: 100, sporty: 0 });
  assert.deepEqual(allocation.set({ a: 100, b: 50, c: 150, d: 0 }, 'a', 200), { a: 200, b: 25, c: 75, d: 0 });
});

test('zero disables every category and positive input recovers from all-off and sole-category states', () => {
  for (const key of Object.keys(defaults)) {
    let state = allocation.set(defaults, key, defaults[key] ? 0 : 100);
    assert.equal(sum(state), defaults[key] ? 400 : 600);
    assert.equal(state[key], defaults[key] ? 0 : 100);
  }
  const allOn = allocation.set(defaults, 'sporty', 100);
  assert.deepEqual(allOn, { ...defaults, sporty: 100 });
  assert.deepEqual(allocation.set(allOn, 'sporty', 0), defaults);
  assert.deepEqual(allocation.set({ a: 200, b: 50, c: 50 }, 'a', 0), { a: 0, b: 100, c: 100 });
  assert.deepEqual(allocation.set(defaults, 'cost', 0), { ...defaults, cost: 0 });
  let state = defaults;
  for (const key of Object.keys(state)) state = allocation.set(state, key, 0);
  assert.equal(sum(state), 0);
  state = allocation.set(state, 'sporty', state.sporty ? 0 : 100);
  assert.equal(state.sporty, 100);
  assert.equal(allocation.set(state, 'sporty', 12).sporty, 100);
  assert.equal(sum(allocation.set(state, 'sporty', state.sporty ? 0 : 100)), 0);
});

test('extremes and rounding preserve active categories and deterministic exact budgets', () => {
  assert.deepEqual(allocation.set(defaults, 'cost', 500), { ...defaults, cost: 200, eco: 75, mountain: 75, lux: 75, commute: 75 });
  assert.deepEqual(allocation.set({ a: 100, b: 100, c: 100, d: 100 }, 'd', 100), { a: 100, b: 100, c: 100, d: 100 });
  assert.deepEqual(allocation.set({ a: 1, b: 99, c: 200 }, 'a', 498), { a: 200, b: 33, c: 67 });
  assert.deepEqual(allocation.set({ a: 100, b: 100 }, 'a', 500), { a: 199, b: 1 });
  let state = defaults;
  let seed = 13;
  for (let i = 0; i < 3000; i++) {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    const key = Object.keys(state)[seed % 6];
    const before = state;
    state = i % 7 ? allocation.set(state, key, seed % 501) : allocation.set(state, key, state[key] ? 0 : 100);
    assert.equal(sum(state), Object.values(state).filter(value => value > 0).length * 100);
    for (const k of Object.keys(state)) {
      assert.ok(Number.isInteger(state[k]) && state[k] >= 0 && state[k] <= 200);
      if (k !== key) assert.equal(state[k] > 0, before[k] > 0);
    }
  }
});

test('linked redistribution caps other priorities and reallocates their excess', () => {
  const state = { a: 200, b: 150, c: 25, d: 25 };
  assert.deepEqual(allocation.set(state, 'a', 0), { a: 0, b: 200, c: 50, d: 50 });
  assert.deepEqual(allocation.set(state, 'a', 1), { a: 1, b: 200, c: 100, d: 99 });
  assert.deepEqual(allocation.set({ a: 200, b: 198, c: 199, d: 1, e: 1, f: 1 }, 'a', 1),
    { a: 1, b: 200, c: 200, d: 67, e: 66, f: 66 });
});

test('gesture basis prevents proportional rounding drift and scores use integer arithmetic', () => {
  const basis = { a: 100, b: 67, c: 133 };
  let state = basis;
  for (let i = 101; i <= 450; i++) state = allocation.set(state, 'a', i, basis);
  assert.deepEqual(state, allocation.set(basis, 'a', 450));
  assert.equal(allocation.total({ scores: { a: 1, b: 1, c: -1 } }, { a: .1, b: .2, c: .3 }), 0);
});
