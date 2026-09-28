---
type: Feature
title: Model Residuals
description: What each fitted model leaves unexplained — response, standardized, and per-category residuals across 40 leaves, including SETAR/STAR which have no predict leaf.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/residuals.md
tags: [residuals, diagnostics, standardized-residuals, deviance, innovations]
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:58:15Z
sources:
  - id: generated-residuals
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/residuals.md
    title: Generated residuals reference (options, defaults, output tables)
  - id: predict-guide
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/predict_residuals.md
    title: predict/residuals narrative guide (residual kinds, regime notes, examples)
  - id: fitted-src
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/fitted.jl
    title: Residuals command implementation (23-kind loop + hand-written specs)
---

# Summary

Forty leaves return the matching residual vector per model: response residuals for regressions and choice models, standardized innovations for volatility models, one-step prediction errors for state-space models, idiosyncratic components for factor models, and per-category matrices for ordered and multinomial models. Every leaf re-estimates from the `data` CSV or reuses a `--model` handle; each `residuals` leaf mirrors its `estimate` sibling's fit options so any fit that changes the residuals can be reproduced, while inference-only options are omitted (`residuals regime setar` drops `--reps`/`--ci-level`/`--het` and skips the Hansen bootstrap entirely). Implementation shape (LEAVES.md open question 5, confirmed in `src/commands/fitted.jl`): the same 23-entry `FITTED_MODEL_KINDS` table behind `predict` expands into 23 residuals leaves, plus 17 hand-written specs — the same 15 as predict (sarima, poisson, nbreg, ms-ar, ms, statespace, sur, 3sls, arfima, six extended-GARCH) plus `setar` and `star`, which exist only here because upstream exposes `StatsAPI.residuals` but no fitted values for `ThresholdModel`/`STARModel` (adding a predict leaf that recomputes the MS-style weighted mean risks diverging from a definition upstream never published). Residual-kind notes: ordered/multinomial leaves take `--kind response` (default; `d−P̂`, rows sum to zero), `pearson`, or `deviance`, and the ordered models add `--generalized` for the length-n Chesher–Irish score residual — deliberately not offered on mlogit, where it is a usage error (exit 2); count models offer no `--kind` (upstream exposes a single residual vector); state-space `--standardized` divides by √F_t for diagnostic checking; `period` on regime leaves is the effective-sample index (SETAR/STAR/MS-AR drop leading lags; MS regression drops nothing).

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman residuals choice logit` | Binary logit response residuals y − p | `logit_residuals` (one row per observation) |
| `friedman residuals choice probit` | Binary probit response residuals y − p | `probit_residuals` |
| `friedman residuals choice ologit` | Ordered-logit per-category residuals (+ optional generalized score residual) | `ordered_logit_residuals` (`resid_<cat>` per `--kind`); `ordered_logit_generalized_residuals` (`--generalized`) |
| `friedman residuals choice oprobit` | Ordered-probit per-category residuals (+ optional generalized score residual) | `ordered_probit_residuals`; `ordered_probit_generalized_residuals` |
| `friedman residuals choice mlogit` | Multinomial-logit per-alternative residuals (no `--generalized`: response residuals already are the generalized residuals) | `multinomial_logit_residuals` |
| `friedman residuals choice poisson` | Poisson residuals y − μ̂ (single kind upstream) | `poisson_residuals` |
| `friedman residuals choice nbreg` | Negative-binomial residuals | `negative_binomial_residuals` |
| `friedman residuals factor static` | Static-factor idiosyncratic component, one column per series | `static_factor_idiosyncratic_component` |
| `friedman residuals factor dynamic` | Dynamic-factor idiosyncratic component | `dynamic_factor_idiosyncratic_component` |
| `friedman residuals factor gdfm` | GDFM idiosyncratic component | `gdfm_idiosyncratic_component` |
| `friedman residuals multivariate var` | VAR residuals, one column per variable | `var_residuals` |
| `friedman residuals multivariate bvar` | BVAR residuals at the posterior mean | `bvar_residuals` |
| `friedman residuals multivariate vecm` | VECM residuals via the VAR representation | `vecm_residuals` |
| `friedman residuals multivariate favar` | FAVAR residuals | `favar_residuals` |
| `friedman residuals panel piv` | Panel IV residuals | `panel_iv_residuals` |
| `friedman residuals panel plogit` | Panel logit residuals | `panel_logit_residuals` |
| `friedman residuals panel pprobit` | Panel probit residuals | `panel_probit_residuals` |
| `friedman residuals panel preg` | Panel regression residuals | `panel_regression_residuals` |
| `friedman residuals regime ms` | MS-regression smoothed-probability-weighted residuals (fit on levels; drops nothing) | `ms_regression_residuals` |
| `friedman residuals regime ms-ar` | MS-AR smoothed-probability-weighted residuals; Hamilton constant-variance default | `ms_ar_residuals` (effective periods) |
| `friedman residuals regime setar` | SETAR residuals; skips the Hansen bootstrap (no `--reps`/`--ci-level`/`--het`) | `setar_residuals` (effective periods) |
| `friedman residuals regime star` | STAR residuals; `--transition-col 0` = self-exciting | `star_residuals` (effective periods) |
| `friedman residuals regression 3sls` | 3SLS per-equation residuals, tidy long; `--config` required | `3sls_residuals_per_equation` |
| `friedman residuals regression reg` | OLS/WLS residuals | `reg_residuals` |
| `friedman residuals regression statespace` | One-step prediction errors v_t (long `period \| residual`; `--standardized` gives v_t/√F_t) | `state_space_innovations` |
| `friedman residuals regression sur` | SUR per-equation residuals, tidy long; `--config` required | `sur_residuals_per_equation` |
| `friedman residuals univariate arfima` | ARFIMA residuals | `arfima_residuals` |
| `friedman residuals univariate arima` | ARIMA residuals | `arima_residuals` |
| `friedman residuals univariate sarima` | SARIMA residuals | `sarima_residuals` |
| `friedman residuals volatility arch` | ARCH standardized residuals | `arch_standardized_residuals` |
| `friedman residuals volatility garch` | GARCH standardized residuals | `garch_standardized_residuals` |
| `friedman residuals volatility egarch` | EGARCH standardized residuals | `egarch_standardized_residuals` |
| `friedman residuals volatility gjr-garch` | GJR-GARCH standardized residuals | `gjr_garch_standardized_residuals` |
| `friedman residuals volatility igarch` | IGARCH standardized residuals | `igarch_standardized_residuals` |
| `friedman residuals volatility cgarch` | CGARCH standardized residuals | `cgarch_standardized_residuals` |
| `friedman residuals volatility aparch` | APARCH standardized residuals | `aparch_standardized_residuals` |
| `friedman residuals volatility figarch` | FIGARCH standardized residuals | `figarch_standardized_residuals` |
| `friedman residuals volatility fiegarch` | FIEGARCH standardized residuals | `fiegarch_standardized_residuals` |
| `friedman residuals volatility garch-midas` | GARCH-MIDAS standardized residuals; `--m-freq` required | `garch_midas_standardized_residuals` |
| `friedman residuals volatility sv` | SV standardized residuals | `sv_standardized_residuals` |

Every leaf takes the `data` CSV positional plus `--format`/`-f`, `--output`/`-o`, and `--model` (saved-model handle, skips re-estimation). Option sets mirror the `predict` sibling except for the residual-kind surface:

| Option / Flag | Leaves | Default | Description |
|---|---|---|---|
| `--dep` | choice ×7, panel ×4, reg, ms | first numeric | Dependent variable column name |
| `--kind` | ologit, oprobit, mlogit | `response` | `response`, `pearson`, `deviance` |
| `--generalized` (flag) | ologit, oprobit only | off | Length-n Chesher–Irish score residual (usage error on mlogit) |
| `--cov-type` | binary/ordered/multinomial choice (hc1), poisson (robust), reg (hc1), panel (cluster) | — | Covariance estimator (same choices as predict) |
| `--clusters` | binary/ordered/multinomial choice, poisson, reg | — | Cluster variable column name |
| `--weights` | reg | — | Weights column (WLS) |
| `--offset` / `--exposure` | poisson, nbreg | — | Log-scale offset / exposure column (mutually exclusive) |
| `--maxiter` / `--tol` | poisson (100), nbreg (1000), both tol 1e-10 | — | IRLS/optimizer iterations and tolerance |
| `--nfactors` / `-r` | static, dynamic, gdfm (no short) | auto via IC | Factor counts |
| `--factor-lags` / `-p` | dynamic | `1` | Factor VAR lag order |
| `--method` | dynamic (`twostep\|qml`) | `twostep` | Factor estimation method |
| `--dynamic-rank` / `-q` | gdfm | auto | Dynamic rank |
| `--lags` / `-p` | var (auto), bvar (4), vecm (2), favar (2) | — | Lag orders |
| `--draws` / `-n` | bvar (2000), sv (5000) | — | MCMC draws |
| `--sampler` | bvar | `direct` | Sampler |
| `--config` (+ `--config-json`, `--set`, `--strict`) | bvar (prior), 3sls (equations+instruments, required), sur (equations, required), garch-midas (x_lf) | — | TOML configs |
| `--rank` / `-r` | vecm | `auto` | Cointegration rank |
| `--deterministic` | vecm | `constant` | `none`, `constant`, `trend` |
| `--factors` / `-r` | favar | — | Number of factors |
| `--key-vars` | favar | — | Key observed variables |
| `--indep` | preg, plogit, pprobit | — | Independent variables (comma-separated) |
| `--exog` / `--endog` / `--instruments` | piv | — | IV split; `--endog` required |
| `--id-col` / `--time-col` | panel ×4 | first/second column (piv: —) | Panel group / time columns |
| `--method` / `-m` | preg (`fe`), plogit/pprobit (`pooled`), piv (`fe`) | — | Panel estimation method |
| `--k-regimes` | ms, ms-ar | `2` | Number of regimes (≥ 2) |
| `--max-iter` | ms (500), ms-ar (1000) | — | Max EM iterations |
| `--tol` | ms | `1e-8` | EM convergence tolerance |
| `--no-switching-variance` (flag) | ms | off | Force common σ² (default: σ² switches) |
| `--switching-variance` (flag) | ms-ar | off | Let σ² switch (default: Hamilton constant-variance form) |
| `--column` / `-c` | ms-ar, setar, star, statespace, arima, sarima, arfima, all volatility | `1` | Column index |
| `--p` | ms-ar, setar, star (1), arima (auto), arfima (0), sarima (auto), vol pq (1) | — | AR/GARCH orders |
| `--d` | setar (`1`, String: int or `auto`), star (`1`), arima (`0`), sarima (`0` + `--P`/`--D`/`--Q`/`--s` 12) | — | Delay lag / differencing / seasonal orders |
| `--trim` | setar | `0.15` | Threshold-grid trimming fraction in (0, 0.5) |
| `--type` | star | `auto` | `lstr1`, `lstr2`, `estr`, `auto` |
| `--n-gamma` / `--n-c` | star | `15` / `15` | Grid points for γ / c start values (≥ 2) |
| `--transition-col` | star | `0` | External transition-variable column (0 = self-exciting y[t−d]) |
| `--q` | arima/auto, vol arch (1), vol pq (1) | — | MA/ARCH orders |
| `--method` / `-m` | arima, arfima, sarima | `css_mle`/`css`/`css_mle` | Time-series estimators (same choices as predict) |
| `--auto` (flag) | arima, sarima | off | Force automatic order selection |
| `--max-p`/`--max-q`/`--max-P`/`--max-Q` + `--criterion` | sarima | `2`/`2`/`1`/`1`, `aic` | Auto-search bounds and criterion |
| `--no-intercept` (flag) | sarima, 3sls, sur | off | Exclude intercept |
| `--max-iter` | arfima, sarima | `500` | Optimizer iterations |
| `--d0` | arfima (GPH), figarch/fiegarch (0.4) | — | Fractional-d starting value |
| `--truncation` / `--dist` | figarch, fiegarch | `1000` / `normal` | ARCH(∞) truncation; innovation distribution |
| `--fix-delta` / `--fix-gamma` | aparch | — | Fix power/asymmetry parameters |
| `--m-freq` / `--k` / `--rv` / `--span` | garch-midas | required/`12`/`realized`/`fixed` | HF-per-LF block, MIDAS lags, driver, span |
| `--instruments` | 3sls | `common` | `common`, `perequation` |
| `--iterate` (flag) | sur | off | Iterate feasible-GLS to convergence |
| `--kind` | statespace | `local-level` | `local-level`, `local-linear-trend` |
| `--init-mode` / `--kappa` | statespace | `kappa` / `1e6` | Diffuse initialisation; large-κ prior variance |
| `--standardized` (flag) | statespace | off | Standardized innovations v_t/√F_t (replaces raw v_t) |

# Examples

```bash
friedman residuals multivariate var :denmark --lags 2
friedman residuals univariate arima :nile --p 1 --d 1 --q 1
friedman residuals volatility garch :nile --p 1 --q 1
friedman residuals multivariate vecm :denmark --lags 2 --rank 1 --deterministic constant
friedman residuals regime setar :nile --p 1 --d auto
friedman residuals regime star :nile --p 1 --type lstr1
friedman residuals regime ms-ar :nile --p 1 --k-regimes 3
friedman residuals regime ms :stackloss --dep stack.loss --k-regimes 2
friedman residuals choice ologit :mroz --dep kidslt6 --kind deviance
friedman residuals regression statespace :nile --standardized
friedman residuals choice nbreg :mroz --dep kidslt6
```

# See also

* [In-Sample Fitted Values](predict.md) - fitted values from the same loop; `y − fitted` reproduces residuals on the linear leaves
* [Forecasting and Forecast Evaluation](forecast.md) - out-of-sample projections of the same models
* [Trend-Cycle Filters and Nowcasting](filter-nowcast.md) - filters and mixed-frequency nowcasts
