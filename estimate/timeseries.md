---
type: Feature
title: Time-series and factor estimation
description: VAR, BVAR, VECM, SVAR/SVEC, local projections, TVP-VAR, MFVAR, ARIMA-family, ARDL/NARDL/MIDAS, and static/dynamic/GDFM/structural factor estimators.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/estimate.md
tags:
  - estimate
  - var
  - vecm
  - bvar
  - local-projections
  - arima
  - ardl
  - factor-models
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

These 20 leaves fit multivariate systems (VAR, BVAR, VECM, SVAR, SVEC, LP, TVP-VAR, MFVAR), univariate dynamics (ARIMA, SARIMA, ARFIMA, ARDL, NARDL, MIDAS), and factor structures (static, dynamic, GDFM, structural DFM, FastICA statistical identification). Every leaf takes a required `data` CSV path (a file or a bundled `:dataset` such as `:denmark`) and the shared flags `--output`/`-o`, `--format`/`-f` (`table|csv|json`), and `--save-model` (persist the fit to a `.jld2`/`.fmod` handle for `forecast`, `predict`, `irf`, `fevd`, `hd`); several leaves add `--plot`/`--plot-save`, and the TOML-config leaves add `--config`/`--config-json`/`--set`/`--strict`.

LEAVES open question (intermediates): the generated reference contains no `##` section headers for this file — `multivariate`, `univariate`, and `factor` are CLI path segments only, not leaves, so each `###` entry below is counted exactly once. LEAVES open question (inventory): `INVENTORY.md` heads this command as "~74" but its prose enumerates all 76 `estimate` leaves (naming `sarima` twice); no leaf is missing or extra.

# Functions

## Multivariate systems (9 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate multivariate var` | OLS VAR(p); `--lags` omitted selects via AIC | `var_coefficients`, `information_criteria` |
| `friedman estimate multivariate bvar` | Minnesota-prior BVAR with posterior sampling | `bvar_coefficients`, `minnesota_hyperparameters`, `information_criteria` |
| `friedman estimate multivariate vecm` | Johansen or Engle-Granger VECM, auto rank | `cointegrating_vectors_beta`, `adjustment_coefficients_alpha`, `information_criteria` |
| `friedman estimate multivariate svar` | AB-model SVAR, recursive to overidentified | `svar_a`, `svar_b`, `svar_summary` |
| `friedman estimate multivariate svec` | Structural VECM with long/short-run zeros | `svec_b0`, `svec_xi`, `svec_summary` |
| `friedman estimate multivariate lp` | Local projections, 6 methods incl. LP-IV | `lp_coefficients`, `lp_coefficients_expansion`, `lp_coefficients_recession`, `lp_estimation_summary`, `montiel_olea_pflueger_effective_f`, `lp_iv_anderson_rubin_bands` |
| `friedman estimate multivariate tvpvar` | TVP-VAR with stochastic volatility (Primiceri 2005) | `tvp_var_stochastic_volatility_path_posterior_sd_68_band`, `tvp_var_specification` |
| `friedman estimate multivariate mfvar` | Mixed-frequency VAR (Schorfheide-Song 2015) | `mf_var_latent_high_frequency_path_68_credible_band`, `mf_var_specification` |
| `friedman estimate multivariate favar` | Two-step or Bayesian factor-augmented VAR | `favar_coefficients`, `bayesian_favar` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `var` | `data` (required) | `--lags`/`-p` (auto AIC), `--trend` (`constant`: none\|constant\|trend\|both) |
| `bvar` | `data` (required) | `--lags`/`-p` (4), `--prior` (`minnesota`), `--draws`/`-n` (2000), `--sampler` (`direct`\|gibbs), `--method` (`mean`\|median), `--hyperopt` (`glp`\|grid), `--config` (prior hyperparameters) |
| `vecm` | `data` (required) | `--lags`/`-p` (2, in levels), `--rank`/`-r` (`auto`), `--deterministic` (`constant`: none\|constant\|trend), `--method` (`johansen`\|engle_granger), `--significance` (0.05) |
| `svar` | `data` (required) | `--lags`/`-p` (auto AIC), `--pattern` (`recursive`: recursive\|blanchard-quah\|a-model\|b-model\|ab-model), `--config` ([svar] A/B matrices), `--n-starts` (5), `--max-iter` (400) |
| `svec` | `data` (required) | `--lags`/`-p` (2), `--rank`/`-r` (`auto`), `--deterministic` (`constant`), `--method` (`johansen`\|engle_granger), `--significance` (0.05), `--config` ([svec] zero matrices), `--n-starts` (5), `--max-iter` (400) |
| `lp` | `data` (required) | `--method` (`standard`: standard\|iv\|smooth\|state\|propensity\|robust), `--shock` (1), `--horizons` (20), `--control-lags` (4), `--vcov` (`newey_west`: newey_west\|white\|driscoll_kraay), method-gated `--instruments`, `--knots`, `--lambda`, `--state-var`, `--gamma`, `--transition`, `--treatment`, `--score-method`, `--mop-tau`, `--mop-bandwidth`, `--ar-level`, `--ar-grid`, `--ar-span`; flags `--mop-f`, `--ar-bands` |
| `tvpvar` | `data` (required) | `--lags`/`-p` (2), `--draws`/`-n` (2000), `--burnin` (1000), `--thin` (1), `--n-train` (0), `--k-q` (0.01), `--k-s` (0.1), `--k-w` (0.01); flags `--no-tvp`, `--no-sv` |
| `mfvar` | `data` (required, high-frequency CSV with blanks) | `--lags`/`-p` (2), `--low-freq` (auto gap detection), `--freq-ratio` (3), `--aggregation` (`growth`: stock\|flow\|average\|growth), `--draws`/`-n` (1000), `--burnin` (500), `--prior` (`minnesota`\|diffuse) |
| `favar` | `data` (required) | `--factors`/`-r` (auto IC), `--lags`/`-p` (2), `--key-vars` (names/indices), `--method` (`two_step`\|bayesian), `--draws`/`-n` (5000, bayesian) |

## Univariate dynamics (6 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate univariate arima` | ARIMA with auto order selection | `arima_coefficients`, `information_criteria` |
| `friedman estimate univariate sarima` | Seasonal ARIMA, explicit or auto orders | `sarima_coefficients`, `information_criteria` |
| `friedman estimate univariate arfima` | Fractional integration, CSS or exact ML | `arfima_coefficients`, `arfima_diagnostics` |
| `friedman estimate univariate ardl` | ARDL with long-run multipliers, PSS case | `ardl_coefficients`, `ardl_long_run_coefficients`, `ardl_diagnostics` |
| `friedman estimate univariate nardl` | Asymmetric ARDL with cumulative multipliers | `nardl_coefficients`, `nardl_asymmetric_long_run_coefficients`, `nardl_diagnostics`, `nardl_cumulative_dynamic_multipliers`, `nardl_multipliers_summary` |
| `friedman estimate univariate midas` | Mixed-frequency MIDAS, 5 weight schemes | `midas_weight_curve`, `midas_coefficients`, `midas_diagnostics` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `arima` | `data` (required) | `--column`/`-c` (1), `--p` (auto), `--d` (0), `--q` (0), `--max-p`/`--max-d`/`--max-q` (5/2/5), `--criterion` (`bic`: aic\|bic), `--method`/`-m` (`css_mle`: ols\|css\|mle\|css_mle) |
| `sarima` | `data` (required) | `--column`/`-c` (1), `--p`/`--d`/`--q` (auto/0/0), `--P`/`--D`/`--Q` (0), `--s` (12), `--max-p`/`--max-q`/`--max-P`/`--max-Q` (2/2/1/1), `--criterion` (`aic`: aic\|bic), `--method` (`css_mle`: css_mle\|mle\|css), `--max-iter` (500); flags `--auto`, `--no-intercept` |
| `arfima` | `data` (required) | `--column`/`-c` (1), `--p` (0), `--q` (0), `--method`/`-m` (`css`: css\|mle), `--d0` (GPH pre-estimate), `--max-iter` (500) |
| `ardl` | `data` (required) | `--dep` (first numeric), `--p`/`--q` (`auto`), `--max-p`/`--max-q` (4), `--ic` (`aic`: aic\|bic), `--case` (3, PSS 1..5), `--trend` (`none`: none\|const\|trend) |
| `nardl` | `data` (required) | `--dep`, `--asymmetric` (`all` or 1-based indices), `--p`/`--q` (`auto`), `--max-p`/`--max-q` (4), `--ic` (`aic`: aic\|bic), `--case` (3), `--horizon` (12), `--nreps` (500), `--level` (0.95); flags `--no-bootstrap`, `--plot` |
| `midas` | `data` (required, low-frequency target CSV) | `--column` (1), `--hf-data` (required HF CSV), `--hf-column` (1), `--m` (required freq ratio), `--k` (required HF lags), `--weights` (`expalmon`: expalmon\|beta2\|beta3\|almon\|umidas), `--p-ar` (0), `--poly-degree` (2), `--horizon` (1), `--max-iter` (500) |

## Factor models (5 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate factor static` | Static PCA factors, IC auto-selection | `scree_data_eigenvalues_variance_shares`, `factor_loadings` |
| `friedman estimate factor dynamic` | Dynamic factor model, two-step or EM | `dynamic_factor_loadings` |
| `friedman estimate factor gdfm` | Generalized dynamic factor model (FHLR) | `gdfm_common_variance_shares` |
| `friedman estimate factor sdfm` | Structural DFM with shock identification | `sdfm_estimation_summary` |
| `friedman estimate factor fastica` | Statistical SVAR identification (ICA family) | `structural_impact_matrix_b0`, `structural_shocks` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `static` | `data` (required) | `--nfactors`/`-r` (auto IC), `--criterion` (`ic1`: ic1\|ic2\|ic3) |
| `dynamic` | `data` (required) | `--nfactors`/`-r` (auto), `--factor-lags`/`-p` (1), `--method` (`twostep`: twostep\|em) |
| `gdfm` | `data` (required) | `--nfactors`/`-r` (auto), `--dynamic-rank`/`-q` (auto), `--spectral` (`lag-window`: lag-window\|smoothed-periodogram) |
| `sdfm` | `data` (required) | `--factors`/`-q` (auto), `--id` (`cholesky`: cholesky\|sign\|proxy\|lewis-tvv\|sv-em\|gmm-moments), `--q-method` (`hallin-liska`: hallin-liska\|bai-ng\|amengual-watson), `--method` (`fglr`: fglr\|gdfm-var), `--spectral` (`lag-window`), `--instrument`, `--var-lags` (1), `--horizon` (40), `--config`, `--bandwidth` (0=auto), `--kernel` (`bartlett`: bartlett\|parzen\|quadratic_spectral) |
| `fastica` | `data` (required) | `--lags`/`-p` (auto AIC), `--method` (`fastica`: fastica\|jade\|sobi\|dcov\|hsic), `--contrast` (`logcosh`: logcosh\|exp\|kurtosis) |

# Examples

```bash
friedman estimate multivariate var :denmark
friedman estimate multivariate var :denmark --lags=2
friedman estimate multivariate bvar :denmark --lags=4 --draws=5000 --sampler=gibbs
friedman estimate multivariate vecm :denmark --lags=2 --rank=1 --deterministic=constant
friedman estimate multivariate lp :denmark --method=iv --shock=1 --horizons=20 --mop-f
friedman estimate univariate ardl ardl.csv --dep=y --p=1 --q=1 --case=3
friedman estimate univariate arima :nile --column=1 --p=1 --d=1 --q=1
friedman estimate univariate midas lf.csv --hf-data=hf.csv --m=3 --k=6 --weights=expalmon
friedman estimate factor static :denmark --nfactors=3
friedman estimate factor sdfm :denmark --factors=2 --id=cholesky --var-lags=1
```

# See also

* [Regime-switching and volatility](regime-volatility.md) - nonlinear time-series and volatility estimators
* [Regression](regression.md) - cross-section and systems regression estimators
* [Panel and discrete choice](panel-choice.md) - panel and choice estimators
* [Unit roots and long memory](../test/unit-root.md) - pre-estimation integration-order tests
* [Impulse responses](../impulse/irf.md) - structural IRFs from fitted multivariate models
