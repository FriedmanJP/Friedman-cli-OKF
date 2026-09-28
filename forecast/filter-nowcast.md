---
type: Feature
title: Trend-Cycle Filters and Nowcasting
description: HP, boosted HP, Hamilton, Beveridge-Nelson, Baxter-King, and X-13 decompositions plus DFM/BVAR/bridge nowcasts, news decomposition, and nowcast-model forecasts.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/filter.md
tags: [filter, hp, hamilton, beveridge-nelson, baxter-king, x13, nowcast, dfm, bridge, news]
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:58:15Z
sources:
  - id: generated-filter
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/filter.md
    title: Generated filter reference (options, defaults, output tables)
  - id: generated-nowcast
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/nowcast.md
    title: Generated nowcast reference (options, defaults, output tables)
  - id: filter-guide
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/filter.md
    title: Filter narrative guide (decompositions, frequency mapping, examples)
  - id: nowcast-guide
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/nowcast.md
    title: Nowcast narrative guide (panel splits, priors, vintage rules, bridge gap)
---

# Summary

Eleven leaves split series into trend and cycle or estimate the current quarter from mixed-frequency panels. The six `filter` leaves regress nothing: each splits every selected column into a trend (permanent) and cycle (transitory) component and reports the cycle variance ratio on stderr. `hp` penalizes second-difference curvature with λ (6.25 annual, 1600 quarterly, 129600 monthly); `bhp` iteratively re-applies HP until a stopping criterion fires (Phillips–Shi 2021), hardening the trend against breaks; `hamilton` defines the cycle as the residual of projecting yt on yt−h…yt−h−p+1 (first h+p−1 observations have no cycle value); `bn` splits into random-walk trend and stationary cycle analytically from an ARIMA fit or via state space; `bk` keeps oscillations with periods between `--pl` and `--pu` through a symmetric ±K window (costing K observations at each end); `x13` runs X-13ARIMA-SEATS seasonal adjustment via a pure-Julia X-11/SEATS port (no external binary), emitting five tables and requiring at least 3×frequency observations. The five `nowcast` leaves estimate the current quarter from a monthly/quarterly panel: columns split via `--monthly-vars`/`--quarterly-vars` (omit both and all-but-last are monthly with the last as target; `--target-var 0` means last). `dfm` fits a dynamic factor model by EM, `bvar` a mixed-frequency BVAR (`conjugate` vs `litterman` log-likelihoods are not comparable — compare lags within a prior, priors out of sample), `bridge` runs bridge equations with separate `--lag-m`/`--lag-q`/`--lag-y` knobs, `news` attributes a nowcast revision to releases by comparing two same-shape vintages (`--data-new`/`--data-old`, no positional; newer fills cells, never adds rows), and `forecast` multi-steps a fitted DFM/BVAR model. Known gap: `--method=bridge` on `nowcast forecast` fails — upstream defines `forecast` only for DFM/BVAR models.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman filter hp` | Hodrick–Prescott trend/cycle by time index | `hp_filter` (per-variable trend and cycle) |
| `friedman filter bhp` | Boosted HP trend/cycle (Phillips & Shi 2021) | `boosted_hp_filter` |
| `friedman filter hamilton` | Hamilton (2018) regression-filter trend/cycle over the valid range | `hamilton_filter` |
| `friedman filter bn` | Beveridge–Nelson permanent/transitory split | `beveridge_nelson_decomposition` |
| `friedman filter bk` | Baxter–King band-pass trend/cycle over the untrimmed range | `baxter_king_filter` |
| `friedman filter x13` | X-13ARIMA-SEATS seasonal adjustment (X-11 / SEATS, pure Julia) | `x_13_seasonally_adjusted`; `x_13_trend`; `x_13_seasonal_factors`; `x_13_irregular`; `x_13_diagnostics` (ARIMA order, AIC, σ², outlier count, T) |
| `friedman nowcast dfm` | DFM nowcast by EM (Banbura–Giannone–Reichlin) | `nowcast_dfm` (nowcast, forecast, log-likelihood, EM iterations) |
| `friedman nowcast bvar` | Mixed-frequency BVAR nowcast | `nowcast_bvar` (nowcast, forecast, log-likelihood); `nowcast_bvar_hyperparameters` (optimized λ, θ, μ, α, θ×) |
| `friedman nowcast bridge` | Bridge-equation nowcast | `nowcast_bridge` (nowcast, forecast, equation count) |
| `friedman nowcast news` | News decomposition (Banbura & Modugno 2014) across two vintages | `nowcast_news_decomposition` (per-variable news impacts) |
| `friedman nowcast forecast` | Multi-step forecast from a fitted DFM/BVAR nowcasting model (`bridge` fails: no upstream method) | `nowcast_forecast` (path by horizon, one column per variable) |

Filter leaves share the `data` CSV positional plus `--columns`/`-c` (comma-separated indices; default all numeric), `--format`/`-f`, `--output`/`-o`, `--plot-save`, `--plot`, and `--result`/`--save-result` handles:

| Option / Flag | Leaves | Default | Description |
|---|---|---|---|
| `--lambda` / `-l` | hp, bhp | `1600.0` | Smoothing parameter (6.25 annual, 1600 quarterly, 129600 monthly) |
| `--stopping` | bhp | `BIC` | `BIC`, `ADF`, `fixed` |
| `--max-iter` | bhp | `100` | Maximum boosting iterations |
| `--sig-p` | bhp | `0.05` | ADF significance level (ADF stopping only) |
| `--horizon` | hamilton | `8` | Forecast horizon h |
| `--lags` / `-p` | hamilton | `4` | Lags p in the projection |
| `--method` | bn (`arima\|statespace`), x13 (`seats\|x11`) | `arima` / `seats` | Decomposition method |
| `--p` / `--q` | bn | auto | AR/MA orders (ARIMA method only) |
| `--pl` / `--pu` / `--K` | bk | `6` / `32` / `12` | Min/max oscillation period; truncation half-length |
| `--frequency` | x13 | `12` | Seasonal period: 4 (quarterly) or 12 (monthly) |
| `--transform` | x13 | `auto` | Pre-transformation: `auto`, `log`, `none` (`log` for strictly-positive multiplicative seasonality) |
| `--critical-value` | x13 | `0.0` | Outlier critical value (0 = automatic) |
| `--outliers` | x13 | `true` | Detect AO/LS/TC outliers (`true`/`false`) |
| `--trading-day` (flag) | x13 | off | Trading-day regressors |
| `--easter` (flag) | x13 | off | Easter effect regressor |

Nowcast leaves share the panel split plus `--format`/`-f` and `--output`/`-o` (dfm/forecast/news also take `--plot-save`/`--plot`; bridge/bvar do not):

| Option | Leaves | Default | Description |
|---|---|---|---|
| `data` (arg) | dfm, bvar, bridge, forecast | — | Path to CSV panel (news takes vintages instead) |
| `--monthly-vars` | all 5 | `0` | Monthly variables (first N columns; omit with `--quarterly-vars` for all-but-last) |
| `--quarterly-vars` | all 5 | `0` | Quarterly variables (remaining columns) |
| `--target-var` | all 5 | `0` | Target variable index (0 = last) |
| `--factors` / `-r` | dfm (2), forecast-DFM (2), news-DFM (2) | `2` | Number of factors |
| `--lags` / `-p` | dfm (1), bvar (5), forecast (1), news (1) | — | Factor VAR lags / VAR lags |
| `--idio` | dfm | `ar1` | Idiosyncratic component: `ar1`, `iid` |
| `--max-iter` | dfm | `100` | Maximum EM iterations |
| `--prior` | bvar | `conjugate` | `conjugate` (GLP dummy-observation NIW) or `litterman` (fixed-Σ) |
| `--theta-cross` | bvar | — | Cross-variable tightness > 0 (litterman only; usage error with conjugate) |
| `--lambda0` / `--theta0` / `--miu0` / `--alpha0` | bvar | `0.2` / `1.0` / `1.0` / `2.0` | Initial shrinkage λ, lag-decay θ, sum-of-coefficients μ, co-persistence α |
| `--lag-m` / `--lag-q` / `--lag-y` | bridge | `1` / `1` / `1` | Monthly-indicator / quarterly-indicator / dependent-variable lags |
| `--data-new` / `--data-old` | news | (required) | New / old vintage CSV (same shape; newer fills cells, never adds rows) |
| `--method` | news (`dfm\|bvar`), forecast (`dfm\|bvar\|bridge`) | `dfm` | Nowcasting model (`forecast --method=bridge` fails upstream) |
| `--target-period` | news | `0` | Target period (0 = last) |
| `--horizons` | forecast | `4` | Forecast horizon (no short flag: `-h` is help) |

# Examples

```bash
friedman filter hp :nile --lambda=1600
friedman filter hp :nile --columns=1 --lambda=6.25
friedman filter hamilton :nile --horizon=8 --lags=4
friedman filter bn :nile --p=2 --q=2
friedman filter bk :nile --pl=6 --pu=32 --K=12
friedman filter bhp :nile --lambda=1600 --stopping=BIC
awk 'BEGIN{srand(7); print "y"; for(t=1;t<=120;t++) printf "%.4f\n", 100+10*sin(2*3.14159265*t/12)+0.05*t+0.3*(rand()-0.5)*2}' > monthly.csv && friedman filter x13 monthly.csv --frequency=12 --method=x11 --transform=none
friedman nowcast dfm :fred_md --factors=3 --lags=2
friedman nowcast bvar :fred_md --lags=5
friedman nowcast bvar :fred_md --prior=litterman --theta-cross=0.5
friedman nowcast bridge :fred_md --lag-m=2 --lag-q=1 --lag-y=1
friedman nowcast forecast :fred_md --method=dfm --horizons=4
```

# See also

* [Forecasting and Forecast Evaluation](forecast.md) - out-of-sample projections; `forecast evaluate` scores saved nowcast paths
* [Correlograms and Spectral Density](../spectral-filter/spectral-density.md) - ACF/periodogram/density diagnostics for filtered series
* [Cross-Spectra and Transfer Functions](../spectral-filter/spectral-cross.md) - theoretical gain/phase of the HP, BK, and Hamilton filters
