/* Embedded by the page builder; also exercised directly in Node. */
(function (root) {
  'use strict';
  var BUDGET = 500;
  function distribute(keys, total, basis, result) {
    var remaining = keys.slice(), available = total;
    // Water-fill small shares first, so redistribution never silently turns one off.
    while (remaining.length) {
      var sum = remaining.reduce(function (n, key) { return n + basis[key]; }, 0);
      var small = remaining.filter(function (key) { return available * basis[key] / sum < 1; });
      if (!small.length) break;
      small.forEach(function (key) { result[key] = 1; available--; });
      remaining = remaining.filter(function (key) { return small.indexOf(key) < 0; });
    }
    if (!remaining.length) return;
    var denominator = remaining.reduce(function (n, key) { return n + basis[key]; }, 0);
    var shares = remaining.map(function (key, index) {
      var exact = available * basis[key] / denominator;
      result[key] = Math.floor(exact);
      return { key: key, remainder: exact - result[key], index: index };
    });
    var spare = available - remaining.reduce(function (n, key) { return n + result[key]; }, 0);
    shares.sort(function (a, b) { return b.remainder - a.remainder || a.index - b.index; });
    shares.slice(0, spare).forEach(function (share) { result[share.key]++; });
  }
  function set(state, key, requested, basis) {
    var result = Object.assign({}, state);
    var others = Object.keys(state).filter(function (k) { return k !== key && state[k] > 0; });
    result[key] = requested <= 0 ? 0 : others.length ? Math.max(1, Math.min(BUDGET - others.length, Math.round(requested))) : BUDGET;
    if (others.length) distribute(others, BUDGET - result[key], basis || state, result);
    return result;
  }
  function total(car, weights) {
    return Object.keys(weights).reduce(function (sum, key) {
      return sum + car.scores[key] * Math.round(weights[key] * 100);
    }, 0) / 100;
  }
  function number(value) { return String(Math.round(value * 100) / 100); }
  var api = { set: set, total: total, number: number };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.CarAllocation = api;
})(typeof window !== 'undefined' ? window : globalThis);
