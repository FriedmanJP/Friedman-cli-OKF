---
type: Feature
title: Regression diagnostics
description: Serial correlation, heteroskedasticity, influence, distributional, nonlinearity, and discrete-choice specification tests.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/test.md
tags:
  - test
  - diagnostics
  - heteroskedasticity
  - serial-correlation
  - arch
  - specification
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:57:55Z
sources:
  - id: generated-test
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/test.md
    title: Generated test reference (option and output tables)
  - id: guide-test
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/test.md
    title: test guide (null hypotheses, decision logic, pitfalls)
  - id: src-test
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/test.jl
    title: test command implementation
---

# Summary

These 23 leaves diagnose fitted models: serial-correlation and white-noise tests (`ljung-box`, `box-pierce`, `bartlett-wn`, `durbin-watson`, `bds`), heteroskedasticity tests (`white`, `glejser`, `harvey`, `arch-lm`, `sign-bias`), heteroskedasticity-based SVAR identification (`heteroskedasticity`, `identifiability`), OLS influence and collinearity (`influence`, `vif`), distributional checks (`edf`, `normality`, `dispersion`, `fisher`), linearity tests (`hansen-linearity`, `star-linearity`), and choice-model specification (`brant`, `hausman-iia`).

Know which series each leaf tests: `ljung-box` squares the passed column first (always a variance test), while `box-pierce` tests the levels; `arch-lm`/`ljung-box` test the column directly with no model fit, while `sign-bias` first fits the `--model` GARCH and tests its standardized residuals. The OLS-family leaves fit like `estimate regression reg` (`--dep` plus all other numeric columns, no prepended intercept; `--cov-type` forwarded). `test serial breusch-pagan` is the panel random-effects LM test, not a heteroskedasticity test — it lives in [panel-var.md](panel-var.md). Most leaves here accept `--result`/`--save-result`; the exceptions are `arch-lm`, `sign-bias`, `identifiability`, and `vif`.

LEAVES open question (intermediates): `serial` is a CLI path segment only — no `##` header exists for it in the generated reference, so each `###` entry below is counted exactly once.

# Functions

## Serial correlation and white noise (5 leaves)

| Command | H0 | Output tables |
|---|---|---|
| `friedman test serial ljung-box` | no serial correlation in squares | `ljung_box_squared_test` |
| `friedman test serial box-pierce` | no autocorrelation to `--lags` | `box_pierce_test` |
| `friedman test serial bartlett-wn` | white noise | `bartlett_white_noise_test` |
| `friedman test serial durbin-watson` | no AR(1) | `durbin_watson_test` |
| `friedman test serial bds` | iid (per embedding dimension) | `bds_test` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `ljung-box` | `data` (required) | `--column`/`-c` (1), `--lags`/`-p` (10) |
| `box-pierce` | `data` (required) | `--column`/`-c` (1), `--lags`/`-p` (20) |
| `bartlett-wn` | `data` (required) | `--column`/`-c` (1) |
| `durbin-watson` | `data` (required) | `--column`/`-c` (1) |
| `bds` | `data` (required) | `--column`/`-c` (1), `--max-dim` (6), `--eps-frac` (0.7) |

## Heteroskedasticity (5 leaves + 2 SVAR leaves)

| Command | H0 / role | Output tables |
|---|---|---|
| `friedman test serial white` | homoskedasticity | `white_test` |
| `friedman test serial glejser` | homoskedasticity | `glejser_test` |
| `friedman test serial harvey` | homoskedasticity (multiplicative) | `harvey_test` |
| `friedman test serial arch-lm` | no ARCH effects | `arch_lm_test` |
| `friedman test serial sign-bias` | no remaining asymmetry (Engle-Ng) | `sign_bias_test` |
| `friedman test serial heteroskedasticity` | B0 from variance-regime changes | `structural_impact_matrix_b0` |
| `friedman test identifiability` | non-Gaussian SVAR pre-checks | `identifiability_test_results` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `white` | `data` (required) | `--dep`, `--cov-type` (`hc1`); flag `--no-cross-terms` |
| `glejser` | `data` (required) | `--dep`, `--cov-type` (`hc1`) |
| `harvey` | `data` (required) | `--dep`, `--cov-type` (`hc1`) |
| `arch-lm` | `data` (required) | `--column`/`-c` (1), `--lags`/`-p` (4); no `--result`/`--save-result` |
| `sign-bias` | `data` (required) | `--column`/`-c` (1), `--model` (`garch`: garch\|egarch\|gjr-garch), `--p`/`--q` (1); no `--result`/`--save-result` |
| `heteroskedasticity` | `data` (required) | `--lags`/`-p` (auto AIC), `--method` (`markov`: markov\|garch\|smooth_transition\|external), `--config` (transition/regime vars), `--regimes` (2) |
| `identifiability` | `data` (required) | `--lags`/`-p` (auto AIC), `--test`/`-t` (`all`: strength\|gaussianity\|independence\|overidentification\|lambda-distinct\|gaussian-count\|label-stability\|all), `--method` (`fastica`: fastica\|jade\|sobi\|dcov\|hsic), `--contrast` (`logcosh`: logcosh\|exp\|kurtosis), `--n-bootstrap` (999); no `--result`/`--save-result` |

## Influence, distributional, and linearity (9 leaves)

| Command | H0 / role | Output tables |
|---|---|---|
| `friedman test influence` | per-observation leverage and influence | `influence_diagnostics`, `influence_summary` |
| `friedman test vif` | VIF and tolerance per regressor | `variance_inflation_factors` |
| `friedman test edf` | series follows `--dist` | `edf_test` |
| `friedman test normality` | Gaussian VAR residuals (suite) | `normality_tests_for_var_residuals` |
| `friedman test dispersion` | equidispersion (Cameron-Trivedi) | `overdispersion_test_cameron_trivedi_1990`, `dispersion_summary` |
| `friedman test fisher` | white noise (periodicity) | `fisher_s_test` |
| `friedman test hansen-linearity` | linearity vs SETAR | `hansen_1996_linearity_test` |
| `friedman test star-linearity` | linearity vs STAR (LM3) | `star_linearity_test_lm3` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `influence` | `data` (required) | `--dep`, `--cov-type` (`hc1`) |
| `vif` | `data` (required) | `--dep`, `--cov-type` (`hc1`); no `--result`/`--save-result` |
| `edf` | `data` (required) | `--column`/`-c` (1), `--dist` (`normal`: normal\|exponential\|logistic\|gumbel\|gamma\|weibull\|chisq), `--test` (`ad`: ks\|lilliefors\|cvm\|ad\|watson), `--params` (`estimate`: estimate\|specified), `--theta` (required with `specified`) |
| `normality` | `data` (required) | `--lags`/`-p` (auto AIC) |
| `dispersion` | `data` (required) | `--dep`, `--offset`/`--exposure`, `--cov-type` (`robust`), `--clusters`, `--maxiter` (100), `--tol` (1e-10), `--alpha` (0.05) |
| `fisher` | `data` (required) | `--column`/`-c` (1) |
| `hansen-linearity` | `data` (required) | `--column`/`-c` (1), `--p` (1), `--d` (1), `--trim` (0.15), `--reps` (1000) |
| `star-linearity` | `data` (required) | `--column`/`-c` (1), `--p` (1), `--d` (1), `--transition-col` (0 = self-exciting) |

## Discrete-choice specification (2 leaves)

| Command | H0 | Output tables |
|---|---|---|
| `friedman test brant` | proportional odds | `brant_test` |
| `friedman test hausman-iia` | IIA for the omitted category | `hausman_mcfadden_iia_test` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `brant` | `data` (required) | `--dep`, `--cov-type` (`hc1`) |
| `hausman-iia` | `data` (required) | `--dep`, `--omit-category` (default: last) |

# Examples

```bash
friedman test serial white :stackloss --dep=stack.loss
friedman test serial white :stackloss --dep=stack.loss --no-cross-terms
friedman test serial arch-lm :gnp_hamilton --column=1 --lags=4
friedman test serial ljung-box :gnp_hamilton --column=1 --lags=10
friedman test serial sign-bias :gnp_hamilton --column=1 --model=garch
friedman test influence :stackloss --dep=stack.loss
friedman test vif :stackloss --dep=stack.loss
friedman test hansen-linearity :nile --p=1 --d=1
friedman test star-linearity :nile --p=1 --d=1
friedman test dispersion sim_counts.csv --dep=y
```

# See also

* [Cointegration and stability](cointegration.md) - Chow, CUSUM, and Nyblom stability tests
* [Panel, VAR, IV, and DiD tests](panel-var.md) - Breusch-Pagan panel LM and VAR diagnostics
* [Regression estimation](../estimate/regression.md) - the OLS fits under diagnosis
* [Regime-switching estimation](../estimate/regime-volatility.md) - where linearity rejection leads
