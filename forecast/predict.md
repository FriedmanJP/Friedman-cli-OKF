---
type: Feature
title: In-Sample Fitted Values
description: What each fitted model implies for the estimation sample — conditional means, variances, state paths, and per-category probabilities across 38 leaves.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/predict.md
tags: [predict, fitted-values, in-sample, conditional-mean, marginal-effects]
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:58:15Z
sources:
  - id: generated-predict
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/predict.md
    title: Generated predict reference (options, defaults, output tables)
  - id: predict-guide
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/predict_residuals.md
    title: predict/residuals narrative guide (supported models, semantics, examples)
  - id: fitted-src
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/fitted.jl
    title: Fitted-values command implementation (23-kind loop + hand-written specs)
---

# Summary

Thirty-eight leaves return what a fitted model implies for the estimation sample — conditional means, conditional variances, state paths, or per-category probabilities — completing the fit–diagnose loop (`estimate` fits, `predict` implies, `residuals` leaves unexplained). Every leaf re-estimates from the `data` CSV or reuses a `--model` handle (pass stems without suffix: `--model var`, never `--model var.jld2`); stdout carries data only, diagnostics go to stderr. Implementation shape (LEAVES.md open question 5, confirmed in `src/commands/fitted.jl`): a 23-entry `FITTED_MODEL_KINDS` table (var, bvar, arima, vecm, static, dynamic, gdfm, arch, garch, egarch, gjr-garch, sv, favar, reg, logit, probit, preg, piv, plogit, pprobit, ologit, oprobit, mlogit) is expanded by `_specs_for_verb` into both verbs — 23 of the 38 predict leaves — while 15 leaves carry hand-written specs because their option sets diverge from the loop (sarima, poisson, nbreg, ms-ar, ms, statespace, sur, 3sls, arfima, plus the six extended-GARCH variants igarch/cgarch/aparch/figarch/fiegarch/garch-midas, which are not in the shared volatility table). The generated reference groups leaves under family intermediates (`choice`, `factor`, `multivariate`, `panel`, `regime`, `regression`, `univariate`, `volatility`) for display; each `###` leaf below is covered exactly once. Asymmetries to note: `predict` exists for the Markov-switching models only (`ms`, `ms-ar`) — SETAR/STAR have `residuals` leaves but no `predict` leaf because upstream exposes no fitted values for `ThresholdModel`/`STARModel`; the plain volatility leaves refit at Gaussian-QMLE defaults with no `--dist` option; `--marginal-effects`/`--odds-ratio`/`--classification-table` on binary choice are bare mutually-exclusive flags that replace the fitted-values output.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman predict choice logit` | Binary logit fitted probabilities + optional AMEs / odds ratios / classification | `logit_fitted_probabilities`; `average_marginal_effects_logit` (`--marginal-effects`); `odds_ratios_logit` (`--odds-ratio`); `classification_metrics` + `confusion_matrix` (`--classification-table`, at `--threshold`) |
| `friedman predict choice probit` | Binary probit fitted probabilities + optional AMEs / classification (no odds ratios) | `probit_fitted_probabilities`; `average_marginal_effects_probit`; `classification_metrics`; `confusion_matrix` |
| `friedman predict choice ologit` | Ordered-logit per-category probabilities (+ per-category AMEs) | `ordered_logit_predicted_probabilities` (`prob_<cat>` per row); `ordered_logit_average_marginal_effects` (`--marginal-effects`; delta-method SEs, no z/p) |
| `friedman predict choice oprobit` | Ordered-probit per-category probabilities (+ per-category AMEs) | `ordered_probit_predicted_probabilities`; `ordered_probit_average_marginal_effects` |
| `friedman predict choice mlogit` | Multinomial-logit per-alternative probabilities (+ per-alternative AMEs) | `multinomial_logit_predicted_probabilities`; `multinomial_logit_average_marginal_effects` |
| `friedman predict choice poisson` | Poisson conditional means exp(x'β + offset) | `poisson_conditional_means` (`observation \| fitted`) |
| `friedman predict choice nbreg` | Negative-binomial conditional means | `negative_binomial_conditional_means` |
| `friedman predict factor static` | Static-factor common component, one column per series | `static_factor_common_component` |
| `friedman predict factor dynamic` | Dynamic-factor common component | `dynamic_factor_common_component` |
| `friedman predict factor gdfm` | GDFM common component | `gdfm_common_component` |
| `friedman predict multivariate var` | VAR fitted values (auto lags when omitted) | `var_predictions` (one column per variable) |
| `friedman predict multivariate bvar` | BVAR fitted values at the posterior mean | `bvar_predictions` |
| `friedman predict multivariate vecm` | VECM fitted values via the VAR representation | `vecm_predictions` |
| `friedman predict multivariate favar` | FAVAR fitted values | `favar_predictions` (factors + observed variables) |
| `friedman predict panel preg` | Panel regression fitted values (default `--method fe`) | `panel_regression_fitted_values` |
| `friedman predict panel piv` | Panel IV (2SLS) fitted values; `--endog` hard-required | `panel_iv_fitted_values` |
| `friedman predict panel plogit` | Panel logit fitted probabilities (default `--method pooled`) | `panel_logit_fitted_probabilities` |
| `friedman predict panel pprobit` | Panel probit fitted probabilities (default `--method pooled`; no FE estimator exists) | `panel_probit_fitted_probabilities` |
| `friedman predict regime ms` | MS-regression regime-weighted conditional mean Σₖ Pr(s=k)·E[y\|s=k]; `--probs smoothed` (default; `y − fitted` reproduces residuals) or `filtered` | `ms_regression_fitted_values` (`t \| fitted`) |
| `friedman predict regime ms-ar` | MS-AR regime-weighted conditional mean; Hamilton constant-variance default | `ms_ar_fitted_values` |
| `friedman predict regression reg` | OLS/WLS fitted values | `reg_fitted_values` |
| `friedman predict regression statespace` | Kalman state paths, tidy long `period \| state \| filtered \| smoothed` (model via `--kind`, not `--model`) | `state_space_state_paths` |
| `friedman predict regression sur` | SUR per-equation fitted values, tidy long `equation \| t \| fitted`; `--config` required | `sur_fitted_values_per_equation` |
| `friedman predict regression 3sls` | 3SLS per-equation fitted values, tidy long; `--config` required | `3sls_fitted_values_per_equation` |
| `friedman predict univariate arima` | ARIMA fitted values (auto selection when `--p` omitted or `--auto`) | `arima_predictions` |
| `friedman predict univariate sarima` | SARIMA fitted values | `sarima_predictions` |
| `friedman predict univariate arfima` | ARFIMA fitted values | `arfima_predictions` |
| `friedman predict volatility arch` | ARCH conditional variance + implied volatility | `arch_conditional_variance` |
| `friedman predict volatility garch` | GARCH conditional variance + implied volatility | `garch_conditional_variance` |
| `friedman predict volatility egarch` | EGARCH conditional variance + implied volatility | `egarch_conditional_variance` |
| `friedman predict volatility gjr-garch` | GJR-GARCH conditional variance + implied volatility | `gjr_garch_conditional_variance` |
| `friedman predict volatility igarch` | IGARCH conditional variance + implied volatility | `igarch_conditional_variance` |
| `friedman predict volatility cgarch` | Component-GARCH conditional variance + implied volatility | `cgarch_conditional_variance` |
| `friedman predict volatility aparch` | APARCH conditional variance + implied volatility | `aparch_conditional_variance` |
| `friedman predict volatility figarch` | FIGARCH conditional variance + implied volatility | `figarch_conditional_variance` |
| `friedman predict volatility fiegarch` | FIEGARCH conditional variance + implied volatility | `fiegarch_conditional_variance` |
| `friedman predict volatility garch-midas` | GARCH-MIDAS conditional variance + implied volatility; `--m-freq` required | `garch_midas_conditional_variance` |
| `friedman predict volatility sv` | Posterior-mean SV path (variance + volatility) per period | `sv_conditional_variance` |

Every leaf takes the `data` CSV positional plus `--format`/`-f`, `--output`/`-o`, and `--model` (saved-model handle, skips re-estimation):

| Option / Flag | Leaves | Default | Description |
|---|---|---|---|
| `--dep` | choice ×7, panel ×4, reg, ms | first numeric | Dependent variable column name |
| `--cov-type` | logit/probit/ologit/oprobit/mlogit (hc1; `ols\|hc0-hc3\|cluster`), poisson (`robust\|mle\|hc0-hc3\|cluster`), reg (hc1), panel (cluster; `ols\|cluster\|twoway\|driscoll-kraay`) | — | Covariance estimator |
| `--clusters` | binary/ordered/multinomial choice, poisson, reg | — | Cluster variable column name |
| `--weights` | reg | — | Weights column (WLS) |
| `--threshold` | logit, probit | `0.5` | Classification threshold |
| `--marginal-effects` (flag) | logit, probit, ologit, oprobit, mlogit | off | Average marginal effects (replaces fitted values on binary; appends per-category on ordered/multinomial) |
| `--odds-ratio` (flag) | logit only | off | Odds ratios (replaces fitted values) |
| `--classification-table` (flag) | logit, probit | off | Classification metrics + confusion matrix (replaces fitted values) |
| `--offset` / `--exposure` | poisson, nbreg | — | Log-scale offset / strictly-positive exposure column (mutually exclusive) |
| `--maxiter` / `--tol` | poisson (100), nbreg (1000), both tol 1e-10 | — | IRLS/optimizer iterations and convergence tolerance |
| `--nfactors` / `-r` | static, dynamic, gdfm (`--nfactors` no short) | auto via IC | Factor counts |
| `--factor-lags` / `-p` | dynamic | `1` | Factor VAR lag order |
| `--method` | dynamic (`twostep\|qml`) | `twostep` | Factor estimation method |
| `--dynamic-rank` / `-q` | gdfm | auto | Dynamic rank |
| `--lags` / `-p` | var (auto), bvar (4), vecm (2), favar (2) | — | Lag orders |
| `--draws` / `-n` | bvar (2000), sv (5000) | — | MCMC draws |
| `--sampler` | bvar | `direct` | Sampler |
| `--config` (+ `--config-json`, `--set`, `--strict`) | bvar (prior), 3sls (equations+instruments, required), sur (equations, required), garch-midas (x_lf for `--rv macro`) | — | TOML configs |
| `--rank` / `-r` | vecm | `auto` | Cointegration rank |
| `--deterministic` | vecm | `constant` | `none`, `constant`, `trend` |
| `--factors` / `-r` | favar | — | Number of factors |
| `--key-vars` | favar | — | Key observed variables |
| `--indep` | preg, plogit, pprobit | — | Independent variables (comma-separated) |
| `--exog` / `--endog` / `--instruments` | piv | — | IV split (mirrors `estimate panel piv`; `--endog` required) |
| `--id-col` / `--time-col` | panel ×4 | first/second column (piv: —) | Panel group / time columns |
| `--method` / `-m` | preg (`fe`), plogit/pprobit (`pooled`), piv (`fe`; `fe\|re\|fd\|hausman-taylor`) | — | Panel estimation method |
| `--k-regimes` | ms, ms-ar | `2` | Number of regimes (≥ 2) |
| `--max-iter` | ms (500), ms-ar (1000) | — | Max EM iterations |
| `--tol` | ms | `1e-8` | EM convergence tolerance |
| `--probs` | ms, ms-ar | `smoothed` | Regime weighting: `smoothed` or `filtered` |
| `--no-switching-variance` (flag) | ms | off | Force common σ² (default: σ² switches) |
| `--switching-variance` (flag) | ms-ar | off | Let σ² switch (default: Hamilton constant-variance form) |
| `--instruments` | 3sls | `common` | Instrument mode: `common`, `perequation` |
| `--no-intercept` (flag) | 3sls, sur | off | Do not add an intercept per equation |
| `--iterate` (flag) | sur | off | Iterate feasible-GLS to convergence |
| `--column` / `-c` | statespace, arima, sarima, arfima, all volatility | `1` | Column index |
| `--kind` | statespace | `local-level` | `local-level`, `local-linear-trend` |
| `--init-mode` / `--kappa` | statespace | `kappa` / `1e6` | Diffuse initialisation; large-κ prior variance |
| `--state` | statespace | `both` | `filtered`, `smoothed`, `both` |
| `--p` / `--d` / `--q` | arima (auto/`0`/`0`), arfima (`0`/—/`0`), sarima (auto/`0`/`0` + `--P`/`--D`/`--Q`/`--s` 12), vol pq (1/1), arch (`--q` 1), ms-ar (`--p` 1) | — | AR/differencing/MA and GARCH/ARCH orders |
| `--method` / `-m` | arima (`ols\|css\|mle\|css_mle`), arfima (`css\|mle`), sarima (`css_mle\|mle\|css`) | — | Time-series estimators |
| `--auto` (flag) | arima, sarima | off | Force automatic order selection |
| `--max-p`/`--max-q`/`--max-P`/`--max-Q` + `--criterion` | sarima | `2`/`2`/`1`/`1`, `aic` | Auto-search bounds and criterion |
| `--no-intercept` (flag) | sarima | off | Exclude intercept |
| `--max-iter` | arfima, sarima | `500` | Optimizer iterations |
| `--d0` | arfima (GPH), figarch/fiegarch (0.4) | — | Fractional-d starting value |
| `--truncation` / `--dist` | figarch, fiegarch | `1000` / `normal` | ARCH(∞) truncation; innovation distribution |
| `--fix-delta` / `--fix-gamma` | aparch | — | Fix power/asymmetry parameters |
| `--m-freq` / `--k` / `--rv` / `--span` | garch-midas | required/`12`/`realized`/`fixed` | HF-per-LF block, MIDAS lags, driver, span |

# Examples

```bash
friedman predict regression reg :stackloss --dep stack.loss
friedman predict multivariate var :denmark --lags 2
friedman predict univariate arima :nile --p 1 --d 1 --q 1
friedman predict volatility garch :nile --p 1 --q 1
friedman predict multivariate vecm :denmark --lags 2 --rank 1 --deterministic constant
friedman predict choice logit :mroz --dep kidslt6 --marginal-effects
friedman predict regression statespace :nile --kind local-linear-trend
friedman predict regime ms-ar :nile --p 1 --probs filtered
friedman predict choice poisson :mroz --dep kidslt6
```

# See also

* [Model Residuals](residuals.md) - the matching residual vector per leaf; SETAR/STAR exist only there
* [Forecasting and Forecast Evaluation](forecast.md) - out-of-sample projections of the same models
* [Trend-Cycle Filters and Nowcasting](filter-nowcast.md) - filters and mixed-frequency nowcasts
