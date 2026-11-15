/* Embedded by build_car_rankings.py; no runtime requests or dependencies. */
(function (root) {
  'use strict';

  function nameOrder(a, b) {
    var left = a.name.toLowerCase(), right = b.name.toLowerCase();
    return left < right ? -1 : left > right ? 1 : 0;
  }
  function scores(car, scale) { return scale === 5 ? car.scores5 : car.scores; }
  function total(car, weights, scale) {
    return Object.keys(weights).reduce(function (sum, key) { return sum + scores(car, scale)[key] * weights[key]; }, 0);
  }
  function ascending(weights, scale) {
    return function (a, b) { return total(a, weights, scale) - total(b, weights, scale) || a.five - b.five || nameOrder(a, b); };
  }
  function dominates(a, b, active, scale) {
    // Coverage is a prerequisite, not an imputed middle-tier score.
    return active.every(function (key) { return a.assessed[key] && b.assessed[key] && scores(a, scale)[key] >= scores(b, scale)[key]; }) &&
      active.some(function (key) { return scores(a, scale)[key] > scores(b, scale)[key]; });
  }
  function buildGraph(cars, categories, weights, scale) {
    var active = categories.map(function (cat) { return cat.key; }).filter(function (key) { return weights[key] > 0; });
    var eligible = [], incomplete = [], profiles = new Map(), byCar = new Map();
    cars.forEach(function (car) {
      if (!active.every(function (key) { return car.assessed[key]; })) { incomplete.push(car); return; }
      eligible.push(car);
      var signature = JSON.stringify(active.map(function (key) { return scores(car, scale)[key]; }));
      if (!profiles.has(signature)) profiles.set(signature, { members: [] });
      profiles.get(signature).members.push(car);
    });
    var groups = Array.from(profiles.values());
    groups.forEach(function (group) { group.members.sort(nameOrder); });
    groups.sort(function (a, b) { return nameOrder(a.members[0], b.members[0]); });
    groups.forEach(function (group, i) {
      group.index = i;
      group.members.forEach(function (car) { byCar.set(car.id, group); });
    });
    var matrix = groups.map(function (a) {
      return groups.map(function (b) { return dominates(a.members[0], b.members[0], active, scale); });
    });
    var edges = [], dominancePairs = 0;
    groups.forEach(function (a, i) {
      groups.forEach(function (b, j) {
        if (!matrix[i][j]) return;
        dominancePairs += a.members.length * b.members.length;
        if (!groups.some(function (_, k) { return matrix[i][k] && matrix[k][j]; })) edges.push({ better: i, worse: j });
      });
    });
    var remaining = groups.slice(), layers = [];
    while (remaining.length) {
      var layer = remaining.filter(function (b) { return !remaining.some(function (a) { return matrix[a.index][b.index]; }); });
      layer.forEach(function (group) { group.layer = layers.length; });
      layers.push(layer);
      remaining = remaining.filter(function (group) { return layer.indexOf(group) < 0; });
    }
    incomplete.sort(nameOrder);
    return { active: active, eligible: eligible, incomplete: incomplete, groups: groups, byCar: byCar,
      edges: edges, layers: layers, dominancePairs: dominancePairs };
  }
  function upgrades(graph, car, weights, scale) {
    var group = graph.byCar.get(car.id);
    if (!group) return [];
    var result = [];
    graph.edges.forEach(function (edge) {
      if (edge.worse === group.index) result = result.concat(graph.groups[edge.better].members);
    });
    return result.sort(ascending(weights, scale));
  }
  function preferredPath(graph, car, weights, scale) {
    var result = [], next = car;
    while (next && graph.byCar.has(next.id)) {
      result.push(next);
      next = upgrades(graph, next, weights, scale)[0];
    }
    return result;
  }

  function createView(options) {
    var data = options.data, cars = data.cars, categories = data.categories;
    var byId = new Map(cars.map(function (car) { return [car.id, car]; }));
    var cache = new Map(), graph = null, renderedGraph = null, currentWeights = {};
    var state = { active: false, scale: 3, presentation: 'network', selected: null, comparison: null };
    var frame = null, revealSelection = false;
    function el(id) { return document.getElementById(id); }
    function signed(n) { return n > 0 ? '+' + n : n < 0 ? '−' + Math.abs(n) : '0'; }
    function money(n) { return '$' + (n / 1000).toFixed(1) + 'k'; }
    function escape(text) {
      return String(text).replace(/[&<>"']/g, function (ch) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]; });
    }
    function button(car, label) {
      return '<button type="button" class="pareto-button" data-select="' + escape(car.id) + '" aria-pressed="' + (state.selected === car.id) + '">' + escape(label || car.name) + '</button>';
    }
    function scoreText(car, key) { return car.assessed[key] ? signed(scores(car, state.scale)[key]) : '—'; }
    function readLocation() {
      var params = new URLSearchParams(location.search);
      state.active = params.get('view') === 'pareto';
      if (params.has('scale') || state.active) state.scale = params.get('scale') === '5' ? 5 : 3;
      // A dialog's close anchor also remains a usable same-document link.
      if (location.hash === '#pareto') state.active = true;
      else if (location.hash === '#ranking') state.active = false;
    }
    function saveLocation() {
      var url = new URL(location.href);
      if (state.active) { url.searchParams.set('view', 'pareto'); url.searchParams.set('scale', state.scale); }
      else { url.searchParams.delete('view'); url.searchParams.delete('scale'); }
      if (url.hash === '#ranking' || url.hash === '#pareto') url.hash = state.active ? 'pareto' : 'ranking';
      // Some local-file hosts disallow history writes; controls still work there.
      try { history.replaceState(null, '', url); } catch (_) { /* Retain in-memory state. */ }
    }
    function choose(id) {
      var focused = document.activeElement;
      state.selected = id; state.comparison = null;
      revealSelection = true;
      options.redraw();
      if (focused && !focused.isConnected) el('pareto-car').focus();
    }
    function memberButtons(group) {
      return group.members.map(function (car) { return button(car); }).join('');
    }
    function groupNode(group) {
      var car = group.members.find(function (c) { return c.id === state.selected; }) || group.members[0];
      return '<section class="pareto-node" data-node="' + group.index + '" aria-label="Score profile, ' + group.members.length + ' vehicle(s)">' +
        '<span class="node-score" data-group-total="' + group.index + '"></span>' +
        '<button type="button" data-primary="' + group.index + '" data-select="' + escape(car.id) + '">' + escape(car.name) + '</button>' +
        (group.members.length > 1 ? '<details><summary>' + group.members.length + ' equivalent cars</summary>' + memberButtons(group) + '</details>' : '') + '</section>';
    }
    function renderStructure() {
      var stage = el('pareto-stage');
      stage.innerHTML = '<svg class="pareto-links" id="pareto-links" role="img" aria-label="Direct upgrade connections; arrows point toward better score profiles"></svg>' + graph.layers.map(function (layer, i) {
        return '<section class="pareto-layer"><h3>' + (graph.active.length ? i === 0 ? 'Frontier' : 'Layer ' + (i + 1) : 'All scores equivalent') + '</h3>' + layer.map(groupNode).join('') + '</section>';
      }).join('');
      el('pareto-list').innerHTML = graph.layers.map(function (layer, i) {
        return '<section class="pareto-layer-list"><h3>' + (graph.active.length ? i === 0 ? 'Frontier' : 'Layer ' + (i + 1) : 'All scores equivalent') + '</h3>' + layer.map(function (group) {
          var better = graph.edges.filter(function (edge) { return edge.worse === group.index; });
          return '<div class="pareto-list-group" data-list-node="' + group.index + '"><div>' + memberButtons(group) +
            '<strong data-group-total="' + group.index + '"></strong></div><small>' + (group.members.length > 1 ? 'Equivalent active scores. ' : '') +
            (better.length ? 'Direct upgrades:' : graph.active.length ? 'No dominating alternative.' : 'No active metrics.') + '</small>' +
            (better.length ? '<div>' + better.map(function (edge) { return button(graph.groups[edge.better].members[0]); }).join('') + '</div>' : '') + '</div>';
        }).join('') + '</section>';
      }).join('');
      el('pareto-incomplete-cars').innerHTML = graph.incomplete.map(function (car) {
        var missing = categories.filter(function (cat) { return currentWeights[cat.key] > 0 && !car.assessed[cat.key]; }).map(function (cat) { return cat.label; });
        return '<button type="button" class="pareto-button" data-select="' + escape(car.id) + '">' + escape(car.name) + '<small>Missing: ' + escape(missing.join(', ')) + '</small></button>';
      }).join('');
      renderedGraph = graph;
      revealSelection = true;
    }
    function highlight() {
      var selected = byId.get(state.selected), group = graph.byCar.get(state.selected);
      var path = preferredPath(graph, selected, currentWeights, state.scale);
      var pathGroups = path.map(function (car) { return graph.byCar.get(car.id).index; });
      var direct = group ? graph.edges.filter(function (edge) { return edge.worse === group.index; }).map(function (edge) { return edge.better; }) : [];
      graph.groups.forEach(function (g) {
        var node = el('pareto-stage').querySelector('[data-node="' + g.index + '"]');
        node.classList.toggle('is-selected', g === group);
        node.classList.toggle('is-direct', direct.indexOf(g.index) >= 0);
        node.classList.toggle('is-path', pathGroups.indexOf(g.index) >= 0 && g !== group);
        el('pareto-list').querySelector('[data-list-node="' + g.index + '"]').classList.toggle('is-selected', g === group);
        var primary = node.querySelector('[data-primary]'), car = g === group ? selected : g.members[0];
        primary.dataset.select = car.id; primary.textContent = car.name;
      });
      el('pareto').querySelectorAll('[data-select]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.select === state.selected)); });
      el('pareto').querySelectorAll('[data-group-total]').forEach(function (target) {
        target.textContent = signed(total(graph.groups[Number(target.dataset.groupTotal)].members[0], currentWeights, state.scale));
      });
      el('pareto-links').querySelectorAll('[data-better]').forEach(function (line) {
        var better = Number(line.dataset.better), worse = Number(line.dataset.worse);
        var isDirect = group && worse === group.index;
        var isPath = pathGroups.some(function (g, i) { return g === worse && pathGroups[i + 1] === better; });
        line.setAttribute('class', 'pareto-edge' + (isDirect ? ' is-direct' : '') + (isPath ? ' is-path' : ''));
        line.setAttribute('marker-end', 'url(#pareto-arrow-' + (isPath ? 'path' : isDirect ? 'direct' : 'muted') + ')');
      });
    }
    function drawEdges() {
      frame = null;
      if (!state.active || state.presentation !== 'network' || !graph) return;
      var stage = el('pareto-stage'), svg = el('pareto-links'), scroller = el('pareto-network');
      var width = Math.max(136, Math.min(190, (scroller.clientWidth - 36 - 32 * (graph.layers.length - 1)) / Math.max(1, graph.layers.length)));
      stage.style.setProperty('--pareto-node-width', width + 'px');
      var rect = stage.getBoundingClientRect();
      // Measure the layout box: scrollWidth/Height include the previous absolute SVG
      // and can otherwise leave a blank scrollable tail after a viewport shrinks.
      svg.setAttribute('width', rect.width); svg.setAttribute('height', rect.height);
      svg.innerHTML = '<defs>' + [['muted', '#bbcbbf'], ['direct', '#5a9270'], ['path', '#11764b']].map(function (entry) {
        return '<marker id="pareto-arrow-' + entry[0] + '" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="' + entry[1] + '"/></marker>';
      }).join('') + '</defs>' + graph.edges.map(function (edge) {
        var better = stage.querySelector('[data-node="' + edge.better + '"]').getBoundingClientRect();
        var worse = stage.querySelector('[data-node="' + edge.worse + '"]').getBoundingClientRect();
        var x1 = worse.left - rect.left, y1 = worse.top + worse.height / 2 - rect.top;
        var x2 = better.right - rect.left, y2 = better.top + better.height / 2 - rect.top;
        var bend = Math.max(28, Math.min(70, (x1 - x2) / 2));
        return '<path class="pareto-edge" data-better="' + edge.better + '" data-worse="' + edge.worse + '" d="M' + x1 + ',' + y1 + ' C' + (x1 - bend) + ',' + y1 + ' ' + (x2 + bend) + ',' + y2 + ' ' + x2 + ',' + y2 + '"/>';
      }).join('');
      highlight();
      if (revealSelection) {
        var selected = stage.querySelector('.is-selected');
        if (selected) {
          var selectedRect = selected.getBoundingClientRect(), scrollRect = scroller.getBoundingClientRect();
          if (selectedRect.left < scrollRect.left || selectedRect.right > scrollRect.right) {
            scroller.scrollLeft += selectedRect.left - scrollRect.left - (scroller.clientWidth - selectedRect.width) / 2;
          }
          if (selectedRect.top < scrollRect.top || selectedRect.bottom > scrollRect.bottom) {
            scroller.scrollTop += selectedRect.top - scrollRect.top - (scroller.clientHeight - selectedRect.height) / 2;
          }
        }
        revealSelection = false;
      }
    }
    function scheduleEdges() {
      if (frame !== null) cancelAnimationFrame(frame);
      frame = requestAnimationFrame(drawEdges);
    }
    function comparison() {
      var car = byId.get(state.selected), alternatives = upgrades(graph, car, currentWeights, state.scale);
      var next = alternatives[0], compared = alternatives.find(function (c) { return c.id === state.comparison; }) || next;
      var group = graph.byCar.get(car.id), scaleLabel = state.scale + ' levels' + (state.scale === 5 ? ' · experimental' : '');
      var html = '<div class="selected-summary"><div><h3>' + escape(car.name) + '</h3><p>' + escape(scaleLabel) + ' · Est. five-year cost ' + money(car.five) + '</p></div><strong class="selected-total">' + signed(total(car, currentWeights, state.scale)) + '</strong></div>' +
        '<div class="comparison-actions"><a href="#detail-' + escape(car.id) + '">Research and cost breakdown ↗</a></div>';
      if (!group) {
        var missing = categories.filter(function (cat) { return currentWeights[cat.key] > 0 && !car.assessed[cat.key]; }).map(function (cat) { return cat.label; });
        html += '<p class="notice">Missing active-metric evidence: ' + escape(missing.join(', ')) + '. No dominance or frontier classification is assigned.</p>';
        el('pareto-incomplete').open = true;
      } else if (!graph.active.length) html += '<p>No active metrics. All cars have equal active scores; cost only determines display order.</p>';
      else if (!next) html += '<p>No dominating alternative. This car is on the frontier for the selected scores.</p>';
      else {
        var gain = total(next, currentWeights, state.scale) - total(car, currentWeights, state.scale);
        var tied = alternatives.filter(function (c) { return total(c, currentWeights, state.scale) === total(next, currentWeights, state.scale); }).length;
        html += '<div class="next-upgrade"><small>Next dominator · smallest weighted-score gain</small><h4>' + escape(next.name) + ' · ' + signed(gain) + '</h4><p>Est. five-year cost ' + money(next.five) + '</p><div class="comparison-actions">' + button(next, 'Follow upgrade') + '<a href="#detail-' + escape(next.id) + '">Upgrade evidence ↗</a></div></div>' +
          (tied > 1 ? '<p class="pareto-intro">' + tied + ' alternatives share the smallest gain. Lower five-year cost, then name breaks the tie; it is not a performance difference.</p>' : '') +
          '<label class="alternative-label" for="pareto-alternative">Compare a direct upgrade (' + alternatives.length + ')<select id="pareto-alternative">' + alternatives.map(function (alt) {
            return '<option value="' + escape(alt.id) + '"' + (alt === compared ? ' selected' : '') + '>' + escape(alt.name) + ' · ' + signed(total(alt, currentWeights, state.scale)) + '</option>';
          }).join('') + '</select></label>';
      }
      html += '<table class="metric-comparison"><caption class="pareto-intro">Active tier comparison' + (compared ? ' · upgrade: ' + escape(compared.name) : '') + '</caption><thead><tr><th scope="col">Metric</th><th scope="col">Selected</th><th scope="col">Upgrade</th><th scope="col">Change</th></tr></thead><tbody>' + categories.map(function (cat) {
        var key = cat.key, active = currentWeights[key] > 0;
        var comparable = compared && car.assessed[key] && compared.assessed[key];
        var delta = comparable ? scores(compared, state.scale)[key] - scores(car, state.scale)[key] : null;
        return '<tr data-metric="' + key + '"' + (!active ? ' class="ignored"' : '') + '><th scope="row">' + escape(cat.label) + '<small>' + currentWeights[key] + '×' + (!active ? ' · ignored' : '') + '</small></th><td>' + scoreText(car, key) + '</td><td>' + (compared ? scoreText(compared, key) : '—') + '</td><td' + (active && delta > 0 ? ' class="improvement"' : '') + '>' + (!active ? 'Ignored' : delta === null ? '—' : delta === 0 ? 'Equal' : signed(delta) + '<small> (' + signed(delta * currentWeights[key]) + ' weighted)</small>') + '</td></tr>';
      }).join('') + '</tbody></table>';
      el('pareto-comparison').innerHTML = html;
      var announcement = car.name + ', ' + scaleLabel + ', score ' + signed(total(car, currentWeights, state.scale)) + '. ' +
        (!group ? 'Missing active-metric evidence.' : !graph.active.length ? 'No active metrics.' : next ? 'Next dominator: ' + next.name + '.' : 'No dominating alternative.');
      if (el('pareto-selection-status').textContent !== announcement) el('pareto-selection-status').textContent = announcement;
    }
    // Save audited three-level wording once; experimental labels never overwrite it.
    var detailCells = [];
    cars.forEach(function (car) {
      var modal = el('detail-' + car.id);
      categories.forEach(function (cat) {
        var section = modal.querySelector('[data-assessment="' + cat.key + '"]');
        detailCells.push({ car: car, key: cat.key, pill: section.querySelector('.pill'), note: section.querySelector('.tiernote'), original: section.querySelector('.tiernote').textContent });
      });
    });
    function syncDetails() {
      var scale = state.active ? state.scale : 3;
      cars.forEach(function (car) {
        var target = document.querySelector('[data-total="' + car.id + '"]');
        target.textContent = signed(total(car, currentWeights, scale));
        target.previousElementSibling.textContent = scale === 5 ? 'Weighted score (5 levels)' : 'Weighted score';
      });
      detailCells.forEach(function (cell) {
        var missing = !cell.car.assessed[cell.key], value = scores(cell.car, scale)[cell.key];
        cell.pill.textContent = missing ? '—' : signed(value);
        cell.pill.className = 'pill ' + (missing ? 'unscored' : value > 0 ? 'positive' : value < 0 ? 'negative' : 'neutral');
        cell.note.textContent = scale === 5 && !missing ? '5 levels · ' + ({ 2: 'Highest band', 1: 'Upper band', 0: 'Middle band', '-1': 'Lower band', '-2': 'Lowest band' }[value]) + cell.original.slice(cell.original.indexOf(' · ')) : cell.original;
      });
      document.querySelectorAll('.modal .scrim,.modal .close').forEach(function (anchor) { anchor.setAttribute('href', state.active ? '#pareto' : '#ranking'); });
    }
    function update(weights) {
      currentWeights = weights;
      el('rankings-view').hidden = state.active;
      el('pareto').hidden = !state.active;
      ['rankings', 'pareto'].forEach(function (view) {
        var selected = view === 'pareto' ? state.active : !state.active, tab = el('tab-' + view);
        tab.setAttribute('aria-selected', String(selected)); tab.tabIndex = selected ? 0 : -1;
      });
      syncDetails();
      if (!state.active) return;
      el('leader').textContent = 'Rankings · 3 levels · ' + el('leader').textContent;
      var mask = categories.map(function (cat) { return weights[cat.key] > 0 ? '1' : '0'; }).join('');
      var key = state.scale + ':' + mask;
      if (!cache.has(key)) cache.set(key, buildGraph(cars, categories, weights, state.scale));
      graph = cache.get(key);
      if (!state.selected) {
        var ordered = graph.eligible.slice().sort(ascending(weights, state.scale));
        state.selected = (ordered.find(function (car) { return upgrades(graph, car, weights, state.scale).length; }) || ordered[0] || cars[0]).id;
      }
      el('pareto-car').value = state.selected;
      el('pareto-scale').value = String(state.scale);
      var summary = graph.eligible.length + ' comparable · ' + graph.incomplete.length + ' missing active-metric evidence';
      if (graph.active.length) summary += ' · ' + graph.groups.length + ' profiles · ' + graph.edges.length + ' direct connections';
      else summary = 'No active metrics · all ' + cars.length + ' cars have equal active scores';
      if (el('pareto-coverage').textContent !== summary) el('pareto-coverage').textContent = summary;
      el('pareto-scale-note').hidden = state.scale !== 5;
      el('pareto-incomplete').hidden = !graph.incomplete.length;
      el('pareto-incomplete-summary').textContent = 'Missing active-metric evidence (' + graph.incomplete.length + ')';
      el('pareto-without-eco').hidden = !graph.incomplete.some(function (car) { return weights.eco > 0 && !car.assessed.eco; });
      el('pareto-empty').hidden = graph.eligible.length > 0;
      el('pareto-empty').textContent = 'No cars have complete scores for the active metrics.';
      el('pareto-network').hidden = state.presentation !== 'network' || !graph.eligible.length;
      el('pareto-list').hidden = state.presentation !== 'list' || !graph.eligible.length;
      el('pareto-network-button').setAttribute('aria-pressed', String(state.presentation === 'network'));
      el('pareto-list-button').setAttribute('aria-pressed', String(state.presentation === 'list'));
      if (renderedGraph !== graph) renderStructure();
      comparison(); highlight(); scheduleEdges();
    }
    readLocation();
    el('pareto-car').innerHTML = cars.slice().sort(nameOrder).map(function (car) { return '<option value="' + escape(car.id) + '">' + escape(car.name) + '</option>'; }).join('');
    document.querySelector('.view-tabs').hidden = false;
    function switchView(active) { state.active = active; saveLocation(); options.redraw(); }
    el('tab-rankings').addEventListener('click', function () { switchView(false); });
    el('tab-pareto').addEventListener('click', function () { switchView(true); });
    document.querySelector('.view-tabs').addEventListener('keydown', function (event) {
      if (['ArrowLeft', 'ArrowRight', 'Home', 'End'].indexOf(event.key) < 0) return;
      event.preventDefault();
      var active = event.key === 'Home' ? false : event.key === 'End' ? true : !state.active;
      switchView(active); el(active ? 'tab-pareto' : 'tab-rankings').focus();
    });
    el('pareto-scale').addEventListener('change', function () { state.scale = Number(this.value); state.comparison = null; saveLocation(); options.redraw(); });
    el('pareto-car').addEventListener('change', function () { choose(this.value); });
    el('pareto').addEventListener('click', function (event) {
      var target = event.target.closest('button[data-select]');
      if (target) choose(target.dataset.select);
    });
    el('pareto-comparison').addEventListener('change', function (event) {
      if (event.target.id === 'pareto-alternative') { state.comparison = event.target.value; comparison(); el('pareto-alternative').focus(); }
    });
    el('pareto-without-eco').addEventListener('click', function () {
      options.inputs.eco.value = '0'; options.redraw();
      // The initiating button is now hidden; return to the selected car control.
      el('pareto-car').focus();
    });
    ['network', 'list'].forEach(function (presentation) {
      el('pareto-' + presentation + '-button').addEventListener('click', function () { state.presentation = presentation; options.redraw(); });
    });
    window.addEventListener('resize', scheduleEdges);
    if (typeof ResizeObserver !== 'undefined') new ResizeObserver(scheduleEdges).observe(el('pareto-stage'));
    window.addEventListener('popstate', function () {
      var active = state.active, scale = state.scale;
      readLocation();
      // Hash-only dialog navigation must not replace the opener before focus returns.
      if (active !== state.active || scale !== state.scale) options.redraw();
    });
    window.addEventListener('hashchange', function () {
      if (location.hash === '#ranking' || location.hash === '#pareto') {
        var active = location.hash === '#pareto';
        if (state.active !== active) { state.active = active; saveLocation(); options.redraw(); }
      }
    });
    return { update: update, isActive: function () { return state.active; } };
  }

  var api = { buildGraph: buildGraph, dominates: dominates, total: total, upgrades: upgrades, preferredPath: preferredPath, createView: createView };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.CarPareto = api;
})(typeof window !== 'undefined' ? window : globalThis);
