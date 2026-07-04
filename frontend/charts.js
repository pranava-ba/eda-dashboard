/* charts.js — turn backend chart payloads into themed Plotly figures. */

const PALETTE_TWO = ['#2563eb', '#f97316'];
const PALETTE_MULTI = ['#4f46e5', '#0ea5e9', '#10b981', '#f59e0b',
  '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#eab308', '#64748b'];

const PLOT_CONFIG = {
  responsive: true,
  displaylogo: false,
  modeBarButtonsToRemove: ['lasso2d', 'select2d', 'autoScale2d'],
  toImageButtonOptions: { format: 'png', scale: 2 },
};

function cssVar(name) {
  return getComputedStyle(document.body).getPropertyValue(name).trim();
}

function baseLayout(extra) {
  const text = cssVar('--text');
  const grid = cssVar('--grid');
  const axis = {
    gridcolor: grid, zerolinecolor: grid, linecolor: grid,
    tickfont: { size: 11 }, automargin: true,
  };
  return Object.assign({
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: text, family: 'Inter, system-ui, sans-serif', size: 12 },
    margin: { l: 60, r: 24, t: 40, b: 56 },
    xaxis: Object.assign({}, axis),
    yaxis: Object.assign({}, axis),
    legend: { orientation: 'h', y: 1.12, x: 0, font: { size: 11 } },
    hoverlabel: { font: { family: 'Inter, system-ui, sans-serif' } },
    bargap: 0.18,
    colorway: PALETTE_MULTI,
  }, extra || {});
}

function draw(el, traces, layout) {
  Plotly.react(el, traces, baseLayout(layout), PLOT_CONFIG);
}

/* ── main entry ─────────────────────────────────────────────────────────── */
function renderChart(el, p) {
  if (!p) { el.innerHTML = ''; return; }
  switch (p.kind) {
    case 'hist_norm': return histNorm(el, p);
    case 'box_by_group': return boxByGroup(el, p);
    case 'overlap_hist': return overlapHist(el, p);
    case 'cat_bar': return catBar(el, p);
    case 'grouped_bar': return groupedBar(el, p);
    case 'scatter': return scatter(el, p);
    case 'heatmap': return heatmap(el, p);
    default: el.innerHTML = '';
  }
}

/* ── numeric univariate: histogram + normal curve ───────────────────────── */
function histNorm(el, p) {
  const traces = [{
    type: 'histogram', x: p.values, histnorm: 'probability density',
    marker: { color: PALETTE_MULTI[0], line: { color: cssVar('--surface'), width: 1 } },
    opacity: 0.85, name: 'Distribution',
  }];
  if (p.curve) {
    traces.push({
      type: 'scatter', mode: 'lines', x: p.curve.x, y: p.curve.y,
      line: { color: PALETTE_TWO[1], width: 2.5 },
      name: `Normal(μ=${p.mu.toFixed(1)}, σ=${p.sigma.toFixed(1)})`,
    });
  }
  draw(el, traces, {
    xaxis: { title: { text: p.xlabel } }, yaxis: { title: { text: 'Density' } },
  });
}

/* ── numeric × group: boxplot ───────────────────────────────────────────── */
function boxByGroup(el, p) {
  const pal = p.groups.length <= 2 ? PALETTE_TWO : PALETTE_MULTI;
  const traces = p.groups.map((g, i) => ({
    type: 'box', y: g.values, name: g.name, boxmean: true,
    marker: { color: pal[i % pal.length] },
    line: { width: 1.5 }, fillcolor: pal[i % pal.length] + '33',
  }));
  draw(el, traces, {
    yaxis: { title: { text: p.label } }, showlegend: false,
    margin: { l: 60, r: 24, t: 24, b: 56 },
  });
}

/* ── numeric × group: overlapping histograms ────────────────────────────── */
function overlapHist(el, p) {
  const pal = p.groups.length <= 2 ? PALETTE_TWO : PALETTE_MULTI;
  const traces = p.groups.map((g, i) => ({
    type: 'histogram', x: g.values, name: g.name,
    histnorm: 'probability density', opacity: 0.55,
    marker: { color: pal[i % pal.length] },
  }));
  draw(el, traces, {
    barmode: 'overlay',
    xaxis: { title: { text: p.label } }, yaxis: { title: { text: 'Density' } },
  });
}

/* ── categorical univariate: pie / donut / bar (auto by cardinality) ─────── */
function catBar(el, p) {
  const useProp = p.measure === 'Proportion';
  const values = useProp ? p.pcts : p.counts;
  const n = p.n_cats;

  if (n <= 4) {                       // pie (≤2) or donut (3–4)
    const trace = {
      type: 'pie', labels: p.categories, values: values,
      hole: n <= 2 ? 0 : 0.55,
      marker: { colors: PALETTE_MULTI, line: { color: cssVar('--surface'), width: 2 } },
      textinfo: useProp ? 'label+percent' : 'label+value',
      textposition: 'outside', sort: false,
    };
    draw(el, [trace], { showlegend: false, margin: { l: 20, r: 20, t: 30, b: 20 } });
    return;
  }
  const trace = {
    type: 'bar', x: p.categories, y: values,
    marker: { color: PALETTE_MULTI[0] },
    text: values.map(v => useProp ? v.toFixed(1) + '%' : v.toLocaleString()),
    textposition: 'outside', cliponaxis: false,
  };
  draw(el, [trace], {
    xaxis: { title: { text: p.label }, tickangle: -25 },
    yaxis: { title: { text: useProp ? 'Proportion (%)' : 'Count' } },
    showlegend: false,
  });
}

/* ── grouped / stacked bars (cat×qoi, cat×cat) ──────────────────────────── */
function groupedBar(el, p) {
  const useProp = p.measure === 'Proportion';
  const pal = p.series.length <= 2 ? PALETTE_TWO : PALETTE_MULTI;
  const traces = p.series.map((s, i) => ({
    type: 'bar', name: s.name, x: p.categories, y: s.values,
    marker: { color: pal[i % pal.length] },
  }));
  draw(el, traces, {
    barmode: p.stacked ? 'stack' : 'group',
    xaxis: { title: { text: p.xlabel || p.label || '' }, tickangle: -25 },
    yaxis: { title: { text: useProp ? 'Proportion (%)' : 'Count' } },
  });
}

/* ── scatter + regression ───────────────────────────────────────────────── */
function scatter(el, p) {
  const pal = p.groups.length <= 2 ? PALETTE_TWO : PALETTE_MULTI;
  const traces = p.groups.map((g, i) => ({
    type: 'scattergl', mode: 'markers', name: g.name, x: g.x, y: g.y,
    marker: { color: pal[i % pal.length], size: 6, opacity: 0.55 },
  }));
  if (p.reg) {
    traces.push({
      type: 'scatter', mode: 'lines', x: p.reg.x, y: p.reg.y,
      line: { color: cssVar('--text'), width: 2, dash: 'dash' },
      name: `r = ${p.reg.r}`,
    });
  }
  draw(el, traces, {
    xaxis: { title: { text: p.xlabel } }, yaxis: { title: { text: p.ylabel } },
    showlegend: p.groups.length > 1 || !!p.reg,
  });
}

/* ── correlation heatmap ────────────────────────────────────────────────── */
function heatmap(el, p) {
  const annotations = [];
  for (let i = 0; i < p.labels.length; i++) {
    for (let j = 0; j < p.labels.length; j++) {
      const v = p.z[i][j];
      if (v === null) continue;
      annotations.push({
        x: p.labels[j], y: p.labels[i], text: v.toFixed(2), showarrow: false,
        font: { color: Math.abs(v) > 0.6 ? '#fff' : cssVar('--text'), size: 11 },
      });
    }
  }
  const trace = {
    type: 'heatmap', x: p.labels, y: p.labels, z: p.z,
    zmin: -1, zmax: 1, colorscale: 'RdBu', reversescale: true,
    xgap: 3, ygap: 3, colorbar: { thickness: 12, len: 0.8 },
  };
  draw(el, [trace], {
    annotations,
    xaxis: { tickangle: -30, automargin: true },
    yaxis: { automargin: true, autorange: 'reversed' },
    margin: { l: 90, r: 24, t: 24, b: 90 },
  });
}
