# Test

Specification and hypothesis tests: unit roots and long memory, cointegration and VECM restrictions, breaks and stability, OLS/panel/VAR diagnostics, IV strength, DiD checks, and discrete-choice specification tests. Every leaf reports a named test with its null, statistic, and p-value or critical-value decision; most accept `--result`/`--save-result` handles.

* [Unit roots and long memory](unit-root.md) - ADF, KPSS, PP, Ng-Perron, break-robust and panel unit-root tests, GPH/local-Whittle long-memory estimators, and variance-ratio tests (21 leaves).
* [Cointegration and stability](cointegration.md) - Johansen, residual-based, panel, and bounds cointegration tests, VECM restriction tests, break tests, and bubble detectors (27 leaves).
* [Regression diagnostics](diagnostics.md) - Serial correlation, heteroskedasticity, influence, distributional, nonlinearity, and choice-model specification tests (22 leaves).
* [Panel, VAR, IV, and DiD tests](panel-var.md) - Panel specification, VAR/PVAR diagnostics, weak-instrument-robust IV inference, and difference-in-differences checks (25 leaves).
