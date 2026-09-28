---
type: Feature
title: Regression estimation
description: OLS/WLS, IV, GMM/SMM, SUR/3SLS, penalized, robust, censored, sample-selection, quantile, RDD, and nonparametric regression.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/estimate.md
tags:
  - estimate
  - regression
  - iv
  - gmm
  - penalized-regression
  - nonparametric
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:57:55Z
sources:
  - id: generated-estimate
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/estimate.md
    title: Generated estimate reference (option and output tables)
  - id: guide-estimate
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/estimate.md
    title: estimate guide (worked examples per leaf)
  - id: src-estimate
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/estimate.jl
    title: estimate command implementation
---

# Summary

These 22 leaves cover single-equation regression (`reg`, `iv`, `qreg`, `rdd`), moment-based estimation (`gmm`, `smm`), equation systems (`sur`, `3sls`), penalized fits (`lasso`, `ridge`, `elastic-net`), robust and limited-dependent-variable models (`robust`, `tobit`, `truncreg`, `heckman`), model selection (`select`), cointegrating regression (`cointreg`), state-space models (`statespace`), non-Gaussian SVAR identification by ML (`ml`), and nonparametric fits (`kde`, `kernel-reg`, `lowess`). Every leaf takes a required `data` CSV plus `--output`/`-o`, `--format`/`-f` (`table|csv|json`), `--save-model`; TOML-config leaves add `--config`/`--config-json`/`--set`/`--strict`.

Conventions worth knowing: `--dep` names the dependent column (default: first numeric column) and remaining numeric columns are regressors — no intercept is prepended unless the CSV has a `const` column (systems leaves prepend one per equation unless `--no-intercept`). Coefficient tables follow the C051 tidy format (`term|estimate|std_error|stat|p_value|ci_lower|ci_upper`) with a separate fit-statistics table. `regression ml` is maximum-likelihood non-Gaussian SVAR identification, not machine learning.

LEAVES open question (intermediates): `regression` is a CLI path segment only — no `##` header exists for it in the generated reference, so each `###` entry below is counted exactly once.

# Functions

## Linear, IV, and systems (6 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate regression reg` | OLS/WLS with HC/cluster/Conley covariances | `reg_coefficients`, `fit_statistics`, `conley_spatial_hac_settings` |
| `friedman estimate regression iv` | k-class IV (2SLS/LIML/Fuller/k-class) | `iv_coefficients`, `iv_diagnostics` |
| `friedman estimate regression gmm` | GMM with configurable weighting | `gmm_estimates`, `gmm_diagnostics` |
| `friedman estimate regression smm` | Simulated method of moments | `smm_estimates` |
| `friedman estimate regression sur` | Seemingly unrelated regressions (FGLS/MLE) | `sur_coefficients`, `sur_system_statistics` |
| `friedman estimate regression 3sls` | Three-stage least squares systems | `3sls_coefficients`, `3sls_system_statistics` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `reg` | `data` (required) | `--dep`, `--cov-type` (`hc1`: ols\|hc0\|hc1\|hc2\|hc3\|cluster\|conley), `--clusters`, `--weights` (WLS), `--lat`/`--lon`/`--dist-cutoff`/`--conley-kernel` (`bartlett`)/`--conley-metric` (`euclidean`)/`--time-col`/`--time-cutoff` (Conley spatial HAC) |
| `iv` | `data` (required) | `--dep`, `--endogenous` (required), `--instruments` (required excluded), `--cov-type` (`hc1`), `--method` (`tsls`: tsls\|liml\|fuller\|kclass), `--k` (k-class scalar), `--fuller-a` (1.0) |
| `gmm` | `data` (required) | `--config` (moments/instruments TOML), `--weighting`/`-w` (`twostep`: identity\|optimal\|twostep\|iterated) |
| `smm` | `data` (required) | `--config` (SMM spec TOML), `--weighting` (`two_step`: identity\|optimal\|two_step\|iterated), `--sim-ratio` (5), `--burn` (100) |
| `sur` | `data` (required) | `--config` (required [[equations]] TOML); flags `--iterate` (FGLS to MLE), `--no-intercept` |
| `3sls` | `data` (required) | `--config` (required [[equations]] + instruments TOML), `--instruments` (`common`: common\|perequation); flags `--no-intercept` |

## Penalized, robust, and limited dependent variables (7 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate regression lasso` | L1-penalized regression, CV/IC lambda | `lasso_coefficients`, `lasso_diagnostics` |
| `friedman estimate regression ridge` | L2-penalized regression | `ridge_coefficients`, `ridge_diagnostics` |
| `friedman estimate regression elastic-net` | L1/L2 mixing with alpha | `elastic_net_coefficients`, `elastic_net_diagnostics` |
| `friedman estimate regression robust` | M/MM-estimation (Huber/bisquare) | `robust_regression_coefficients`, `robust_regression_diagnostics` |
| `friedman estimate regression tobit` | Censored regression (two-sided bounds) | `tobit_coefficients`, `tobit_diagnostics` |
| `friedman estimate regression truncreg` | Truncated-normal regression | `truncated_regression_coefficients`, `truncated_regression_diagnostics` |
| `friedman estimate regression heckman` | Heckman selection (two-step/FIML) | `heckman_coefficients_outcome_selection`, `heckman_diagnostics` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `lasso` | `data` (required) | `--dep`, `--lambda` (`auto` or number), `--select` (`cv`: cv\|aic\|bic\|ebic) |
| `ridge` | `data` (required) | `--dep`, `--lambda` (`auto` or number), `--select` (`cv`: cv\|aic\|bic\|ebic) |
| `elastic-net` | `data` (required) | `--dep`, `--alpha` (0.5 in [0,1]), `--lambda` (`auto`), `--select` (`cv`) |
| `robust` | `data` (required) | `--dep`, `--psi` (`huber`: huber\|bisquare), `--method` (`m`: m\|mm) |
| `tobit` | `data` (required) | `--dep`, `--lower` (0.0), `--upper` (Inf) |
| `truncreg` | `data` (required) | `--dep`, `--lower` (0.0), `--upper` (Inf) |
| `heckman` | `data` (required) | `--dep`, `--select` (required 0/1 indicator), `--outcome-vars` (required), `--select-vars` (required), `--method` (`twostep`: twostep\|mle) |

## Quantile, RDD, selection, cointegration, state-space, ML-SVAR (6 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate regression qreg` | Quantile regression (Koenker-Bassett) | `quantile_regression_coefficients`, `quantile_fit_diagnostics` |
| `friedman estimate regression rdd` | Sharp/fuzzy RDD (Calonico-Cattaneo-Titiunik) | `rdd_treatment_effect`, `rdd_settings_diagnostics` |
| `friedman estimate regression select` | Stepwise/best-subset/GETS selection | `selected_model_coefficients`, `selection_path`, `selection_summary` |
| `friedman estimate regression cointreg` | FMOLS/CCR/DOLS cointegrating regression | `cointegrating_regression_coefficients`, `cointegrating_regression_diagnostics` |
| `friedman estimate regression statespace` | Local-level/trend or general state-space | `state_space_hyper_parameters`, `state_space_system_general`, `state_space_diagnostics` |
| `friedman estimate regression ml` | Non-Gaussian SVAR identification by ML | `structural_impact_matrix_b0`, `model_fit`, `parameter_estimates_with_standard_errors` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `qreg` | `data` (required) | `--dep`, `--tau` (`0.5`, single or comma-list), `--se` (`iid`: iid\|robust\|boot), `--n-boot` (500), `--alpha` (0.05) |
| `rdd` | `data` (required) | `--outcome`, `--running`, `--fuzzy` (fuzzy design), `--cutoff` (0.0), `--bandwidth`/`--bias-bandwidth` (0 = CCT auto), `--kernel` (`triangular`: triangular\|epanechnikov\|uniform), `--order` (1), `--level` (0.95) |
| `select` | `data` (required) | `--dep`, `--method` (`bidirectional`: forward\|backward\|bidirectional\|best-subset\|gets), `--criterion` (`pvalue`: pvalue\|aic\|bic), `--p-enter` (0.05), `--p-remove` (0.1), `--keep` (forced regressors) |
| `cointreg` | `data` (required) | `--dep`, `--method` (`fmols`: fmols\|ccr\|dols), `--trend` (`const`: none\|const\|linear), `--kernel` (`bartlett`: bartlett\|parzen\|qs\|tukey-hanning), `--bandwidth` (`andrews`), `--leads`/`--lags` (`auto`), `--ic` (`aic`: aic\|bic), `--dols-se` (`lrv`: lrv\|robust) |
| `statespace` | `data` (required) | `--column`/`-c` (1), `--model` (`local-level`: local-level\|local-linear-trend), `--init-mode` (`kappa`: kappa\|diffuse), `--kappa` (1e6), `--config` ([statespace] general-system TOML) |
| `ml` | `data` (required) | `--lags`/`-p` (auto AIC), `--distribution`/`-d` (`student_t`: student_t\|skew_t\|ghd\|mixture_normal\|pml\|skew_normal) |

## Nonparametric (3 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate regression kde` | Kernel density estimation | `kernel_density_estimate`, `kernel_density_diagnostics` |
| `friedman estimate regression kernel-reg` | Nadaraya-Watson/local-linear/local-poly | `kernel_regression_fit`, `kernel_regression_diagnostics` |
| `friedman estimate regression lowess` | LOWESS with robustifying passes | `lowess_fit`, `lowess_diagnostics` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `kde` | `data` (required) | `--column`/`-c` (1), `--kernel` (`gaussian`: gaussian\|epanechnikov\|triangular\|uniform), `--bw` (`silverman`: silverman\|sj\|number), `--npoints` (512), `--cut` (3.0) |
| `kernel-reg` | `data` (required) | `--dep`, `--indep` (required predictor), `--method` (`ll`: nw\|ll\|lp), `--degree` (1), `--bw` (`cv`: cv\|rot\|number), `--kernel` (`gaussian`) |
| `lowess` | `data` (required) | `--dep`, `--indep` (required predictor), `--frac` (0.6667), `--iter` (3) |

# Examples

```bash
friedman estimate regression reg :stackloss --dep=stack.loss --cov-type=hc1
friedman estimate regression iv iv.csv --dep=y --endogenous=x_endog --instruments=z1,z2
friedman estimate regression qreg q.csv --dep=y --tau=0.25,0.5,0.75 --se=boot
friedman estimate regression lasso pen.csv --dep=y --lambda=auto --select=cv
friedman estimate regression heckman sel.csv --dep=wage --select=employed --outcome-vars=educ,exper --select-vars=educ,exper,kids --method=twostep
friedman estimate regression cointreg :denmark --dep=LRM --method=fmols --trend=const
friedman estimate regression kde :nile --column=1 --kernel=gaussian --bw=silverman
```

# See also

* [Time-series and factor estimation](timeseries.md) - multivariate, univariate, and factor estimators
* [Panel and discrete choice](panel-choice.md) - panel and choice estimators
* [Regression diagnostics](../test/diagnostics.md) - White, influence, VIF, and Chow diagnostics for OLS fits
* [IV diagnostics](../test/panel-var.md) - weak-instrument and Anderson-Rubin inference
