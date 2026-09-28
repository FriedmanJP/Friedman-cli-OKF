---
type: Feature
title: Bayesian DSGE Estimation and Diagnostics
description: The dsge bayes intermediate node with 15 leaves for posterior estimation, analysis, and checks.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/dsge.md
tags:
  - friedman-cli
  - dsge
  - bayesian
  - smc
  - mcmc
  - identification
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:57:28Z
sources:
  - id: gen-dsge
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/dsge.md
    title: Generated dsge reference (flag surface and output tables)
  - id: guide-dsge
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/dsge.md
    title: dsge workflow guide (Bayesian DSGE section, priors TOML)
  - id: src-dsge
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/dsge.jl
    title: src/commands/dsge.jl leaf handlers
---

# Summary

`dsge bayes` is an intermediate node (not a leaf): its 15 sub-leaves re-estimate the posterior and then analyze it. All sampling leaves share the `BAYES_OPTIONS` set: `--data, -d` (CSV), `--params` (comma-separated names), `--priors` (priors TOML path), `--sampler` (`smc` default, `smc2`, `mh`), `--n-smc` (5000), `--n-particles` (500, smc2), `--n-draws`/`--burnin` (10000/5000), `--ess-target` (0.5), `--observables`, `--solver` (`gensys`/`klein`/`perturbation`), `--order` (1-3), `--constraint-solver`, `--prefilter` (`none`/`demean`/`first-difference`/`linear-detrend`/`hp`, the Dynare prefilter; `--hp-lambda` 1600 quarterly), `--measurement-error` (`none`/`auto`/csv), `--delayed-acceptance` (MH flag), plus `--format`/`--output`. Priors live in a TOML file with a `[priors]` section. Non-sampling leaves (`identification`, `posterior-mode`, `prior-predictive`) take a subset: no `--data`/`--sampler` where no posterior is drawn.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman dsge bayes estimate <model>` | Posterior draws via smc/smc2/mh | `bayesian_dsge_posterior` |
| `friedman dsge bayes summary <model>` | Posterior moments + prior-vs-posterior | `bayesian_dsge_posterior_summary`, `prior_vs_posterior_comparison` |
| `friedman dsge bayes irf <model>` | Posterior-mean IRFs | `bayesian_dsge_irf_*` (per shock) |
| `friedman dsge bayes fevd <model>` | Posterior-mean FEVD | `bayesian_dsge_fevd_*` (per variable) |
| `friedman dsge bayes hd <model>` | Posterior-mean HD with quantiles | `bayesian_dsge_historical_decomposition_*` (per shock) |
| `friedman dsge bayes simulate <model>` | Posterior-mean simulated path | `bayesian_dsge_simulation` |
| `friedman dsge bayes predictive <model>` | Posterior predictive simulations | `posterior_predictive_summary` |
| `friedman dsge bayes prior-predictive <model>` | Prior predictive distribution (no data) | `prior_predictive_distribution`, `prior_predictive_summary` |
| `friedman dsge bayes compare <model>` | Two-model comparison via log marginal likelihood | `bayesian_model_comparison` |
| `friedman dsge bayes marginal-lik <model>` | Bridge-sampling + SMC log marginal likelihood | `marginal_likelihood_bridge_sampling` |
| `friedman dsge bayes posterior-mode <model>` | Posterior mode + Laplace log ML (no sampling) | `posterior_mode`, `posterior_mode_diagnostics` |
| `friedman dsge bayes mcmc-diag <model>` | R-hat, bulk/tail ESS, Geweke | `mcmc_convergence_diagnostics`, `mcmc_diagnostics_summary` |
| `friedman dsge bayes identification <model>` | Iskrev rank identification test (no sampling) | `identification_diagnostics`, `singular_values` |
| `friedman dsge bayes learning-rate <model>` | Koop-Pesaran-Smith learning rate on nested subsamples | `learning_rate_check`, `learning_rate_summary` |
| `friedman dsge bayes overlap <model>` | Prior/posterior overlap weak-identification flags | `prior_posterior_overlap`, `overlap_summary` |

All 15 take a required `model` argument. Leaf-specific options beyond `BAYES_OPTIONS`:

| Leaf | Option | Default | Description |
|---|---|---|---|
| `estimate` | `--save-model` | `""` | Save fitted model to a handle |
| `irf` / `fevd` | `--horizon` | `40` | Response / decomposition horizon |
| `irf` / `fevd` | `--plot` / `--plot-save` | off | Browser plot / save HTML |
| `hd` | `--horizon` / `--n-hd-draws` / `--quantiles` | `40` / `200` / `0.16,0.5,0.84` | Horizon / posterior draws / quantile levels |
| `hd` | `--mode-only` / `--plot` / `--plot-save` | off | Posterior mode only / plot / save HTML |
| `simulate` | `--periods` / `--plot` / `--plot-save` | `200` / off | Simulation periods / plot / save HTML |
| `predictive` | `--n-sim` / `--periods` | `500` / `100` | Predictive simulations / periods each |
| `predictive` | `--plot` / `--plot-save` | off | Plot / save HTML |
| `prior-predictive` | `--periods` / `--n-draws` | `200` / `10000` | Periods per draw / prior draws (no `--data`/`--sampler`) |
| `compare` | `--model2` / `--params2` / `--priors2` | `""` | Second model file / params / priors TOML |
| `marginal-lik` | `--proposal` / `--df` | `normal` / `5.0` | Bridge proposal `normal\|t` / t d.f. |
| `posterior-mode` | `--max-iter` / `--f-reltol` | `500` / `1e-8` | Optimizer iterations (>= 1) / rel tol (> 0); no sampling flags |
| `identification` | `--n-lags` | `2` | Autocovariance lags in the Iskrev moment vector; `--params` required |
| `learning-rate` | `--fractions` / `--threshold` / `--refit-n-smc` | `0.5,1.0` / `0.2` / `100` | Nested subsample fractions / flag threshold / SMC particles per refit |
| `overlap` | `--threshold` / `--n-grid` | `0.8` / `0` | Overlap flag threshold / histogram bins (0 = auto) |

# Examples

```bash
friedman dsge bayes estimate rbc.toml --data obs.csv --params rho,sigma --priors priors.toml --observables Y,C --sampler smc --n-smc 500
friedman dsge bayes summary rbc.toml --data obs.csv --params rho,sigma --priors priors.toml
friedman dsge bayes irf rbc.toml --data obs.csv --params rho,sigma --priors priors.toml --horizon 40
friedman dsge bayes identification rbc.toml --params rho,sigma --observables Y,C
friedman dsge bayes posterior-mode rbc.toml --data obs.csv --params rho,sigma --priors priors.toml --observables Y,C
friedman dsge bayes compare rbc.toml --data obs.csv --params rho --priors priors.toml --model2 alt.toml --params2 rho --priors2 priors.toml
friedman dsge bayes prior-predictive rbc.toml --params rho,sigma --priors priors.toml --periods 200
```

# See also

* [RA Core: Solve and Analyze](core.md) - point-solution and GMM estimation leaves
* [HA-DSGE](hadsge.md) - Bayesian estimation of heterogeneous-agent models
