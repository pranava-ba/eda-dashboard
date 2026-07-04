/* app.js — SPA logic + QWebChannel bridge for the EDA Dashboard. */

const S = {
  backend: null,
  data: null,            // last get_state() payload
  measure: 'Count',      // 'Count' | 'Proportion'
  withQoi: false,
  tab: 'load',
  uniPlot: 'Boxplot',
  multiPlot: 'Boxplot',
  multiStacked: false,
  multiN: 2,
  multiSel: [],          // [{group, var}]
};

/* ── tiny helpers ─────────────────────────────────────────────────────────*/
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const esc = s => String(s).replace(/[&<>"]/g, c =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function call(method, ...args) {
  return new Promise((resolve, reject) => {
    try { S.backend[method](...args, res => resolve(JSON.parse(res))); }
    catch (e) { reject(e); }
  });
}

/* ── toasts ───────────────────────────────────────────────────────────────*/
function showToast(msg, level = 'info') {
  const wrap = $('#toasts');
  const t = document.createElement('div');
  t.className = `toast toast-${level}`;
  t.innerHTML = `<span class="toast-dot"></span><span>${esc(msg)}</span>`;
  wrap.appendChild(t);
  requestAnimationFrame(() => t.classList.add('show'));
  setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 300); }, 3800);
}

/* ── theme ────────────────────────────────────────────────────────────────*/
function setTheme(theme) {
  document.body.dataset.theme = theme;
  localStorage.setItem('eda-theme', theme);
  $('#theme-toggle').textContent = theme === 'dark' ? '☀️' : '🌙';
  renderTab();  // re-theme charts
}
function toggleTheme() {
  setTheme(document.body.dataset.theme === 'dark' ? 'light' : 'dark');
}

/* ── column pools ─────────────────────────────────────────────────────────*/
function poolFor(group) {
  if (!S.data || !S.data.has_data) return [];
  if (group === '__qoi__') return S.data.qoi ? [S.data.qoi] : [];
  if (group === 'All')
    return S.data.all_columns.filter(c => c !== S.data.qoi);
  return (S.data.groups[group] || []).filter(c => S.data.all_columns.includes(c));
}
function groupOptions(includeQoi = true) {
  const opts = ['All', ...Object.keys(S.data.groups || {})];
  if (includeQoi && S.data.qoi) opts.push('__qoi__');
  return opts;
}
function groupLabel(g) { return g === '__qoi__' ? '🎯 Target' : g; }

/* ── UI atoms ─────────────────────────────────────────────────────────────*/
function selectHTML(id, options, selected, labeler = (x) => x) {
  return `<select id="${id}" class="select">` + options.map(o =>
    `<option value="${esc(o)}" ${o === selected ? 'selected' : ''}>${esc(labeler(o))}</option>`
  ).join('') + `</select>`;
}
function tableHTML(columns, rows, opts = {}) {
  const cls = 'data-table' + (opts.compact ? ' compact' : '');
  return `<div class="table-wrap"><table class="${cls}"><thead><tr>` +
    columns.map(c => `<th>${esc(c)}</th>`).join('') + `</tr></thead><tbody>` +
    rows.map(r => `<tr>` + r.map(v =>
      `<td>${v === null || v === undefined ? '—' : esc(v)}</td>`).join('') + `</tr>`).join('') +
    `</tbody></table></div>`;
}
function statCallout(stat) {
  if (!stat) return '';
  if (!stat.ok)
    return `<div class="stat-card muted"><div class="stat-name">${esc(stat.name || 'Test')}</div>
      <div class="stat-interp">${esc(stat.interpretation || '')}</div></div>`;
  const sig = /No statistically significant/i.test(stat.interpretation);
  const chips = (stat.stats || []).map(s =>
    `<span class="chip"><b>${esc(s.label)}</b> ${esc(s.value)}</span>`).join('');
  return `<div class="stat-card ${sig ? 'muted' : 'sig'}">
      <div class="stat-name">🧪 ${esc(stat.name)}</div>
      <div class="stat-chips">${chips}</div>
      <div class="stat-interp">${esc(stat.interpretation)}</div></div>`;
}
function segmented(control, options, active) {
  return `<div class="segmented" data-control="${control}">` + options.map(o =>
    `<button data-val="${esc(o.val)}" class="${o.val === active ? 'active' : ''}">${esc(o.label)}</button>`
  ).join('') + `</div>`;
}
function emptyState(icon, title, sub) {
  return `<div class="empty"><div class="empty-icon">${icon}</div>
    <div class="empty-title">${esc(title)}</div>
    <div class="empty-sub">${esc(sub || '')}</div></div>`;
}
function chartCard(title, chartId, extraHead = '') {
  return `<div class="card">
    <div class="card-head"><span>${esc(title)}</span>${extraHead}</div>
    <div id="${chartId}" class="chart"></div></div>`;
}

/* ══════════════════════════════════════════════════════════════════════════
   TAB: LOAD
   ══════════════════════════════════════════════════════════════════════════*/
function renderLoad(root) {
  if (!S.data || !S.data.has_data) {
    root.innerHTML = `
      <div class="dropzone card">
        <div class="dz-icon">📂</div>
        <h2>Load a dataset to begin</h2>
        <p class="muted">Excel (.xlsx, .xls) or CSV (.csv, .tsv). Everything runs locally on your machine.</p>
        <div class="dz-actions">
          <button class="btn btn-primary" id="btn-browse">Browse files…</button>
          <button class="btn btn-ghost" id="btn-sample">Use sample data</button>
        </div>
      </div>`;
    $('#btn-browse').onclick = async () => {
      const r = await call('browse_and_load');
      if (r.ok && r.has_data) { S.data = r; renderTab(); syncHeader(); }
    };
    $('#btn-sample').onclick = async () => {
      const sp = await call('sample_data_path');
      if (!sp.ok) return showToast('Sample data not found.', 'error');
      const r = await call('load_path', sp.path);
      if (r.ok && r.has_data) { S.data = r; renderTab(); syncHeader(); }
    };
    return;
  }

  const ov = S.data.overview;
  const metric = (label, val, accent) =>
    `<div class="metric ${accent || ''}"><div class="metric-val">${val}</div>
      <div class="metric-label">${label}</div></div>`;

  const targetBlock = S.data.qoi
    ? `<div class="target-row">
         <span class="target-badge">🎯 Target: <b>${esc(S.data.qoi)}</b></span>
         <span class="muted">${S.data.qoi_nunique} distinct values</span>
         <button class="link" id="btn-change-target">change</button>
       </div>`
    : `<div class="notice warn">
         <b>No target detected.</b> Choose the column you want to analyse (the QoI):
         ${selectHTML('sel-target', ['—', ...S.data.all_columns], '—')}
       </div>`;

  const cols = ov.columns.map(c => [
    c.name, c.dtype, c.type, c.non_null.toLocaleString(),
    c.missing ? c.missing.toLocaleString() : '0', c.unique.toLocaleString(), c.sample,
  ]);

  root.innerHTML = `
    <div class="metrics">
      ${metric('Rows', ov.rows.toLocaleString())}
      ${metric('Columns', ov.cols)}
      ${metric('Numeric', ov.numeric_cols)}
      ${metric('Missing cells', ov.missing.toLocaleString(),
    ov.missing ? 'metric-warn' : 'metric-ok')}
    </div>
    <div class="card">
      <div class="card-head"><span>📄 ${esc(S.data.filename)}</span></div>
      ${targetBlock}
      <div class="card-sub">Column overview</div>
      ${tableHTML(['Column', 'dtype', 'Detected type', 'Non-null', 'Missing', 'Unique', 'Sample'], cols, { compact: true })}
      <div class="card-actions">
        <button class="btn btn-primary" id="btn-goto-types">Continue to Variable Types →</button>
      </div>
    </div>`;

  const chg = $('#btn-change-target'); if (chg) chg.onclick = () => switchTab('types');
  const selT = $('#sel-target');
  if (selT) selT.onchange = async () => {
    if (selT.value === '—') return;
    S.data = await call('set_qoi', selT.value); renderTab(); syncHeader();
  };
  $('#btn-goto-types').onclick = () => switchTab('types');
}

/* ══════════════════════════════════════════════════════════════════════════
   TAB: VARIABLE TYPES
   ══════════════════════════════════════════════════════════════════════════*/
function renderTypes(root) {
  if (!requireData(root)) return;
  const cols = S.data.overview.columns;

  const rows = cols.map(c => `
    <tr>
      <td><code>${esc(c.name)}</code></td>
      <td><span class="pill">${esc(c.dtype)}</span></td>
      <td>${selectHTML('ty-' + cssId(c.name), ['numeric', 'categorical'], c.type)}</td>
    </tr>`).join('');

  root.innerHTML = `
    <div class="card">
      <div class="card-head"><span>🎯 Target column (QoI)</span></div>
      <div class="target-pick">
        ${selectHTML('sel-target2', S.data.all_columns, S.data.qoi || S.data.all_columns[0])}
        <span class="muted">The variable your analysis is centred on (e.g. Churn).</span>
      </div>
    </div>
    <div class="card">
      <div class="card-head"><span>🔧 Variable types</span></div>
      <p class="muted">Review each column's role. Forcing a text column to <b>numeric</b> that
        isn't really numeric will blank it out — so double-check before applying.</p>
      ${tableHTML.length ? '' : ''}
      <div class="table-wrap"><table class="data-table"><thead><tr>
        <th>Variable</th><th>Detected dtype</th><th>Analysis type</th></tr></thead>
        <tbody>${rows}</tbody></table></div>
      <div class="card-actions">
        <button class="btn btn-primary" id="btn-apply-types">Apply &amp; continue →</button>
        <button class="btn btn-ghost" id="btn-reset-types">Reset to original</button>
      </div>
    </div>`;

  $('#sel-target2').onchange = async e => {
    S.data = await call('set_qoi', e.target.value); syncHeader();
  };
  $('#btn-apply-types').onclick = async () => {
    const mapping = {};
    cols.forEach(c => { mapping[c.name] = $('#ty-' + cssId(c.name)).value; });
    if ($('#sel-target2').value !== S.data.qoi)
      await call('set_qoi', $('#sel-target2').value);
    S.data = await call('apply_types', JSON.stringify(mapping));
    syncHeader(); switchTab('univariate');
  };
  $('#btn-reset-types').onclick = async () => {
    S.data = await call('reset_data'); renderTab(); syncHeader();
  };
}

/* ══════════════════════════════════════════════════════════════════════════
   TAB: UNIVARIATE
   ══════════════════════════════════════════════════════════════════════════*/
function renderUnivariate(root) {
  if (!requireData(root)) return;
  if (!S._uniGroup) S._uniGroup = 'All';
  let pool = poolFor(S._uniGroup);
  if (!pool.length) { S._uniGroup = 'All'; pool = poolFor('All'); }
  if (!S._uniVar || !pool.includes(S._uniVar)) S._uniVar = pool[0];

  root.innerHTML = `
    <div class="toolbar">
      <label>KPI group ${selectHTML('u-group', groupOptions(), S._uniGroup, groupLabel)}</label>
      <label>Variable ${selectHTML('u-var', pool, S._uniVar)}</label>
    </div>
    <div id="uni-body"></div>`;

  $('#u-group').onchange = e => {
    S._uniGroup = e.target.value; S._uniVar = null; renderUnivariate(root);
  };
  $('#u-var').onchange = e => { S._uniVar = e.target.value; loadUnivariate(); };
  loadUnivariate();
}

async function loadUnivariate() {
  const body = $('#uni-body');
  if (!body) return;
  const r = await call('univariate', S._uniVar, S.withQoi, S.measure, S.uniPlot);
  if (!r.ok) { body.innerHTML = emptyState('🤔', 'Nothing to show'); return; }

  const summaryHTML = r.summary.kind === 'numeric'
    ? tableHTML(['Statistic', 'Value'], r.summary.rows.map(x => [x.stat, x.value]))
    : tableHTML(['Category', 'Count', '%'],
      r.summary.rows.map(x => [x.category, x.count.toLocaleString(), x.pct + '%']));

  let plotToggle = '';
  if (r.plot_options && r.plot_options.length) {
    plotToggle = segmented('uniPlot',
      r.plot_options.map(o => ({ val: o, label: o })), S.uniPlot);
  }

  body.innerHTML = `
    <div class="grid-2">
      <div class="card">
        <div class="card-head"><span>Summary</span></div>
        ${summaryHTML}
      </div>
      <div class="col-stack">
        ${chartCard('Visual — ' + r.var, 'uni-chart', plotToggle)}
        ${statCallout(r.stat)}
      </div>
    </div>`;
  renderChart($('#uni-chart'), r.chart);
}

/* ══════════════════════════════════════════════════════════════════════════
   TAB: MULTIVARIATE
   ══════════════════════════════════════════════════════════════════════════*/
function renderMultivariate(root) {
  if (!requireData(root)) return;

  // (re)initialise selection slots
  if (S.multiSel.length !== S.multiN) {
    S.multiSel = [];
    for (let i = 0; i < S.multiN; i++) S.multiSel.push({ group: 'All', var: null });
  }

  const nToggle = segmented('multiN',
    [2, 3, 4].map(n => ({ val: String(n), label: n + ' vars' })), String(S.multiN));

  root.innerHTML = `
    <div class="toolbar wrap">
      <label>Variables ${nToggle}</label>
      <label>Cat × Cat style ${segmented('multiStacked',
    [{ val: 'group', label: 'Grouped' }, { val: 'stack', label: 'Stacked' }],
    S.multiStacked ? 'stack' : 'group')}</label>
      <label>Numeric × target ${segmented('multiPlot',
    [{ val: 'Boxplot', label: 'Boxplot' }, { val: 'Overlapping Histogram', label: 'Histogram' }],
    S.multiPlot)}</label>
    </div>
    <div id="multi-selectors" class="selectors"></div>
    <div class="card-actions left">
      <button class="btn btn-primary" id="btn-analyze">Analyze →</button>
    </div>
    <div id="multi-body"></div>`;

  renderMultiSelectors();
  $('#btn-analyze').onclick = loadMultivariate;
}

function renderMultiSelectors() {
  const host = $('#multi-selectors');
  host.innerHTML = '';
  S.multiSel.forEach((slot, i) => {
    const chosenElsewhere = S.multiSel.filter((_, j) => j !== i).map(s => s.var);
    let pool = poolFor(slot.group).filter(v => !chosenElsewhere.includes(v));
    if (!pool.length) pool = poolFor(slot.group);
    if (!slot.var || !pool.includes(slot.var)) slot.var = pool[Math.min(i, pool.length - 1)] || pool[0];

    const row = document.createElement('div');
    row.className = 'selector-row';
    row.innerHTML = `
      <span class="sel-index">${i + 1}</span>
      ${selectHTML('m-grp-' + i, groupOptions(false), slot.group, groupLabel)}
      ${selectHTML('m-var-' + i, pool, slot.var)}`;
    host.appendChild(row);

    $('#m-grp-' + i).onchange = e => { slot.group = e.target.value; slot.var = null; renderMultiSelectors(); };
    $('#m-var-' + i).onchange = e => { slot.var = e.target.value; renderMultiSelectors(); };
  });
}

async function loadMultivariate() {
  const body = $('#multi-body');
  const vars = S.multiSel.map(s => s.var).filter(Boolean);
  if (new Set(vars).size < 2) { body.innerHTML = emptyState('⚠️', 'Pick at least 2 distinct variables'); return; }
  body.innerHTML = `<div class="loading">Computing analyses…</div>`;

  const r = await call('multivariate', JSON.stringify({
    vars, with_qoi: S.withQoi, measure: S.measure,
    plot_mode: S.multiPlot, stacked: S.multiStacked,
  }));
  if (!r.ok) { body.innerHTML = emptyState('⚠️', r.error || 'Could not analyse'); return; }
  if (!r.blocks.length) { body.innerHTML = emptyState('🔍', 'No pairwise analyses for this mix'); return; }

  // group blocks by section
  const sections = {};
  r.blocks.forEach(b => { (sections[b.section] = sections[b.section] || []).push(b); });

  let html = ''; const charts = [];
  Object.entries(sections).forEach(([sec, blocks]) => {
    html += `<h3 class="section-h">${esc(sec)}</h3>`;
    blocks.forEach((b, bi) => {
      const cid = `mc-${esc(sec).replace(/\W/g, '')}-${bi}`;
      const chartDivs = b.charts.map((c, ci) => {
        const id = `${cid}-${ci}`; charts.push({ id, payload: c });
        return `<div id="${id}" class="chart"></div>`;
      }).join('');
      const tableHTMLstr = b.table
        ? `<div class="card-sub">${esc(b.table.title || 'Table')}</div>${tableHTML(b.table.columns, b.table.rows, { compact: true })}`
        : '';
      html += `<div class="card block">
        <div class="card-head"><span>${esc(b.title)}</span></div>
        ${chartDivs}
        ${tableHTMLstr}
        ${statCallout(b.stat)}
      </div>`;
    });
  });
  body.innerHTML = html;
  charts.forEach(c => renderChart($('#' + c.id), c.payload));
}

/* ══════════════════════════════════════════════════════════════════════════
   TAB: MISSING DATA
   ══════════════════════════════════════════════════════════════════════════*/
async function renderMissing(root) {
  if (!requireData(root)) return;
  const r = await call('missing_overview');
  if (!r.ok) { root.innerHTML = emptyState('🤔', 'No data'); return; }

  if (r.total_missing === 0) {
    root.innerHTML = `<div class="card">${emptyState('✅', 'No missing values',
      'This dataset is complete. (The provided sample has none — but real-world files often do, and these tools will handle them.)')}</div>`;
    return;
  }

  const rows = r.columns.map(c => [
    c.column, c.missing.toLocaleString(),
    `<div class="bar"><span style="width:${Math.min(100, c.pct)}%"></span></div> ${c.pct}%`,
  ]);
  // build table manually to allow HTML bar
  const bodyRows = r.columns.map(c => `<tr>
    <td>${esc(c.column)}</td><td>${c.missing.toLocaleString()}</td>
    <td><div class="bar"><span style="width:${Math.min(100, c.pct)}%"></span></div>${c.pct}%</td></tr>`).join('');

  const cols = S.data.all_columns;
  root.innerHTML = `
    <div class="metrics">
      <div class="metric metric-warn"><div class="metric-val">${r.total_missing.toLocaleString()}</div><div class="metric-label">Missing cells</div></div>
      <div class="metric"><div class="metric-val">${r.rows_with_missing.toLocaleString()}</div><div class="metric-label">Rows affected</div></div>
    </div>
    <div class="card">
      <div class="card-head"><span>Missing by column</span></div>
      <div class="table-wrap"><table class="data-table compact"><thead><tr>
        <th>Column</th><th>Missing</th><th>Percent</th></tr></thead><tbody>${bodyRows}</tbody></table></div>
    </div>
    <div class="card">
      <div class="card-head"><span>🧹 Handle missing data</span></div>
      <div class="miss-controls">
        <label>Strategy ${selectHTML('miss-strat', [
      'drop_rows', 'drop_cols', 'mean', 'median', 'mode', 'zero'], 'median', prettyStrat)}</label>
        <label>Scope ${selectHTML('miss-scope', ['All columns', ...cols], 'All columns')}</label>
        <button class="btn btn-primary" id="btn-apply-miss">Apply</button>
        <button class="btn btn-ghost" id="btn-reset-miss">Reset data</button>
      </div>
      <p class="muted">Tip: set variable types first — mean/median apply to numeric columns, mode fills categoricals.</p>
    </div>`;

  $('#btn-apply-miss').onclick = async () => {
    const strat = $('#miss-strat').value;
    const scope = $('#miss-scope').value;
    const cols_json = scope === 'All columns' ? '' : JSON.stringify([scope]);
    S.data = await call('apply_missing', strat, cols_json);
    renderTab(); syncHeader();
  };
  $('#btn-reset-miss').onclick = async () => {
    S.data = await call('reset_data'); renderTab(); syncHeader();
  };
}
function prettyStrat(s) {
  return {
    drop_rows: 'Drop rows with missing', drop_cols: 'Drop columns with missing',
    mean: 'Fill numeric with mean', median: 'Fill numeric with median',
    mode: 'Fill with most frequent', zero: 'Fill numeric with 0',
  }[s] || s;
}

/* ══════════════════════════════════════════════════════════════════════════
   TAB ROUTING + GLOBAL CONTROLS
   ══════════════════════════════════════════════════════════════════════════*/
const TABS = {
  load: renderLoad, types: renderTypes, univariate: renderUnivariate,
  multivariate: renderMultivariate, missing: renderMissing,
};

function requireData(root) {
  if (!S.data || !S.data.has_data) {
    root.innerHTML = `<div class="card">${emptyState('📂', 'No data loaded',
      'Head to the Load Data tab and open a file (or try the sample).')}</div>`;
    return false;
  }
  return true;
}

function renderTab() {
  const root = $('#view');
  const fn = TABS[S.tab];
  if (fn) fn(root);
}
function switchTab(tab) {
  S.tab = tab;
  $$('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  renderTab();
}

function cssId(s) { return s.replace(/[^a-zA-Z0-9_-]/g, '_'); }

function syncHeader() {
  const has = S.data && S.data.has_data;
  $('#file-badge').textContent = has ? S.data.filename : 'No file loaded';
  $('#file-badge').classList.toggle('active', !!has);
  // enable global controls + export only when data present
  $$('.needs-data').forEach(el => el.classList.toggle('disabled', !has));
  const qoiOK = has && !!S.data.qoi;
  const wq = $('.segmented[data-control="withQoi"]');
  if (wq) wq.classList.toggle('disabled', !qoiOK);
  if (!qoiOK && S.withQoi) { S.withQoi = false; }
}

/* segmented-control + tab click delegation */
document.addEventListener('click', e => {
  const seg = e.target.closest('.segmented button');
  if (seg) {
    const control = seg.parentElement.dataset.control;
    const val = seg.dataset.val;
    seg.parentElement.querySelectorAll('button').forEach(b => b.classList.remove('active'));
    seg.classList.add('active');
    onControl(control, val);
    return;
  }
  const tab = e.target.closest('.tab');
  if (tab && !tab.classList.contains('disabled')) switchTab(tab.dataset.tab);
});

function onControl(control, val) {
  switch (control) {
    case 'measure': S.measure = val; renderTab(); break;
    case 'withQoi': S.withQoi = (val === 'with'); renderTab(); break;
    case 'uniPlot': S.uniPlot = val; loadUnivariate(); break;
    case 'multiN': S.multiN = +val; S.multiSel = []; renderMultivariate($('#view')); break;
    case 'multiStacked': S.multiStacked = (val === 'stack'); break;
    case 'multiPlot': S.multiPlot = val; break;
  }
}

/* ── init ─────────────────────────────────────────────────────────────────*/
function boot() {
  setTheme(localStorage.getItem('eda-theme') || 'light');
  $('#theme-toggle').onclick = toggleTheme;
  $('#btn-export-pdf').onclick = () => S.backend.export_report('pdf');
  $('#btn-export-html').onclick = () => S.backend.export_report('html');

  // global controls
  $('#global-measure').innerHTML = segmented('measure',
    [{ val: 'Count', label: 'Count' }, { val: 'Proportion', label: 'Proportion' }], S.measure);
  $('#global-qoi').innerHTML = segmented('withQoi',
    [{ val: 'without', label: 'Without target' }, { val: 'with', label: 'With target' }],
    S.withQoi ? 'with' : 'without');

  // Bridge is pluggable: the web build defines window.__edaConnect (Pyodide);
  // otherwise we use the desktop QWebChannel transport.
  const connect = window.__edaConnect || (cb =>
    new QWebChannel(qt.webChannelTransport, channel => cb(channel.objects.backend)));

  connect(async backend => {
    S.backend = backend;
    if (backend.toast && backend.toast.connect) backend.toast.connect(showToast);
    S.data = await call('get_state');
    syncHeader();
    switchTab('load');
  });
}
window.addEventListener('DOMContentLoaded', boot);
