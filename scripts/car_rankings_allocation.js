/* Embedded by the page builder; also exercised directly in Node. */
(function (root) {
  'use strict';
  var MAX_UNITS = 200;
  function distribute(keys, total, basis, result) {
    var remaining = keys.slice(), available = total;
    // Cap large shares first; their excess still belongs to the other priorities.
    while (remaining.length) {
      var weight = remaining.reduce(function (n, key) { return n + basis[key]; }, 0);
      var large = remaining.filter(function (key) { return available * basis[key] / weight > MAX_UNITS; });
      if (!large.length) break;
      large.forEach(function (key) { result[key] = MAX_UNITS; available -= MAX_UNITS; });
      remaining = remaining.filter(function (key) { return large.indexOf(key) < 0; });
    }
    // Keep a minimum share, so redistribution never silently turns a priority off.
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
    var budget = (others.length + (requested > 0 ? 1 : 0)) * 100;
    result[key] = requested <= 0 ? 0 : others.length ? Math.max(1, Math.min(MAX_UNITS, budget - others.length, Math.round(requested))) : budget;
    if (others.length) distribute(others, budget - result[key], basis || state, result);
    return result;
  }
  function total(car, weights) {
    return Object.keys(weights).reduce(function (sum, key) {
      return sum + car.scores[key] * Math.round(weights[key] * 100);
    }, 0) / 100;
  }
  function number(value) { return String(Math.round(value * 100) / 100); }
  var api = { set: set, total: total, number: number, MAX_UNITS: MAX_UNITS };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.CarAllocation = api;
})(typeof window !== 'undefined' ? window : globalThis);
