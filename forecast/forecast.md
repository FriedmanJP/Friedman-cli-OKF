---
type: Feature
title: Forecasting and Forecast Evaluation
description: Point and Waggoner-Zha conditional forecasts across multivariate, factor, regime, univariate, and volatility models, plus model-agnostic accuracy metrics, comparison tests, and combination.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/forecast.md
tags: [forecast, conditional-forecast, var, bvar, vecm, arima, volatility, forecast-evaluation, diebold-mariano, combination]
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:58:15Z
sources:
  - id: generated-forecast
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/forecast.md
    title: Generated forecast reference (options, defaults, output tables)
  - id: forecast-guide
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/forecast.md
    title: Forecast narrative guide (leaf choice, conditions file, evaluate semantics)
  - id: forecast-src
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/forecast.jl
    title: Forecast command implementation
---

# Summary

Thirty-five leaves project fitted models forward. Twenty-nine model leaves re-estimate on the `data` CSV (or reuse a `--model` handle) and forecast: multivariate VAR/BVAR/FAVAR/LP/scenario/VECM, factor static/dynamic/GDFM/SDFM, regime MS/MS-AR/SETAR/STAR, univariate ARFIMA/ARIMA/MIDAS/SARIMA, and eleven volatility leaves (ARCH/GARCH/EGARCH/GJR-GARCH/SV plus APARCH/CGARCH/FIGARCH/FIEGARCH/IGARCH/GARCH-MIDAS). Most render the tidy `horizon | variable | value | lower | upper` table (`lower`/`upper` are missing when no interval ships); three deliberate exceptions keep information the generic schema would drop — ARFIMA uses the single-series `horizon | forecast | lower | upper` form, MIDAS adds a standard error plus a summary table, and volatility leaves use `horizon | variance | volatility` (GARCH-MIDAS splits into `total_variance | long_run | short_run | volatility`). Six `forecast evaluate` leaves score already-computed forecasts model-agnostically: `data` carries the realized column named by `--actual`, forecasts arrive as `--forecasts` columns or `--result` handle stems (never both), and each leaf validates its forecast-count arity. `scenario` is the Waggoner–Zha conditional forecast: a `--conditions-file` long CSV (`variable,period,value[,sd]`) pins paths — `sd` 0/absent is hard, positive is soft — and the leaf reports the conditioned path beside its `unconditional` baseline plus the implied structural shocks; check the shocks before believing the path. Note the reserved-name trap: `--conditions` is a pre-dispatch global (GPL notice), so the leaf spells it `--conditions-file`. SETAR/STAR forecast leaves offer no `--plot`/`--plot-save` (no upstream plot recipe for the forecast type).

# Functions

Evaluate leaves (model-agnostic; arity in parentheses):

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman forecast evaluate metrics` | Point accuracy per forecast (≥1): ME, MAE, RMSE, MAPE, sMAPE, MASE, Theil U1/U2 + Theil MSE bias/variance/covariance split; only evaluate leaf with plot flags | `forecast_accuracy_metrics` (one row per forecast); `theil_mse_decomposition` |
| `friedman forecast evaluate dm` | Diebold–Mariano (1995) equal-accuracy test (exactly 2); `d = g(e1) − g(e2)`, positive favors fc2; HLN correction on by default (`t_{T−1}`); invalid for nested models | `diebold_mariano_test` (statistic, p-value, mean differential, lrvar, HLN, n) |
| `friedman forecast evaluate clark-west` | Clark–West (2007) adjusted-MSPE test for nested models (exactly 2, ordered small then big); one-sided `greater` vs N(0,1) | `clark_west_test` |
| `friedman forecast evaluate mincer-zarnowitz` | Efficiency regression `actual = a + b·fc` (exactly 1); joint test of (a,b)=(0,1) via χ²(2) Wald and F(2,T−2) | `mincer_zarnowitz_efficiency_test` |
| `friedman forecast evaluate encompassing` | HLN (1998) encompassing test (exactly 2): `b2 = 0` in `actual = a + b1·fc1 + b2·fc2`; non-rejection means fc1 encompasses fc2 | `forecast_encompassing_test` |
| `friedman forecast evaluate combine` | Blend ≥2 forecasts: `equal`, `bates-granger` (inverse-MSE), `granger-ramanathan` (constrained LS; weights may be negative) | `forecast_combination_weights` (`model \| weight \| mse`, weights sum to 1); `combined_forecast_series` (`--emit-series`) |

Model leaves:

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman forecast multivariate var` | VAR forecasts; auto lags unless `--lags`; analytical or bootstrap intervals | `var_forecast` (tidy) |
| `friedman forecast multivariate bvar` | BVAR forecasts with posterior credible bands; `--sampler direct\|gibbs`, TOML `--config` prior | `bvar_forecast` (tidy; 68% bands) |
| `friedman forecast multivariate favar` | FAVAR forecasts; `--panel-forecast` switches factor-level to panel-wide output | `favar_forecast` (tidy) |
| `friedman forecast multivariate lp` | Direct LP forecasts along a `--shock-size` impulse to variable `--shock` | `lp_forecast` (tidy) |
| `friedman forecast multivariate scenario` | Waggoner–Zha conditional forecast under `--method var\|bvar` | `conditional_forecast` (+ `unconditional` baseline); `implied_structural_shocks`; `scenario_settings` |
| `friedman forecast multivariate vecm` | VECM level forecasts; `--rank auto` via Johansen; intervals off by default | `vecm_forecast` (tidy) |
| `friedman forecast factor static` | PCA static-factor forecasts reconstructed to observables | `static_factor_forecast` (tidy) |
| `friedman forecast factor dynamic` | Dynamic-factor forecasts; factors follow a VAR(`--factor-lags`) | `dynamic_factor_forecast` (tidy) |
| `friedman forecast factor gdfm` | GDFM forecasts; `--method ar\|one-sided\|spectral` projection | `gdfm_forecast` (tidy) |
| `friedman forecast factor sdfm` | Structural-DFM panel forecasts; `--id` identification, `--q-method` auto rank | `sdfm_forecast` (tidy) |
| `friedman forecast regime ms` | MS-regression forecasts averaged over `--reps` simulated regime paths (+ predicted regime probabilities); `--x-future` required unless intercept-only | `ms_regression_forecast` (tidy); `ms_regression_predicted_regime_probabilities` |
| `friedman forecast regime ms-ar` | MS-AR forecasts over simulated regime paths (+ predicted regime probabilities); Hamilton constant-variance default | `ms_ar_forecast` (tidy); `ms_ar_predicted_regime_probabilities` |
| `friedman forecast regime setar` | SETAR bootstrap-simulation forecasts; `--d` integer or `auto`; `--ci-level` must be 0.90/0.95/0.99; no plot flags | `setar_forecast` (tidy) |
| `friedman forecast regime star` | Self-exciting STAR bootstrap-simulation forecasts (`--type lstr1\|lstr2\|estr\|auto`); no plot flags | `star_forecast` (tidy) |
| `friedman forecast univariate arfima` | ARFIMA forecasts; `--method css\|mle`; AR(∞) truncation `--trunc-lag` | `arfima_forecast` (`horizon \| forecast \| lower \| upper`) |
| `friedman forecast univariate arima` | ARIMA forecasts; omit `--p` for auto selection bounded by `--max-p`/`--max-d`/`--max-q` under `--criterion` | `arima_forecast` (tidy) |
| `friedman forecast univariate midas` | Direct h-step ADL-MIDAS forecast of the low-frequency target; `--hf-data`/`--m`/`--k` required | `midas_forecast` (+ `se`); `midas_forecast_summary` |
| `friedman forecast univariate sarima` | SARIMA forecasts; `--auto` forces `auto_sarima`; seasonal bounds `--max-P`/`--max-Q` | `sarima_forecast` (tidy) |
| `friedman forecast volatility arch` | ARCH variance path (Gaussian-only; no `--dist`) | `arch_volatility_forecast` (`horizon \| variance \| volatility`) |
| `friedman forecast volatility garch` | GARCH variance path; `--dist normal\|student\|ged` | `garch_volatility_forecast` |
| `friedman forecast volatility egarch` | EGARCH variance path; `--dist` | `egarch_volatility_forecast` |
| `friedman forecast volatility gjr-garch` | GJR-GARCH variance path; `--dist` | `gjr_garch_volatility_forecast` |
| `friedman forecast volatility sv` | SV variance path; `--draws` MCMC (Gaussian-only) | `sv_volatility_forecast` |
| `friedman forecast volatility aparch` | APARCH variance path; optional `--fix-delta`/`--fix-gamma` | `aparch_volatility_forecast` |
| `friedman forecast volatility cgarch` | Component-GARCH variance path | `cgarch_volatility_forecast` |
| `friedman forecast volatility figarch` | FIGARCH variance path; `--d0`, `--truncation`, `--dist` | `figarch_volatility_forecast` |
| `friedman forecast volatility fiegarch` | FIEGARCH variance path; `--d0`, `--truncation`, `--dist` | `fiegarch_volatility_forecast` |
| `friedman forecast volatility igarch` | IGARCH variance path | `igarch_volatility_forecast` |
| `friedman forecast volatility garch-midas` | GARCH-MIDAS variance path split into long/short-run; `--m-freq` required; no interval level or plot flags | `garch_midas_volatility_forecast` (`total_variance \| long_run \| short_run \| volatility`) |

Every leaf takes the `data` CSV positional. Evaluate leaves share `--actual` (required), `--forecasts`, `--result` (comma-separated handle stems), `--format`/`-f`, `--output`/`-o`:

| Option / Flag | Evaluate leaves | Default | Description |
|---|---|---|---|
| `--horizon` | clark-west, dm | `1` | Forecast horizon (sets truncation lag h−1) |
| `--alternative` | clark-west | `greater` | `two-sided`, `less`, `greater` |
| `--alternative` | dm | `two-sided` | `two-sided`, `less`, `greater` |
| `--loss` | dm | `se` | `se` (squared), `ad` (absolute) |
| `--no-hln` (flag) | dm | off | Disable HLN correction (use N(0,1)) |
| `--lags` | mincer-zarnowitz, encompassing | `0` | Newey–West HAC lag (0 = White) |
| `--kernel` | mincer-zarnowitz, encompassing | `bartlett` | `bartlett`, `parzen`, `quadratic_spectral`, `tukey_hanning` |
| `--method` | combine | `equal` | `equal`, `bates-granger`, `granger-ramanathan` |
| `--emit-series` (flag) | combine | off | Also emit the combined series |
| `--seasonal-period` | metrics | `1` | Seasonal lag for MASE naive scaling |
| `--plot` / `--plot-save` | metrics only | off | Display / save interactive plot |

Model-leaf options (all 29 also take `--output`/`-o`, `--format`/`-f`, `--model` to skip re-estimation, `--result`/`--save-result` handles; all but setar/star/garch-midas/ms/ms-ar take `--plot`/`--plot-save`):

| Option / Flag | Leaves | Default | Description |
|---|---|---|---|
| `--horizons` | all model leaves | `12` (vol extended: `10`) | Forecast horizon (short `-H` on arfima/aparch/cgarch/figarch/fiegarch/igarch/garch-midas) |
| `--lags` / `-p` | var (auto), bvar (4), favar (2), lp (4), vecm levels (2), scenario (auto/4) | — | Lag orders |
| `--draws` / `-n` | bvar (2000), scenario-bvar (2000), sv (5000) | — | MCMC draws |
| `--sampler` | bvar, scenario-bvar | `direct` | `direct`, `gibbs` |
| `--config` (+ `--config-json`, `--set`, `--strict`) | bvar, scenario, sdfm, garch-midas | — | TOML config (BVAR prior / sign restrictions / garch_midas x_lf) |
| `--confidence` | var, vecm, scenario, arfima, arima | `0.95` | Interval level |
| `--conf-level` | static, lp, aparch, cgarch, figarch, fiegarch, igarch | `0.95` | Interval level |
| `--ci-level` | sarima, setar, star | `0.95` | Band coverage (setar/star: exactly 0.90/0.95/0.99) |
| `--ci-method` | var (analytical\|bootstrap), vecm (none\|bootstrap\|parametric), static (none\|bootstrap\|parametric), lp (analytical\|bootstrap\|none), sdfm (`--ci` none\|bootstrap) | — | Interval method |
| `--conditions-file` | scenario | (required) | Long CSV `variable,period,value[,sd]` |
| `--method` | scenario (`var\|bvar`), dynamic (`twostep\|em`), gdfm (`ar\|one-sided\|spectral`), lp vcov — no; arfima (`css\|mle`), arima (`ols\|css\|mle\|css_mle`), sarima (`css_mle\|mle\|css`) | — | Estimator/projection selectors |
| `--replications` | scenario (1000), vecm (500), sdfm `--reps` (200) | — | Simulation/bootstrap draws for bands |
| `--shock` / `--shock-size` | lp | `1` / `1.0` | Shocked variable index; impulse size |
| `--vcov` | lp | `newey_west` | `newey_west`, `white`, `driscoll_kraay` |
| `--n-boot` | lp | `500` | Bootstrap replications |
| `--rank` / `-r` | vecm | `auto` | Cointegration rank |
| `--deterministic` | vecm | `constant` | `none`, `constant`, `trend` |
| `--nfactors` / `-r` | static, dynamic, gdfm | auto | Factor counts |
| `--factor-lags` / `-p` | dynamic | `1` | Factor VAR lag order |
| `--dynamic-rank` / `-q` | gdfm | auto | Dynamic rank |
| `--spectral` | gdfm, sdfm | `lag-window` | `lag-window` (FHLR), `smoothed-periodogram` |
| `--factors` / `-q/-r` | sdfm (`-q`), favar (`-r`) | auto | Dynamic factors / factor count |
| `--id` | sdfm | `cholesky` | `cholesky`, `sign`, `proxy`, `lewis-tvv`, `sv-em`, `gmm-moments` (proxy needs `--instrument`) |
| `--q-method` | sdfm | `hallin-liska` | `hallin-liska`, `bai-ng`, `amengual-watson` |
| `--instrument` | sdfm | — | Proxy-instrument CSV column (with `--id proxy`) |
| `--var-lags` | sdfm | `1` | Factor VAR lag order |
| `--key-vars` | favar | — | Key variable names or indices |
| `--panel-forecast` (flag) | favar | off | Panel-wide instead of factor-level output |
| `--dep` | ms | first numeric | Dependent variable column |
| `--k-regimes` | ms, ms-ar | `2` | Number of regimes (≥ 2) |
| `--max-iter` | ms (500), ms-ar (1000), arfima (500), sarima (500), midas (500) | — | EM/optimizer iterations |
| `--tol` | ms | `1e-8` | EM convergence tolerance |
| `--x-future` | ms | — | CSV of future regressors, h×k (required unless intercept-only) |
| `--reps` | ms, ms-ar, setar, star | `1000` | Simulated regime paths / bootstrap paths |
| `--ci-level` (ms/ms-ar) | ms, ms-ar | `0.9` | Band coverage in (0,1) |
| `--no-switching-variance` (flag) | ms | off | Force common σ² (default: σ² switches) |
| `--switching-variance` (flag) | ms-ar | off | Let σ² switch (default: Hamilton constant-variance form) |
| `--column` / `-c` | ms-ar, setar, star, arfima, arima, midas, sarima, all volatility | `1` | Series column index |
| `--p` | ms-ar, setar, star, arfima (0), arima (auto), sarima (auto), garch-family (1) | — | AR/GARCH orders |
| `--d` | setar (`1`, String: int or `auto`), star (`1`), arfima — no; arima (`0`), sarima (`0` + `--D`/`--P`/`--Q`/`--s` 12) | — | Delay lag / differencing / seasonal orders |
| `--type` | star | `auto` | `lstr1`, `lstr2`, `estr`, `auto` |
| `--d0` | arfima (GPH), figarch/fiegarch (0.4) | — | Fractional-d starting value |
| `--trunc-lag` | arfima | `200` | AR(∞) truncation lag |
| `--max-p`/`--max-d`/`--max-q` + `--criterion` | arima | `5`/`2`/`5`, `bic` | Auto-selection bounds and `aic\|bic` |
| `--max-p`/`--max-q`/`--max-P`/`--max-Q` + `--criterion` | sarima | `2`/`2`/`1`/`1`, `aic` | Auto-selection bounds and criterion |
| `--auto` (flag) | sarima | off | Force `auto_sarima` |
| `--no-intercept` (flag) | sarima | off | Exclude intercept |
| `--hf-data` / `--hf-column` / `--m` / `--k` | midas | required/`1`/required/required | HF indicator CSV, HF column, HF-per-LF ratio, HF lags |
| `--weights` | midas | `expalmon` | `expalmon`, `beta2`, `beta3`, `almon`, `umidas` |
| `--p-ar` / `--poly-degree` / `--horizon` / `--level` | midas | `0` / `2` / `1` / `0.95` | ADL lags, Almon degree, direct horizon, interval level |
| `--q` | arima/auto, vol arch (1), garch-family (1) | — | MA/ARCH orders |
| `--dist` | egarch, garch, gjr-garch (`normal\|student\|ged`), figarch, fiegarch (`normal`) | `normal` | Conditional innovation distribution |
| `--fix-delta` / `--fix-gamma` | aparch | — | Fix power/asymmetry parameters |
| `--d0` / `--truncation` | figarch, fiegarch | `0.4` / `1000` | Fractional-d start; ARCH(∞) truncation |
| `--m-freq` / `--k` / `--rv` / `--span` | garch-midas | required/`12`/`realized`/`fixed` | HF-per-LF block, MIDAS lags, `realized\|macro` driver, `fixed\|rolling` span |
| `--strict` (flag) | bvar, scenario, sdfm, garch-midas | off | Config schema warnings become errors (exit 4) |

# Examples

```bash
friedman forecast multivariate var :denmark --horizons 6
friedman forecast multivariate bvar :denmark --horizons 6 --draws 500 --sampler gibbs
friedman forecast multivariate vecm :denmark --rank 1 --deterministic constant --lags 2
cat > scenario.csv <<'EOF'
variable,period,value,sd
LRM,1,0.5,0
LRM,2,0.4,0
LRY,4,0.3,0.5
EOF
friedman forecast multivariate scenario :denmark --conditions-file scenario.csv --horizons 6
friedman forecast univariate arima :nile --p 1 --d 1 --q 1 --horizons 6
friedman forecast regime setar :gnp_hamilton --p 1 --d 1 --horizons 6
friedman forecast volatility garch returns.csv --column 2 --p 1 --q 1 --horizons 6
friedman forecast volatility sv returns.csv --column 2 --draws 500 --horizons 6
cat > eval.csv <<'EOF'
y,f1,f2,f3
2.10,2.00,2.20,2.05
1.80,1.90,1.70,1.85
2.40,2.30,2.50,2.35
EOF
friedman forecast evaluate metrics eval.csv --actual y --forecasts f1,f2,f3
friedman forecast evaluate dm eval.csv --actual y --forecasts f1,f2 --loss se --horizon 1
friedman forecast evaluate clark-west eval.csv --actual y --forecasts f1,f2
friedman forecast evaluate combine eval.csv --actual y --forecasts f1,f2,f3 --method bates-granger
```

# See also

* [In-Sample Fitted Values](predict.md) - fitted values from the same model families
* [Model Residuals](residuals.md) - residuals completing the fit–diagnose loop
* [Trend-Cycle Filters and Nowcasting](filter-nowcast.md) - filters and mixed-frequency nowcasts
* [Policy Counterfactuals and Optimal Policy](../causal-policy/policy-counterfactual.md) - McKay–Wolf rule counterfactuals as the structural scenario parallel
