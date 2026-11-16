'use strict';
const assert = require('node:assert/strict');
const Sort = require('./car_rankings_sort.js');
const keys = ['cost', 'eco', 'mountain', 'lux', 'commute', 'maintenance'];
const cars = [
  { id: 'a', name: 'Alpha', rank: 2, total: 1.25, five: 40000, scores: Object.fromEntries(keys.map(k => [k, -2])) },
  { id: 'b', name: 'bravo', rank: 1, total: 2.5, five: 42000, scores: Object.fromEntries(keys.map(k => [k, 1])) },
  { id: 'c', name: 'Charlie', rank: 3, total: 1.25, five: 41000, scores: Object.fromEntries(keys.map(k => [k, 1])) }
];
const ids = rows => rows.map(c => c.id);
for (const key of keys) {
  assert.deepEqual(ids(Sort.order(cars, { key, direction: 'desc' })), ['b', 'c', 'a']);
  assert.deepEqual(ids(Sort.order(cars, { key, direction: 'asc' })), ['a', 'b', 'c']);
}
assert.deepEqual(ids(Sort.order(cars, { key: 'name', direction: 'asc' })), ['a', 'b', 'c']);
assert.deepEqual(ids(Sort.order(cars, { key: 'name', direction: 'desc' })), ['c', 'b', 'a']);
assert.deepEqual(ids(Sort.order(cars, { key: 'rank', direction: 'asc' })), ['b', 'a', 'c']);
assert.deepEqual(ids(Sort.order(cars, { key: 'rank', direction: 'desc' })), ['c', 'a', 'b']);
assert.deepEqual(ids(Sort.order(cars, { key: 'total', direction: 'desc' })), ['b', 'a', 'c']);
assert.deepEqual(ids(Sort.order(cars, { key: 'total', direction: 'asc' })), ['a', 'c', 'b']);
assert.deepEqual(ids(cars), ['a', 'b', 'c']);
for (const key of ['rank', 'name', 'total', ...keys]) {
  const first = Sort.next({ key: 'other', direction: 'asc' }, key);
  assert.equal(first.direction, key === 'rank' || key === 'name' ? 'asc' : 'desc');
  assert.notEqual(Sort.next(first, key).direction, first.direction);
}
const equal = cars.map(c => ({ ...c, total: 0, five: 40000, scores: Object.fromEntries(keys.map(k => [k, 0])) }));
assert.deepEqual(ids(Sort.order(equal, { key: 'eco', direction: 'desc' })), ['a', 'b', 'c']);
console.log('Sorting passed: all nine columns, both directions, ties, defaults, immutable inputs.');
