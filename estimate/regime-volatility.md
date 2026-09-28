---
type: Feature
title: Regime-switching and volatility estimation
description: Threshold, SETAR, STAR, Markov-switching, TVP, ARCH/GARCH-family, multivariate GARCH, and stochastic-volatility estimators.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/estimate.md
tags:
  - estimate
  - regime-switching
  - threshold
  - markov-switching
  - garch
  - stochastic-volatility
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

These 20 leaves fit nonlinear conditional-mean models (threshold regression, SETAR, STAR, Markov-switching regression and autoregression, TVP regression) and conditional-variance models (ARCH, GARCH, EGARCH, GJR-GARCH, IGARCH, CGARCH, APARCH, FIGARCH, FIEGARCH, GARCH-MIDAS, CCC/DCC/BEKK, stochastic volatility). Every leaf takes a required `data` CSV path plus the shared `--output`/`-o`, `--format`/`-f` (`table|csv|json`), and `--save-model` flags; most regime and several volatility leaves add `--plot`/`--plot-save`. The `setar`/`threshold` leaves attach a Hansen (1996) linearity test unless `--no-linearity` is passed.

LEAVES open question (intermediates): `regime` and `volatility` are CLI path segments only — the generated reference has no `##` headers for them, so each `###` entry below is counted exactly once.

# Functions

## Regime-switching (6 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate regime threshold` | Cross-section threshold regression, Hansen CI | `threshold_regression_coefficients`, `threshold_regression_diagnostics` |
| `friedman estimate regime setar` | Self-exciting TAR with linearity test | `setar_coefficients`, `setar_diagnostics` |
| `friedman estimate regime star` | Smooth-transition AR (LSTR1/LSTR2/ESTR/auto) | `star_regime_coefficients`, `star_transition_parameters`, `star_diagnostics` |
| `friedman estimate regime ms-ar` | Markov-switching AR (Hamilton form default) | `ms_ar_regime_coefficients`, `ms_ar_regime_variances`, `ms_ar_transition_matrix`, `ms_ar_regime_probabilities`, `ms_ar_diagnostics` |
| `friedman estimate regime ms` | K-state Markov-switching regression | `ms_regression_regime_coefficients`, `ms_regression_regime_variances`, `ms_regression_transition_matrix`, `ms_regression_regime_probabilities`, `ms_regression_diagnostics` |
| `friedman estimate regime tvp` | Kalman-filter TVP regression | `tvp_hyper_parameters`, `tvp_coefficient_paths`, `tvp_diagnostics` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `threshold` | `data` (required) | `--dep` (first numeric), `--threshold-col` (required splitter), `--trim` (0.15), `--reps` (1000), `--ci-level` (0.95: 0.90\|0.95\|0.99); flags `--het`, `--no-linearity` |
| `setar` | `data` (required) | `--column`/`-c` (1), `--p` (1), `--d` (`1` or `auto`), `--trim` (0.15), `--reps` (1000), `--ci-level` (0.95); flags `--het`, `--no-linearity` |
| `star` | `data` (required) | `--column`/`-c` (1), `--p` (1), `--d` (1), `--type` (`auto`: lstr1\|lstr2\|estr\|auto), `--n-gamma`/`--n-c` (15), `--transition-col` (0 = self-exciting) |
| `ms-ar` | `data` (required) | `--column`/`-c` (1), `--p` (1), `--k-regimes` (2), `--max-iter` (1000); flag `--switching-variance` (default off) |
| `ms` | `data` (required) | `--dep` (first numeric), `--k-regimes` (2), `--max-iter` (500), `--tol` (1e-8); flag `--no-switching-variance` (default: variance switches) |
| `tvp` | `data` (required) | `--dep` (first numeric), `--init-mode` (`kappa`: kappa\|diffuse), `--kappa` (1e6); flag `--no-intercept` (default: time-varying intercept included) |

## Univariate volatility (11 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate volatility arch` | ARCH(q) | `arch_coefficients` |
| `friedman estimate volatility garch` | GARCH(p,q), normal/Student/GED | `garch_coefficients`, `conditional_distribution` |
| `friedman estimate volatility egarch` | EGARCH with leverage, 3 distributions | `egarch_coefficients`, `conditional_distribution` |
| `friedman estimate volatility gjr-garch` | GJR-GARCH asymmetry, 3 distributions | `gjr_garch_coefficients`, `conditional_distribution` |
| `friedman estimate volatility igarch` | Integrated GARCH | `igarch_coefficients`, `igarch_diagnostics` |
| `friedman estimate volatility cgarch` | Component GARCH (permanent/transitory) | `cgarch_coefficients`, `cgarch_diagnostics` |
| `friedman estimate volatility aparch` | Asymmetric power ARCH (est. delta/gamma) | `aparch_coefficients`, `aparch_diagnostics` |
| `friedman estimate volatility figarch` | Fractionally integrated GARCH | `figarch_coefficients`, `figarch_diagnostics` |
| `friedman estimate volatility fiegarch` | Fractionally integrated EGARCH | `fiegarch_coefficients`, `fiegarch_diagnostics` |
| `friedman estimate volatility garch-midas` | GARCH-MIDAS two-frequency variance | `garch_midas_coefficients`, `garch_midas_diagnostics` |
| `friedman estimate volatility sv` | MCMC stochastic volatility | `sv_coefficients` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `arch` | `data` (required) | `--column`/`-c` (1), `--q` (1) |
| `garch` | `data` (required) | `--column`/`-c` (1), `--p`/`--q` (1), `--dist` (`normal`: normal\|student\|ged) |
| `egarch` | `data` (required) | `--column`/`-c` (1), `--p`/`--q` (1), `--dist` (`normal`: normal\|student\|ged) |
| `gjr-garch` | `data` (required) | `--column`/`-c` (1), `--p`/`--q` (1), `--dist` (`normal`: normal\|student\|ged) |
| `igarch` | `data` (required) | `--column`/`-c` (1), `--p`/`--q` (1) |
| `cgarch` | `data` (required) | `--column`/`-c` (1) |
| `aparch` | `data` (required) | `--column`/`-c` (1), `--p`/`--q` (1), `--fix-delta`/`--fix-gamma` (pin power/asymmetry; default estimates) |
| `figarch` | `data` (required) | `--column`/`-c` (1), `--p`/`--q` (1), `--d0` (0.4), `--truncation` (1000), `--dist` (`normal`) |
| `fiegarch` | `data` (required) | `--column`/`-c` (1), `--p`/`--q` (1), `--d0` (0.4), `--truncation` (1000), `--dist` (`normal`) |
| `garch-midas` | `data` (required) | `--column`/`-c` (1), `--m-freq` (required HF-per-block), `--k` (12), `--rv` (`realized`: realized\|macro), `--span` (`fixed`: fixed\|rolling), `--config` ([garch_midas] x_lf, required for `--rv macro`) |
| `sv` | `data` (required) | `--column`/`-c` (1), `--draws`/`-n` (5000) |

## Multivariate volatility (3 leaves)

| Command | Description | Output tables |
|---|---|---|
| `friedman estimate volatility ccc` | Constant conditional correlation GARCH | `ccc_garch_conditional_correlation`, `ccc_garch_diagnostics` |
| `friedman estimate volatility dcc` | Dynamic conditional correlation (cDCC option) | `dcc_garch_conditional_correlation`, `dcc_garch_dynamics_parameters`, `dcc_garch_diagnostics` |
| `friedman estimate volatility bekk` | Scalar/diagonal BEKK(1,1) | `bekk_conditional_correlation`, `bekk_dynamics_parameters`, `bekk_diagnostics` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `ccc` | `data` (required) | `--p`/`--q` (1, univariate-margin orders) |
| `dcc` | `data` (required) | `--p`/`--q` (1), `--correction` (`none`: none\|aielli) |
| `bekk` | `data` (required) | `--kind` (`scalar`: scalar\|diagonal) |

# Examples

```bash
friedman estimate regime setar :nile --column=1 --p=1 --d=1
friedman estimate regime star :nile --column=1 --p=1 --type=auto
friedman estimate regime ms-ar :gnp_hamilton --column=1 --p=2 --k-regimes=2
friedman estimate regime threshold thr.csv --dep=y --threshold-col=z --trim=0.15
friedman estimate volatility garch :nile --column=1 --p=1 --q=1
friedman estimate volatility egarch :nile --column=1 --dist=student
friedman estimate volatility garch-midas ret.csv --m-freq=22 --k=12 --rv=realized
friedman estimate volatility dcc retpanel.csv --p=1 --q=1 --correction=aielli
friedman estimate volatility sv :nile --column=1 --draws=5000
```

# See also

* [Time-series and factor estimation](timeseries.md) - multivariate, univariate, and factor estimators
* [Regression](regression.md) - cross-section and systems regression estimators
* [Regression diagnostics](../test/diagnostics.md) - ARCH-LM, sign-bias, and Nyblom volatility diagnostics
* [Linearity tests](../test/diagnostics.md) - Hansen and STAR linearity pre-tests for regime models
