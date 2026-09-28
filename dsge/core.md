---
type: Feature
title: DSGE Core (Solve, Determinacy, IRF, FEVD, HD, Estimation)
description: Representative-agent DSGE steady state, 7-method solution, determinacy maps, simulation, innovation accounting, and estimation.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/dsge.md
tags:
  - friedman-cli
  - dsge
  - gensys
  - perturbation
  - irf
  - estimation
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
    title: dsge workflow guide (model formats, solve, analysis leaves)
  - id: src-dsge
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/dsge.jl
    title: src/commands/dsge.jl leaf handlers
---

# Summary

Representative-agent DSGE from a `.toml` or `.jl` model file (auto-detected by extension; anything else is `usage/invalid-option`). TOML carries `[model]` (`endogenous`, `exogenous`, `parameters`, `[[model.equations]]` in `var[t]` form); a `.jl` file must evaluate to an RA `ModelSpec` (typically `@dsge begin ... end`, evaluated in a sandbox with MEMs exports in scope). A file evaluating to an agent-kind spec is `usage/wrong-command` — run it under `hadsge` or the matching `dsge` family command instead. An `E[t]` expectation wrapping `(...)` is `config/invalid`; write the `x[t+1]` lead directly (it means `E_t x_{t+1}`).

Seven solution methods (`gensys`, `klein`, `blanchard-kahn`, `perturbation` orders 1-3, `projection`, `pfi`, `vfi`) are shared by `solve`, `irf`, `fevd`, `hd`, and `simulate`; `solve` adds OccBin constraints (`--constraints` TOML, optional `--constraint-solver` backend). `determinacy-map` needs a `--config` TOML with a `[determinacy]` section (REQUIRED). `estimate` is GMM-style (`irf_matching`, `likelihood`, `bayesian`, `smm`); full Bayesian work lives under `dsge bayes`.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman dsge steady-state <model>` | Deterministic steady state (+ OccBin steady state) | `dsge_steady_state` |
| `friedman dsge solve <model>` | Solve by one of 7 methods (+ OccBin path) | `dsge_solution`, `perturbation_policy_gx`, `projection_solution`, `projection_diagnostics`, `vfi_value_*`, `determinacy_verdict`, `dsge_occbin_solution` |
| `friedman dsge determinacy-map <model>` | 1-2 parameter determinacy sweep | `dsge_determinacy_map`, `determinacy_region_summary`, `determinacy_boundary` |
| `friedman dsge simulate <model>` | Stochastic simulation (burn-in dropped) | `dsge_simulation` |
| `friedman dsge irf <model>` | Analytical (or simulation-based / OccBin) IRFs | `dsge_irf_*` (per shock), `occbin_irf_*` (per variable) |
| `friedman dsge fevd <model>` | h-step (or unconditional order>=2) FEVD | `dsge_fevd_*` (per variable) |
| `friedman dsge hd <model>` | Kalman-smoother historical decomposition | `dsge_historical_decomposition_*` (per shock) |
| `friedman dsge moments <model>` | Theoretical moments from a perturbation solution | `dsge_theoretical_moments`, `variance_covariance`, `autocovariances` |
| `friedman dsge perfect-foresight <model>` | Newton deterministic transition path | `perfect_foresight_path` |
| `friedman dsge estimate <model>` | GMM-style parameter estimation | `dsge_estimation` |

All ten take a required `model` argument (path to `.toml`/`.jl`). Every leaf accepts `--format, -f` (`table`) and `--output, -o` (`""`).

Shared solver options (`solve`, `irf`, `fevd`, `hd`, `simulate`):

| Option | Default | Description |
|---|---|---|
| `--method` | `gensys` | `gensys\|klein\|perturbation\|projection\|pfi\|vfi\|blanchard-kahn` |
| `--order` | `1` | Perturbation order 1-3 |
| `--degree` | `5` | Polynomial degree (projection/pfi/vfi) |
| `--grid` | `auto` | `auto\|chebyshev\|smolyak` (vfi: `auto\|tensor\|smolyak`) |
| `--next-state` | `""` | VFI `auto\|linear\|residual`; PFI `linear\|policy\|nonlinear` |
| `--howard-steps` | `-1` | Howard steps (vfi dflt 20, pfi 0; -1 = method default) |
| `--n-grid` / `--n-choice` | `0` | VFI tensor nodes/state (>=3; 0 = 12) / line-search points (0 = 41) |
| `--optimizer` | `""` | VFI maximizer `auto\|grid1d\|fminbox-nm\|fminbox-lbfgs` |
| `--smolyak-mu` | `""` | VFI Smolyak level (unset = 2) |
| `--n-quad` / `--scale` / `--tol` / `--max-iter` / `--damping` / `--anderson-m` | `0` | VFI/PFI numerics (0 = upstream defaults: 5 / 3.0 / 1e-8 / 500 / 1.0 / 0) |

Leaf-specific options beyond those:

| Leaf | Option | Default | Description |
|---|---|---|---|
| `steady-state` | `--constraints` / `--constraint-solver` | `""` | OccBin constraints TOML / backend (`nonlinearsolve\|optim\|nlopt\|ipopt\|path`) |
| `solve` | `--evaluate-at` | `""` | State vector `x1,x2,...` for VFI value evaluation |
| `solve` | `--constraints` / `--constraint-solver` / `--periods` | `""` / `""` / `40` | OccBin constraints TOML / backend / simulation periods |
| `solve` | `--save-model` / `--plot` / `--plot-save` | `""` / off | Save handle / browser plot / save HTML |
| `determinacy-map` | `--config` | `""` (REQUIRED) | TOML with `[determinacy]` (params, lower/upper/points or grids) |
| `determinacy-map` | `--rank-rtol` | `1e-8` | Sims rank-test relative tolerance |
| `determinacy-map` | `--threaded` / `--verbose-solver` / `--plot` / `--plot-save` | off | Threaded sweep / keep solver warnings / plot / save HTML |
| `simulate` | `--periods` / `--burn` / `--seed` | `200` / `100` / `0` | Periods after burn-in / burn-in / seed (0 = none) |
| `simulate` | `--antithetic` / `--plot` / `--plot-save` | off | Antithetic sampling / plot / save HTML |
| `irf` | `--horizon` / `--shock-size` / `--n-sim` | `40` / `1.0` / `0` | Horizon / size in std devs / sim draws (0 = analytical) |
| `irf` | `--constraints` / `--plot` / `--plot-save` | `""` / off | OccBin TOML / plot / save HTML |
| `fevd` | `--horizon` / `--unconditional` | `40` / off | Horizon / asymptotic FEVD (order >= 2 perturbation) |
| `fevd` | `--plot` / `--plot-save` | off | Plot / save HTML |
| `hd` | `--data, -d` / `--observables` / `--states` | `""` / `""` / `observables` | CSV data / observable names / `observables\|all` |
| `hd` | `--measurement-error` | `""` | Meas-error s.d. (csv) or `auto` |
| `hd` | `--plot` / `--plot-save` | off | Plot / save HTML |
| `moments` | `--method` / `--order` / `--lags` | `perturbation` / `2` / `1` | Needs PerturbationSolution; order 1-3; autocov lags >= 1 |
| `perfect-foresight` | `--shocks` / `--constraints` / `--constraint-solver` | `""` | Shock-sequence CSV / constraints TOML / backend |
| `perfect-foresight` | `--periods` / `--sparsity` / `--max-iter` / `--tol` | `100` / `auto` / `100` / `1e-8` | Periods / jacobian `auto\|dense` / Newton iters / tol |
| `perfect-foresight` | `--plot` / `--plot-save` | off | Plot / save HTML |
| `estimate` | `--data, -d` / `--params` | `""` | CSV data / comma-separated parameter names |
| `estimate` | `--method` | `irf_matching` | `irf_matching\|likelihood\|bayesian\|smm` |
| `estimate` | `--solve-method` / `--solve-order` | `gensys` / `1` | Solution method / perturbation order |
| `estimate` | `--weighting` / `--irf-horizon` / `--var-lags` / `--sim-ratio` / `--bounds` | `optimal` / `20` / `4` / `5` / `""` | `identity\|optimal\|diagonal` / IRF horizon / VAR lags / SMM sim ratio / bounds TOML |

# Examples

```bash
cat > rbc.toml <<'EOF'
[model]
parameters = { rho = 0.9, sigma = 0.01 }
endogenous = ["Y", "C"]
exogenous = ["e"]
linear = true
[[model.equations]]
expr = "Y[t] = rho * Y[t-1] + sigma * e[t]"
[[model.equations]]
expr = "C[t] = Y[t]"
EOF
friedman dsge steady-state rbc.toml
friedman dsge solve rbc.toml --method=perturbation --order=2
friedman dsge irf rbc.toml --horizon 40
friedman dsge fevd rbc.toml --horizon 40
friedman dsge simulate rbc.toml --periods 200 --burn 100 --seed 7
friedman dsge moments rbc.toml --order 2 --lags 4
friedman dsge determinacy-map rbc.toml --config det.toml
friedman dsge estimate rbc.toml --data obs.csv --params rho,sigma --method irf_matching
friedman dsge perfect-foresight rbc.toml --shocks shocks.csv --periods 100
```

# See also

* [Bayesian DSGE](bayes.md) - full posterior workflow on the same model files
* [Structured Family Models](family.md) - bank, CT, DCEGM, firm, OLG nodes
* [HA-DSGE](hadsge.md) - one-household heterogeneous-agent models
