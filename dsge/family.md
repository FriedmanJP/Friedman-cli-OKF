---
type: Feature
title: Structured DSGE Family Models (Bank, CT, DCEGM, Firm, Lifecycle, OLG)
description: Parameterized heterogeneous-agent family nodes under dsge with MIT/IRF/transition analysis.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/dsge.md
tags:
  - friedman-cli
  - dsge
  - heterogeneous-agents
  - olg
  - continuous-time
  - dcegm
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
    title: dsge workflow guide (CT and OLG pointers)
  - id: guide-hadsge
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/ha-dsge.md
    title: HA-DSGE workflow guide (continuous-time HA and Blanchard OLG)
  - id: src-dsge
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/dsge.jl
    title: src/commands/dsge.jl leaf handlers
---

# Summary

Six intermediate sub-nodes (`bank`, `ct`, `dcegm`, `firm`, `lifecycle`, `olg`) group 26 leaves over parameterized family models — no RA model file needed except `dcegm`, which takes a `model` argument (builtin `retirement` or a `.jl` DCEGMProblem/DCEGMSystem spec). Every leaf accepts `--format, -f` (`table`) and `--output, -o` (`""`); MIT/IRF leaves share `--horizon`/`--shock-size`/`--persist` conventions (TFP impulse with AR(1) decay) and `--plot`/`--plot-save` unless noted. `transition` leaves take a required `--z-path` CSV of the TFP path (length >= 2, all positive); `lifecycle transition` instead takes `--k0` XOR `--z-path`. The `ct` node covers one-asset Aiyagari plus `--two-asset` Kaplan-Moll-Violante (with `--ge` for general equilibrium); `olg` covers Blanchard perpetual youth with an `--nk` New-Keynesian variant.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman dsge bank pe` | Bewley-bank partial equilibrium at given (R, rk) | `bewley_banks_pe`, `bewley_banks_pe_policy` |
| `friedman dsge bank steady-state` | Bewley-bank credit-market stationary equilibrium | `bewley_banks_steady_state`, `bewley_banks_steady_state_policy` |
| `friedman dsge bank irf` | Bewley-bank MIT IRF to TFP | `bewley_banks_irf_*` |
| `friedman dsge bank transition` | Bewley-bank MIT TFP path | `bewley_banks_transition`, `bewley_banks_transition_diagnostics` |
| `friedman dsge ct solve` | CT Aiyagari (or KMV two-asset) stationary equilibrium | `ct_aiyagari_prices`, `ct_aiyagari_aggregates`, `ct_two_asset_solution`, `ct_two_asset_ge` |
| `friedman dsge ct irf` | MIT IRF of CT Aiyagari or two-asset GE | `ct_irf_*` |
| `friedman dsge ct fevd` | FEVD from the CT MIT impulse (single TFP shock) | `ct_fevd_*` |
| `friedman dsge ct transition` | MIT perfect-foresight transition (`ct_mit_shock`) | `ct_mit_shock_transition`, `ct_two_asset_transition` |
| `friedman dsge dcegm solve <model>` | Discrete-continuous EGM household solution | `dcegm_solve_diagnostics`, `dcegm_policy`, `dcegm_kinks` |
| `friedman dsge dcegm steady-state <model>` | DCEGM capital-market equilibrium | `dcegm_equilibrium` |
| `friedman dsge dcegm irf <model>` | MIT IRF of a DCEGM equilibrium (needs GE) | `dcegm_irf_*` |
| `friedman dsge dcegm fevd <model>` | FEVD of a DCEGM equilibrium (single TFP shock) | `dcegm_fevd_*` |
| `friedman dsge dcegm simulate <model>` | MIT simulation of a DCEGM equilibrium (levels) | `dcegm_simulation` |
| `friedman dsge dcegm transition <model>` | MIT TFP path of a DCEGM equilibrium | `dcegm_transition_path`, `dcegm_transition_diagnostics` |
| `friedman dsge firm steady-state` | Khan-Thomas plant-level stationary equilibrium | `khan_thomas_steady_state`, `khan_thomas_policy` |
| `friedman dsge firm irf` | Khan-Thomas MIT IRF of Y, I, K, N, C, Z | `khan_thomas_irf_*` |
| `friedman dsge firm transition` | Khan-Thomas MIT TFP path (`--prices ss\|ge`) | `khan_thomas_transition`, `khan_thomas_transition_diagnostics` |
| `friedman dsge lifecycle steady-state` | Life-cycle OLG stationary equilibrium | `lifecycle_steady_state`, `lifecycle_age_profiles` |
| `friedman dsge lifecycle irf` | MIT IRF of a life-cycle OLG steady state | `lifecycle_irf_*` |
| `friedman dsge lifecycle fevd` | FEVD of a life-cycle OLG steady state | `lifecycle_fevd_*` |
| `friedman dsge lifecycle simulate` | MIT simulation of a life-cycle OLG steady state | `lifecycle_simulation` |
| `friedman dsge lifecycle transition` | Life-cycle perfect-foresight transition | `lifecycle_transition_path`, `lifecycle_transition_diagnostics` |
| `friedman dsge olg solve` | Blanchard perpetual-youth steady state + saddle path | `blanchard_olg_steady_state`, `blanchard_olg_dynamics` |
| `friedman dsge olg simulate` | Blanchard transitional dynamics from k0 | `blanchard_olg_transition` |
| `friedman dsge olg irf` | Blanchard IRF via to_spec (TFP; NK adds monetary) | `blanchard_olg_irf_*` |
| `friedman dsge olg fevd` | Blanchard FEVD via to_spec (TFP; NK adds monetary) | `blanchard_olg_fevd_*` |

Per-node options (defaults from the generated reference):

Bank (`--n-n` 25 grid points, `--n-xi` 3 states throughout): `pe` adds `--n-min`/`--n-max` (0.05/8.0), `--beta`/`--sigma`/`--lambda` (0.99/0.95/0.2), `--zeta1`/`--zeta2` (0.02/2.0), `--r`/`--rk` (1.01/0.05), `--z`/`--alpha` (0.25/0.33), `--max-iter`/`--tol` (250/1e-6). `steady-state` adds `--r` (held fixed), `--r-lo`/`--r-hi` (NaN = default bracket), `--tol`/`--max-iter` (1e-4/24). `irf` adds `--horizon` (20), `--shock-size` (0.01), `--persist` (0.5), `--z` (0.25), `--plot`. `transition` adds required `--z-path`, `--z` (0.25).

CT (`--alpha`/`--rho`/`--sigma`/`--delta`/`--z` = 0.36/0.05/2.0/0.05/1.0 throughout): `solve` adds `--a-min`/`--a-max` (0.0/30.0), `--grid-size` (100), `--max-iter`/`--tol` (100/1e-6), `--two-asset`, `--ge` (two-asset GE; requires `--two-asset`). `irf`/`fevd` add `--horizon` (40), `--shock-size` (0.01), `--persist` (0.0), `--dt` (0.25), `--grid-size` (100), `--two-asset`, `--plot`. `transition` adds `--shock-size` (0.95 = Z0/Z multiplier), `--periods` (40), `--dt` (0.25), `--a-max` (30.0), `--grid-size` (100), `--max-iter`/`--tol` (100/1e-6), `--z-path` (two-asset MIT), `--two-asset`, `--plot` (one-asset only).

DCEGM (all take required `model`; `--n-periods` 20 finite horizon, 0 = infinite; `--beta` 0.98; `--wage` 20.0; `--n-a`/`--a-max` grid): `solve` adds `--r` (1.0), `--disutility` (1.0), `--sigma`/`--n-shocks` (0.0/1), `--taste-shock-scale` (0.0), `--pension`/`--credit-limit` (0.0), `--curvature` (2.0), `--max-iter`/`--tol` (500/1e-8), `--period`/`--income` (1/1 policy slice), `--view` (`policy\|threshold`), `--plot`. `steady-state` adds firm `--alpha`/`--delta`/`--z`/`--l` (0.36/0.08/1.0/1.0), `--r-lo`/`--r-hi` (0.001/0.2), `--labor` (`exogenous\|measured`), `--work-option` (`work`), `--n-sim` (40), `--tol`/`--max-iter` (1e-4/40), `--reprice-wage`. `irf`/`fevd`/`simulate` add firm `--alpha`/`--delta`/`--z`, `--horizon` 40 (irf/fevd) or `--periods` 40 (simulate), `--shock-size` (0.01; simulate 0.0), `--persist` (0.0); irf/fevd add `--plot`. `transition` adds required `--z-path`.

Firm (`--n-k` 16 capital nodes, `--n-eps` 3 states, `--z` 1.0): `steady-state` adds `--alpha`/`--nu` (0.256/0.64), `--delta`/`--beta`/`--gamma` (0.069/0.977/1.016), `--xi-bar`/`--b` (0.0083/0.011), `--phi` (2.4), `--rho-z`/`--sigma-z`/`--rho-e`/`--sigma-e` (0.859/0.014/0.859/0.022), `--tol`/`--max-iter` (1e-5/16). `irf` adds `--horizon` (20), `--shock-size` (0.01), `--persist` (NaN = firm rho_z), `--prices` (`ss\|ge`), `--plot`. `transition` adds required `--z-path`, `--prices` (`ss`).

Lifecycle: `steady-state` (`--j` 60, `--j-retire` 45, `--n-a` 200) adds `--survival` (0.99), `--a-max` (60.0), `--beta`/`--sigma` (0.97/2.0), `--alpha`/`--delta` (0.36/0.06), `--z` (1.0), `--n-pop` (0.0), `--replacement` (0.4), `--credit-limit` (0.0), `--income-rho`/`--income-sigma`/`--income-states` (0.95/0.2/5), `--config` (TOML `[lifecycle]` vectors), `--r-lo`/`--r-hi` (-0.02/0.1), `--tol`/`--max-iter` (1e-6/60), `--bequest-iter` (50), `--no-annuities`, `--plot`. `irf`/`fevd`/`simulate` use lighter grids (`--j` 40, `--j-retire` 30, `--n-a` 40, `--income-states` 3) with `--horizon`/`--periods` 20, `--shock-size` (0.01; simulate 0.0), `--persist` (0.0); irf/fevd add `--plot`. `transition` adds `--config`, `--k0` (NaN) XOR `--z-path`, `--horizon` (80, ignored with `--z-path`), `--tol`/`--max-iter`/`--relax` (1e-5/80/0.5).

OLG (`--alpha`/`--beta`/`--delta`/`--gamma`/`--z`/`--debt` = 0.36/0.96/0.08/0.98/1.0/0.0; b != 0 see MEMs#237): `solve` adds nothing further. `simulate` adds `--k0` (0 = 80% of SS k), `--horizon` (50), `--plot`. `irf`/`fevd` add `--rho-z`/`--sigma-z` (0.0), `--horizon` (40), `--shock-size` (1.0, irf only), NK options `--kappa`/`--phi-pi`/`--phi-y`/`--rho-i`/`--sigma-i`/`--omega` (0.1/1.5/0.125/0.0/0.0/0.0), `--nk` flag (adds pi, i, rr, eps_i), `--plot`.

# Examples

```bash
friedman dsge bank steady-state
friedman dsge bank irf --horizon 20 --shock-size 0.01
friedman dsge ct solve
friedman dsge ct solve --two-asset --ge
friedman dsge ct irf --horizon 40
friedman dsge dcegm solve retirement
friedman dsge dcegm steady-state retirement
friedman dsge dcegm irf retirement --horizon 40
friedman dsge firm steady-state
friedman dsge firm transition --z-path 1.0,1.01,1.0 --prices ge
friedman dsge lifecycle steady-state
friedman dsge olg solve
friedman dsge olg irf --horizon 40 --nk
```

# See also

* [RA Core: Solve and Analyze](core.md) - representative-agent solution methods
* [HA-DSGE](hadsge.md) - one-household SSJ/Reiter/Krusell-Smith models
* [Simulation (DGPs)](../data/simulate.md) - `data simulate olg` and `data simulate ct` DGPs
