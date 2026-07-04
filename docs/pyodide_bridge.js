/*
 * pyodide_bridge.js — makes the SAME UI run in a browser.
 *
 * The desktop app talks to Python through Qt's QWebChannel. Here we stand up an
 * equivalent `backend` object, but the "Python" is Pyodide (CPython compiled to
 * WebAssembly) running the EXACT same app/core.py + analytics.py + viz.py.
 *
 * app.js only needs a `backend` with the same method(...args, callback) shape
 * and a `backend.toast.connect(fn)`, plus window.__edaConnect to hand it over.
 */
(function () {
  let pyReady = null;          // Promise<pyodide>
  let pyHandle = null;         // Python dispatch function (PyProxy)
  let pyodideObj = null;
  let toastHandler = null;

  const PY_FILES = ['analytics.py', 'viz.py', 'core.py'];

  async function initPyodide(status) {
    status('Loading Python runtime…');
    const pyodide = await loadPyodide();
    pyodideObj = pyodide;

    status('Loading data libraries (pandas, scipy)…');
    await pyodide.loadPackage(['numpy', 'pandas', 'scipy', 'micropip']);

    status('Adding Excel support…');
    // runPythonAsync is the reliable way to await an async Python call from JS.
    try {
      await pyodide.runPythonAsync(
        "import micropip\nawait micropip.install('openpyxl')");  // enables .xlsx uploads
    } catch (e) { console.warn('openpyxl install skipped:', e); }

    status('Loading analysis modules…');
    try { pyodide.FS.mkdir('eda'); } catch (e) {}
    pyodide.FS.writeFile('eda/__init__.py', '');
    for (const f of PY_FILES) {
      const txt = await (await fetch('py/' + f)).text();
      pyodide.FS.writeFile('eda/' + f, txt);
    }

    // Build the dispatcher: one entry point JS calls for every backend method.
    pyodide.runPython(`
import sys, json
if '' not in sys.path: sys.path.insert(0, '')
from eda.core import EdaCore
from eda import analytics as _A
_core = EdaCore()

def _handle(method, args_json):
    try:
        args = json.loads(args_json) if args_json else []
        if method == 'get_state':        r = _core.get_state()
        elif method == 'set_qoi':        r = _core.set_qoi(args[0])
        elif method == 'apply_types':    r = _core.apply_types(json.loads(args[0]))
        elif method == 'reset_data':     r = _core.reset()
        elif method == 'univariate':     r = _core.univariate(args[0], args[1], args[2], args[3])
        elif method == 'multivariate':   r = _core.multivariate(json.loads(args[0]))
        elif method == 'missing_overview': r = _core.missing_overview()
        elif method == 'apply_missing':  r = _core.apply_missing(args[0], json.loads(args[1]) if args[1] else None)
        elif method == 'load_file':      r = _core.load_file(args[0], args[1] if len(args) > 1 else None)
        else:                            r = {'ok': False, 'error': 'unknown method ' + method}
        toast = _core.last_toast; _core.last_toast = None
        return json.dumps({'result': _A.clean(r), 'toast': list(toast) if toast else None})
    except Exception as e:
        return json.dumps({'result': {'ok': False, 'error': str(e)},
                           'toast': ['Error: ' + str(e), 'error']})
`);
    pyHandle = pyodide.globals.get('_handle');
    return pyodide;
  }

  // Call Python, surface any toast, hand the result JSON to app.js's callback.
  function dispatch(method, args, cb) {
    let parsed;
    try {
      parsed = JSON.parse(pyHandle(method, JSON.stringify(args)));
    } catch (e) {
      parsed = { result: { ok: false, error: e.message }, toast: ['Error: ' + e.message, 'error'] };
    }
    if (parsed.toast && toastHandler) toastHandler(parsed.toast[0], parsed.toast[1]);
    if (cb) cb(JSON.stringify(parsed.result));
    return parsed.result;
  }

  async function loadBytesIntoCore(name, uint8, cb) {
    try {
      pyodideObj.FS.writeFile('/tmp/' + name, uint8);
      dispatch('load_file', ['/tmp/' + name, name], cb);
    } catch (e) {
      if (toastHandler) toastHandler('Load failed: ' + e.message, 'error');
      if (cb) cb(JSON.stringify({ ok: false }));
    }
  }

  function makeBackend() {
    const b = {};
    // Plain compute methods → straight through to Python.
    ['get_state', 'set_qoi', 'apply_types', 'reset_data', 'univariate',
      'multivariate', 'missing_overview', 'apply_missing'].forEach(m => {
        b[m] = function (...args) { const cb = args.pop(); return dispatch(m, args, cb); };
      });

    b.toast = { connect: fn => { toastHandler = fn; } };

    // Sample dataset (bundled CSV next to the page).
    b.sample_data_path = cb => cb(JSON.stringify({ ok: true, path: 'sample_data/churn_sample.csv' }));

    b.load_path = async (path, cb) => {
      try {
        const buf = new Uint8Array(await (await fetch(path)).arrayBuffer());
        await loadBytesIntoCore(path.split('/').pop(), buf, cb);
      } catch (e) {
        if (toastHandler) toastHandler('Could not fetch file: ' + e.message, 'error');
        cb(JSON.stringify({ ok: false }));
      }
    };

    // Browse = a hidden <input type=file>, then load its bytes into Pyodide's FS.
    b.browse_and_load = cb => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = '.csv,.tsv,.xlsx,.xls';
      input.onchange = async () => {
        const file = input.files[0];
        if (!file) { cb(JSON.stringify({ ok: false, cancelled: true })); return; }
        const buf = new Uint8Array(await file.arrayBuffer());
        await loadBytesIntoCore(file.name, buf, cb);
      };
      input.click();
    };

    // Export: browser-native.
    b.export_report = fmt => {
      if (fmt === 'pdf') {
        window.print();                       // use the browser's Save-as-PDF
      } else {
        const html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
        const blob = new Blob([html], { type: 'text/html' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'eda_report.html';
        a.click();
        if (toastHandler) toastHandler('Saved eda_report.html', 'success');
      }
    };
    return b;
  }

  // Hook app.js picks up (see boot() in app.js).
  window.__edaConnect = function (onReady) {
    const overlay = document.getElementById('boot-overlay');
    const status = msg => { const s = document.getElementById('boot-status'); if (s) s.textContent = msg; };
    if (!pyReady) pyReady = initPyodide(status);
    pyReady.then(() => {
      status('Ready');
      if (overlay) overlay.classList.add('hidden');
      onReady(makeBackend());
    }).catch(err => {
      console.error(err);
      status('Failed to load: ' + (err && err.message ? err.message : err));
    });
  };
})();
