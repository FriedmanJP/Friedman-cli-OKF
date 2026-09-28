---
type: Feature
title: HA-DSGE (One-Household Heterogeneous-Agent Models)
description: hadsge steady state, SSJ/Reiter/Krusell-Smith solution, aggregate and distributional IRFs, and estimation.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/hadsge.md
tags:
  - friedman-cli
  - hadsge
  - heterogeneous-agents
  - ssj
  - reiter
  - krusell-smith
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:57:28Z
sources:
  - id: gen-hadsge
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/hadsge.md
    title: Generated hadsge reference (flag surface and output tables)
  - id: guide-hadsge
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/ha-dsge.md
    title: HA-DSGE workflow guide (builtins, method choice, pitfalls)
  - id: src-hadsge
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/hadsge.jl
    title: src/commands/hadsge.jl leaf handlers
---

# Summary

One-household HA-DSGE (promoted from `dsge ha`) over builtins `huggett` (start here), `krusell-smith`, `one-asset-hank`, `two-asset-hank`, `endogenous-labor` (leading `:` accepted), or a `.jl` file evaluating to a heterogeneous-agent `ModelSpec` (an RA spec is `usage/wrong-command`, the mirror of the RA loader rule). All 11 leaves take a required `model` argument and share `--hh-solver` (`egm` default; SSJ is EGM-only; not with krusell-smith), `--distribution` (`young`/`winberry`), `--format`/`--output`. Method choice: `ssj` (sequence-space Jacobians; default for `solve`), `reiter` (linearized distribution + aggregates; the only method with distribution/inequality IRFs), `krusell-smith` (PLM fixed point; no linear IRF path). Set the asset grid upper bound generously: mass piling at `a_max` breaks market clearing invisibly (MEMs warns on stderr).

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman hadsge steady-state <model>` | Stationary equilibrium + Euler accuracy | `ha_steady_state_aggregates`, `ha_steady_state_prices`, `ha_steady_state_diagnostics`, `ha_euler_accuracy_log10_by_convention` |
| `friedman hadsge solve <model>` | Solve via ssj/reiter/krusell-smith | `ha_dsge_solve_diagnostics`, `krusell_smith_plm_coefficients`, steady-state tables |
| `friedman hadsge irf <model>` | Aggregate IRFs (ssj/reiter) | `ha_dsge_irf_*` (per shock) |
| `friedman hadsge fevd <model>` | Aggregate FEVD (ssj/reiter) | `ha_dsge_fevd_*` (per variable) |
| `friedman hadsge hd <model>` | Historical decomposition of aggregates | `ha_historical_decomposition_*` (per shock) |
| `friedman hadsge simulate <model>` | Aggregate paths from linearized solution | `ha_dsge_simulation` |
| `friedman hadsge simulate-panel <model>` | Individual asset holdings from SS policies | `ha_panel_simulation_summary` |
| `friedman hadsge distribution-irf <model>` | Wealth-distribution IRF (Reiter only) | `ha_distribution_irf` |
| `friedman hadsge inequality-irf <model>` | Gini and wealth-percentile IRFs (Reiter only) | `ha_inequality_irf` |
| `friedman hadsge accuracy <model>` | Den Haan (2010) PLM accuracy test | `den_haan_accuracy`, `reference_vs_plm_only_aggregate_path`, `den_haan_simulation_settings` |
| `friedman hadsge estimate <model>` | Bayesian HA estimation (MH/SMC) | `ha_dsge_bayesian_posterior`, `ha_dsge_bayesian_settings` |

Leaf options beyond the shared `--hh-solver`/`--distribution`/`--format`/`--output`:

| Leaf | Option | Default | Description |
|---|---|---|---|
| `steady-state` | `--euler-points` | `midpoints` | Euler-error points: `midpoints\|nodes` |
| `steady-state` | `--max-iter` / `--tol` | `0` / `0.0` | GE iters / clearing tol (0 = upstream default) |
| `steady-state` | `--save-model` | `""` | Save handle |
| `solve` | `--method` | `ssj` | `ssj\|reiter\|krusell-smith` |
| `solve` | `--n-reduced` / `--t-horizon` | `30` / `300` | Reduced states (SSJ/Reiter) / sequence horizon (SSJ) |
| `solve` | `--save-model` | `""` | Save handle |
| `irf` | `--method` / `--horizon` / `--n-reduced` | `reiter` / `40` / `30` | `ssj\|reiter` / horizon / reduced states |
| `irf` | `--plot` / `--plot-save` | off | Browser plot / save HTML |
| `fevd` | `--method` / `--horizon` / `--n-reduced` | `reiter` / `40` / `30` | `ssj\|reiter` / horizon / reduced states |
| `fevd` | `--plot` / `--plot-save` | off | Browser plot / save HTML |
| `hd` | `--method` / `--data, -d` / `--observables` | `ssj` / `""` / `""` | `ssj\|reiter` / CSV levels / aggregates (ss.aggregates/ss.prices keys) |
| `hd` | `--measurement-error` / `--n-reduced` / `--t-horizon` | `""` / `30` / `300` | s.d. csv or `auto` / reduced states / SSJ horizon |
| `hd` | `--plot` / `--plot-save` | off | Browser plot / save HTML |
| `simulate` | `--method` / `--periods` / `--seed` / `--n-reduced` | `reiter` / `200` / `0` / `30` | `ssj\|reiter` / periods / seed / reduced states |
| `simulate` | `--plot` / `--plot-save` | off | Browser plot / save HTML |
| `simulate-panel` | `--n-agents` / `--periods` / `--seed` | `1000` / `100` / `0` | Agents / periods / seed (no `--method`) |
| `distribution-irf` | `--method` / `--horizon` / `--shock-index` / `--shock-size` / `--n-reduced` | `reiter` / `40` / `1` / `1.0` / `30` | Must be reiter / horizon / 1-based shock / size (std) / states |
| `inequality-irf` | `--method` / `--horizon` / `--shock-index` / `--shock-size` / `--n-reduced` | `reiter` / `40` / `1` / `1.0` / `30` | Must be reiter / horizon / 1-based shock / size (std) / states |
| `inequality-irf` | `--plot` / `--plot-save` | off | Browser plot / save HTML |
| `accuracy` | `--method` / `--n-reduced` | `krusell-smith` / `30` | Solution to score / reduced states |
| `accuracy` | `--t-sim` / `--t-burn` / `--t-fit` | `10000` / `1000` / `4000` | Sim length / burn-in / PLM fit length |
| `accuracy` | `--rho-z` / `--sigma-z` / `--seed` | `0.95` / `0.007` / `98765` | Shock persistence / s.d. / seed |
| `accuracy` | `--plot` / `--plot-save` | off | Browser plot / save HTML |
| `estimate` | `--data` / `--priors` / `--observables` | `""` (data, priors required) | Observed aggregates CSV / priors TOML / aggregates |
| `estimate` | `--method` / `--sampler` | `ssj` / `mh` | Re-solved each draw: `ssj\|reiter` / `mh\|smc` |
| `estimate` | `--n-draws` / `--burnin` / `--n-smc` / `--n-mh-steps` / `--ess-target` | `2000` / `500` / `500` / `1` / `0.5` | RWMH draws / burn-in / SMC particles / MH steps / ESS target |
| `estimate` | `--t-horizon` / `--n-reduced` / `--proposal-scale` / `--adapt-interval` | `300` / `15` / `0.01` / `100` | SSJ truncation / reduced states / RWMH scale / adapt interval |
| `estimate` | `--measurement-error` / `--seed` | `none` / `0` | `none\|auto` (10% per-obs var) / seed |

# Examples

```bash
friedman hadsge steady-state huggett --format json
friedman hadsge solve huggett --method reiter --n-reduced 10
friedman hadsge irf huggett --method reiter --horizon 40
friedman hadsge distribution-irf huggett --horizon 40 --shock-index 1
friedman hadsge inequality-irf huggett --horizon 40
friedman hadsge simulate-panel huggett --n-agents 1000 --periods 100 --seed 7
friedman hadsge accuracy krusell-smith --t-sim 10000 --t-burn 1000
friedman hadsge estimate one-asset-hank --data aggregates.csv --priors priors.toml --method ssj --sampler mh --n-draws 2000
```

# See also

* [RA Core: Solve and Analyze](core.md) - representative-agent solution methods
* [Structured Family Models](family.md) - bank, CT, DCEGM, firm, OLG nodes
* [Simulation (DGPs)](../data/simulate.md) - `data simulate ha` aggregate deviations
