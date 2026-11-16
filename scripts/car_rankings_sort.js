/* Shared ordering for the offline ranking. Scores always remain unweighted cells. */
(function (root) {
  'use strict';
  function nameOrder(a, b) {
    var left = a.name.toLowerCase(), right = b.name.toLowerCase();
    return left < right ? -1 : left > right ? 1 : 0;
  }
  function totalOrder(a, b) { return b.total - a.total || a.five - b.five || nameOrder(a, b); }
  function next(state, key) {
    return { key: key, direction: state.key === key ? (state.direction === 'asc' ? 'desc' : 'asc') : (key === 'name' || key === 'rank' ? 'asc' : 'desc') };
  }
  function order(cars, state) {
    return cars.slice().sort(function (a, b) {
      var difference = state.key === 'name' ? nameOrder(a, b) :
        state.key === 'rank' ? a.rank - b.rank :
        state.key === 'total' ? a.total - b.total : a.scores[state.key] - b.scores[state.key];
      return (state.direction === 'asc' ? difference : -difference) || totalOrder(a, b);
    });
  }
  var api = { next: next, order: order, totalOrder: totalOrder };
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.CarSort = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
