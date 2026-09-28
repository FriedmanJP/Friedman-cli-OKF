---
type: Feature
title: Data Simulation (DGPs with Population Truth)
description: The data simulate intermediate node with 21 DGP leaves emitting observables, truth, and settings.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/data.md
tags:
  - friedman-cli
  - data
  - simulation
  - dgp
  - monte-carlo
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:57:28Z
sources:
  - id: gen-data
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/data.md
    title: Generated data reference (flag surface and output tables)
  - id: guide-data
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/data.md
    title: data workflow guide (simulate semantics and DGP table)
  - id: src-data-sim
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/data_simulate.jl
    title: src/commands/data_simulate.jl leaf handlers
---

# Summary

`data simulate` is an intermediate node (not a leaf): its 21 sub-leaves each draw a sample plus the population that generated it. Every leaf emits the same three tables: `simulated_data` (observables an estimator would read; time series carry `time`, panels `id`/`time`, cross-sections `obs`), `population_truth` (parameters flattened to `parameter,row,col,value`; scalars have `row = col = 0`), and `simulation_settings` (`model`, effective `seed`, kind/distribution). Leaf `--seed 0` defers to the global `--seed`; with neither set the draw is `Xoshiro(0)`, so unseeded calls still reproduce. Structural shocks are not copied into the truth table (the seed reproduces them); conditional variances `h` are included for volatility leaves.

The DSGE-family leaves (`dsge`, `ha`, `olg`, `ct`) have no fixed DGP: they solve the model and call MEMs `simulate`. `--order` applies only to `dsge --method perturbation` (any other combination is `usage/invalid`); `ha --method krusell-smith` has no aggregate path (`usage/invalid`). Keep the `ct` solver grid at its default: coarsened grids have failed to converge on some platforms while passing on others.

# Functions

| Leaf | What it draws |
|---|---|
| `friedman data simulate var` | Reference stationary VAR(1); truth: `A_1`, `B0`, `Sigma`, `c` |
| `friedman data simulate svar` | Non-Gaussian SVAR, independent structural shocks (`--dist`, `--nu`) |
| `friedman data simulate heteroskedastic-var` | Heteroskedastic SVAR: Markov, GARCH, smooth, or break |
| `friedman data simulate arima` | Gaussian ARIMA, optional seasonal AR/MA left at zero |
| `friedman data simulate garch` | GARCH-family returns; `h` path in the truth table |
| `friedman data simulate sv` | Stochastic volatility (Gaussian, no leverage) |
| `friedman data simulate vecm` | Rank-1 VECM; truth: `alpha`, `beta`, `Gamma`, `Sigma` |
| `friedman data simulate cointreg` | Cointegrating regression; `--spurious` draws independent random walks |
| `friedman data simulate ardl` | ARDL(1,1); truth: `phi`, `beta`, long-run multiplier `theta` |
| `friedman data simulate factors` | Dynamic factor model (VAR factors, random loadings) |
| `friedman data simulate lp-iv` | Local-projection IV (instrument `z`, endogenous `s`, outcome `y`) |
| `friedman data simulate panel` | Linear or binary panel with optional correlated effects |
| `friedman data simulate pvar` | Panel VAR(1) with random effects |
| `friedman data simulate did` | Staggered adoption with realized ATT (`overall_att`, `att_e:`, `att_c:`) |
| `friedman data simulate gmm` | Heteroskedastic OLS or IV moments |
| `friedman data simulate regime` | Markov-switching, SETAR, LSTAR, or ESTAR |
| `friedman data simulate cross-section` | Cross-section DGP from OLS through RDD |
| `friedman data simulate dsge <model>` | Representative-agent path from solve + simulate (`.jl`/`.toml` spec) |
| `friedman data simulate ha <model>` | HA aggregate **deviations** (`ssj`/`reiter`); SS levels as `ss_agg:*`/`ss_price:*` |
| `friedman data simulate olg` | Blanchard perpetual-youth saddle path (deterministic; steady state as truth) |
| `friedman data simulate ct` | Continuous-time Aiyagari MIT transition after an initial TFP shock |

All 21 emit `simulated_data`, `population_truth`, `simulation_settings`. Shared options on every leaf: `--format, -f` (`table`), `--output, -o` (`""`), `--seed` (`0` = defer to global, else `Xoshiro(0)`). Only `dsge` and `ha` take a required `model` argument. Leaf-specific options:

| Leaf | Option | Default | Description |
|---|---|---|---|
| `var`, `vecm` | `--periods` / `--burn` | `200` / `50` | Sample length after burn-in / burn-in draws |
| `svar` | `--dist` / `--nu` | `t` / `5.0` | `gauss\|t\|laplace\|mixture\|skew`; t d.f. (> 2) |
| `heteroskedastic-var` | `--kind` | `markov` | `markov\|garch\|smooth\|external` |
| `arima` | `--phi` / `--theta` / `--diff` / `--sigma` / `--drift` | `0.5` / `""` / `0` / `1.0` / `0.0` | AR/MA csv lists, integration order, innov s.d., drift |
| `garch` | `--kind` | `garch` | `arch\|garch\|egarch\|gjr\|aparch\|igarch\|cgarch\|figarch\|fiegarch` |
| `sv` | `--mu` / `--phi` / `--sigma-eta` | `-0.5` / `0.95` / `0.2` | Log-var mean, persistence, vol-of-vol |
| `cointreg` | `--endog-rho` / `--sigma-u` / `--spurious` | `0.7` / `1.0` / off | Endogeneity corr, error scale, no-cointegration flag |
| `ardl` | `--phi` / `--beta0` / `--beta1` | `0.6` / `0.8` / `0.4` | Lag-DV, contemporaneous/lagged regressor coefs |
| `factors` | `--series` | `12` | Observed series N |
| `lp-iv` | `--pi1` / `--theta` | `1.5` / `1.0` | First-stage coef, impact response of y to s |
| `panel` | `--kind` / `--n` | `linear` / `30` | `linear\|logit\|probit`; cross-sectional units |
| `pvar` | `--n` / `--periods` | `15` / `20` | Units / sample length |
| `did` | `--n` / `--periods` | `80` / `20` | Units / sample length (cohorts at dates 6, 11, 16 in-sample) |
| `gmm` | `--kind` / `--n` / `--pi1` | `iv` / `200` / `1.0` | `ols\|iv`; obs; first-stage strength (iv) |
| `regime` | `--kind` | `ms` | `ms\|setar\|lstar\|estr` |
| `cross-section` | `--kind` / `--n` | `ols` / `200` | `ols\|hc\|cluster\|iv\|logit\|probit\|ordered\|mlogit\|poisson\|nb\|tobit\|truncreg\|heckman\|qreg\|rdd` |
| `dsge` | `--method` / `--order` / `--meas-sd` / `--periods` / `--burn` | `gensys` / `1` / `""` / `80` / `20` | `gensys\|klein\|blanchard-kahn\|perturbation\|projection\|pfi\|vfi`; order 1-3 (pert. only); meas-error s.d. |
| `ha` | `--method` / `--n-reduced` / `--distribution` / `--hh-solver` / `--periods` | `reiter` / `10` / `young` / `egm` / `20` | `ssj\|reiter`; reduced states; `young\|winberry`; `egm\|vfi` |
| `olg` | `--alpha` / `--beta` / `--delta` / `--gamma` / `--z` / `--debt` / `--k0` / `--periods` | `0.36` / `0.96` / `0.08` / `0.98` / `1.0` / `0.0` / `0.0` / `40` | Technology/preference params; `k0 = 0` means 0.8 x SS |
| `ct` | `--alpha` / `--rho` / `--sigma` / `--delta` / `--z` / `--shock-size` / `--grid-size` / `--a-max` / `--max-iter` / `--tol` / `--dt` / `--periods` | `0.36` / `0.05` / `2.0` / `0.05` / `1.0` / `0.95` / `40` / `30.0` / `80` / `1e-5` / `0.25` / `12` | Aiyagari params; impact TFP fraction; grid/solver settings |

`--periods`/`--burn` defaults vary slightly by leaf (garch 300/50, regime 200/40, factors 80/20, pvar 20/—, did 20/—, ct 12/—); the generated reference is authoritative per leaf.

# Examples

```bash
friedman data simulate var --periods 200 --burn 50 --seed 7 --format json
friedman data simulate arima --periods 200 --seed 7 --format json
friedman data simulate garch --periods 300 --seed 7 --format json
friedman data simulate did --n 80 --periods 20 --seed 7 -o did_demo
friedman data simulate cross-section --kind rdd --n 500 --seed 7
friedman data simulate dsge rbc.toml --method gensys --periods 80 --seed 7
friedman data simulate ha huggett --method reiter --periods 20 --seed 7
```

# See also

* [Handles and Examples](handles.md) - import simulated CSVs to typed handles
* [RA Core: Solve and Analyze](../dsge/core.md) - the DSGE solve behind `simulate dsge`
* [HA-DSGE](../dsge/hadsge.md) - the HA solve behind `simulate ha`
