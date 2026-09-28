---
type: Feature
title: Panel and discrete-choice estimation
description: Panel regression, IV, ARDL, VAR, cointegrating regression, and binary/ordered/multinomial/count choice models.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/estimate.md
tags:
  - estimate
  - panel
  - discrete-choice
  - logit
  - probit
  - count-data
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

These 14 leaves fit panel estimators (`preg`, `piv`, `plogit`, `pprobit`, `pmg`, `pvar`, `xtcointreg`) and discrete-choice models (`logit`, `probit`, `ologit`, `oprobit`, `mlogit`, `poisson`, `nbreg`). Every leaf takes a required `data` CSV plus `--output`/`-o`, `--format`/`-f` (`table|csv|json`), `--save-model`. Panel leaves read long-format panels with `--id-col`/`--time-col` (defaulting to the first/second columns); choice leaves default `--dep` to the first numeric column. `preg` supports Arellano-Bond/Blundell-Bond GMM (`--method ab|bb`) and high-dimensional fixed effects (`--absorb`); `poisson`/`nbreg` share the `--offset`/`--exposure` and `--irr` incidence-rate-ratio surface.

LEAVES open question (intermediates): `panel` and `choice` are CLI path segments only — no `##` headers exist for them in the generated reference, so each `###` entry below is counted exactly once.

# Functions

## Panel (7 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate panel preg` | Panel OLS incl. AB/BB GMM and HDFE | `panel_regression_coefficients`, `model_statistics`, `dynamic_panel_diagnostics`, `hdfe_absorption` |
| `friedman estimate panel piv` | Panel IV (FE/RE/FD/Hausman-Taylor) | `panel_iv_coefficients`, `weak_instrument_diagnostics` |
| `friedman estimate panel plogit` | Panel logit | `panel_logit_coefficients`, `model_statistics` |
| `friedman estimate panel pprobit` | Panel probit | `panel_probit_coefficients`, `model_statistics` |
| `friedman estimate panel pmg` | Panel ARDL: PMG/MG/DFE | `panel_ardl_long_run_coefficients`, `panel_ardl_short_run_ec_coefficients`, `panel_ardl_diagnostics` |
| `friedman estimate panel pvar` | GMM panel VAR | `panel_var_coefficients`, `panel_summary` |
| `friedman estimate panel xtcointreg` | Panel FMOLS/DOLS cointegrating regression | `panel_cointegrating_regression_coefficients`, `panel_cointegrating_regression_diagnostics` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `preg` | `data` (required, long panel) | `--dep`, `--indep`, `--id-col`, `--time-col`, `--cov-type` (`cluster`: ols\|cluster\|twoway\|driscoll-kraay\|pcse), `--method`/`-m` (`fe`), `--ar1` (`none`: none\|common\|panel-specific), `--pcse-unbalanced` (`casewise`), `--absorb` (HDFE dims, fe only), `--hdfe-tol` (1e-8), `--hdfe-maxiter` (1000), `--min-lag-endo` (2), `--max-lag-endo` (99); flags `--twoway`, `--collapse` |
| `piv` | `data` (required, long panel) | `--dep`, `--exog`, `--endog`, `--instruments`, `--method`/`-m` (`fe`: fe\|re\|fd\|hausman-taylor), `--cov-type` (`cluster`: ols\|cluster\|twoway\|driscoll-kraay), `--id-col`, `--time-col` |
| `plogit` | `data` (required, long panel) | `--dep`, `--indep`, `--id-col`, `--time-col`, `--cov-type` (`cluster`: ols\|cluster\|twoway\|driscoll-kraay), `--method`/`-m` (`pooled`) |
| `pprobit` | `data` (required, long panel) | `--dep`, `--indep`, `--id-col`, `--time-col`, `--cov-type` (`cluster`), `--method`/`-m` (`pooled`) |
| `pmg` | `data` (required) | `--id-col`, `--time-col`, `--dep`, `--indep`, `--method` (`pmg`: pmg\|mg\|dfe), `--trend` (`constant`: none\|constant\|trend), `--p` (1), `--q` (1), `--maxiter` (100), `--tol` (1e-8) |
| `pvar` | `data` (required, long panel) | `--id-col`/`--time-col` (required), `--lags`/`-p` (1), `--dependent`, `--predet`, `--exog`, `--transformation` (`fd`: fd\|fod), `--steps` (`twostep`: onestep\|twostep), `--method` (`gmm`: gmm\|feols), `--min-lag-endo` (2), `--max-lag-endo` (99); flags `--system`, `--collapse` |
| `xtcointreg` | `data` (required) | `--id-col`, `--time-col`, `--dep`, `--indep`, `--method` (`fmols`: fmols\|dols), `--pooling` (`group`: group\|pooled), `--trend` (`const`: none\|const\|linear), `--kernel` (`bartlett`: bartlett\|parzen\|qs\|tukey-hanning), `--bandwidth` (`andrews`: andrews\|nw94\|lag), `--leads`/`--lags` (`auto`), `--ic` (`aic`: aic\|bic), `--dols-se` (`lrv`: lrv\|robust) |

## Discrete choice (7 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate choice logit` | Binary logit (IRLS) | `logit_regression_coefficients`, `fit_statistics` |
| `friedman estimate choice probit` | Binary probit (IRLS) | `probit_regression_coefficients`, `fit_statistics` |
| `friedman estimate choice ologit` | Ordered logit with cutpoints | `ordered_logit_coefficients`, `cutpoints`, `fit_statistics` |
| `friedman estimate choice oprobit` | Ordered probit with cutpoints | `ordered_probit_coefficients`, `cutpoints`, `fit_statistics` |
| `friedman estimate choice mlogit` | Multinomial logit, tidy by alternative | `multinomial_logit_coefficients`, `fit_statistics` |
| `friedman estimate choice poisson` | Poisson QMLE with robust default | `poisson_regression_coefficients`, `incidence_rate_ratios`, `fit_statistics` |
| `friedman estimate choice nbreg` | Negative-binomial (NB2) with dispersion | `negative_binomial_regression_coefficients`, `overdispersion_parameter`, `incidence_rate_ratios`, `fit_statistics` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `logit` | `data` (required) | `--dep`, `--cov-type` (`hc1`: ols\|hc0\|hc1\|hc2\|hc3\|cluster), `--clusters`, `--maxiter` (100), `--tol` (1e-8) |
| `probit` | `data` (required) | `--dep`, `--cov-type` (`hc1`), `--clusters`, `--maxiter` (100), `--tol` (1e-8) |
| `ologit` | `data` (required) | `--dep`, `--cov-type` (`hc1`), `--clusters` |
| `oprobit` | `data` (required) | `--dep`, `--cov-type` (`hc1`), `--clusters` |
| `mlogit` | `data` (required) | `--dep`, `--cov-type` (`ols`: ols\|hc0\|hc1\|hc2\|hc3) |
| `poisson` | `data` (required) | `--dep`, `--offset`/`--exposure` (exclusive), `--cov-type` (`robust`: robust\|mle\|hc0\|hc1\|hc2\|hc3\|cluster), `--clusters`, `--maxiter` (100), `--tol` (1e-10), `--conf-level` (0.95); flag `--irr` |
| `nbreg` | `data` (required) | `--dep`, `--offset`/`--exposure` (exclusive), `--maxiter` (1000), `--tol` (1e-10), `--conf-level` (0.95); flag `--irr` |

# Examples

```bash
friedman estimate panel preg panel.csv --dep=y --indep=x1,x2 --id-col=id --time-col=time
friedman estimate panel pvar panel.csv --id-col=id --time-col=time --lags=1 --dependent=y,x1
friedman estimate panel pmg panel.csv --dep=y --indep=x1,x2 --method=pmg --p=1 --q=1
friedman estimate choice logit choice.csv --dep=voted --cov-type=hc1
friedman estimate choice mlogit choice.csv --dep=mode
friedman estimate choice poisson counts.csv --dep=visits --exposure=days --irr
friedman estimate choice nbreg counts.csv --dep=visits --irr
```

# See also

* [Regression](regression.md) - cross-section and systems regression estimators
* [Time-series and factor estimation](timeseries.md) - multivariate, univariate, and factor estimators
* [Panel, VAR, IV, and DiD tests](../test/panel-var.md) - Hausman, F-FE, and PVAR specification tests
* [Regression diagnostics](../test/diagnostics.md) - Brant, Hausman-IIA, and dispersion choice-model tests
