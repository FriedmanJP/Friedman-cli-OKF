---
type: Feature
title: Policy Counterfactuals and Optimal Policy
description: McKay-Wolf rule counterfactuals, quadratic-loss optimal policy, second-moment and historical counterfactuals, and single-date plus sequential Barnichon-Mesters OPP.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/policy.md
tags: [policy, counterfactual, optimal-policy, opp, mckay-wolf, barnichon-mesters, history]
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:58:15Z
sources:
  - id: generated-policy
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/policy.md
    title: Generated policy reference (options, defaults, output tables)
  - id: policy-guide
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/policy.md
    title: Policy narrative guide (rules, loss TOML, OPP routes, examples)
  - id: policy-src
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/policy.jl
    title: Policy command implementation
---

# Summary

Fourteen leaves turn an estimated causal-effect menu into policy answers. `policy counterfactual` (var/bvar/lp) imposes one builtin rule (`rate-peg`, `inflation-target`, `output-gap`, `ngdp`, `taylor`) or a TOML `[rule]` section — exactly one of `--rule`/`--rule-config`; `rate-target` is TOML-only since the pegged path lives there — on the response to the ONE `--nonpolicy-shock`; `--method auto` solves exactly when the menu is square, otherwise least-squares, and `rate-peg`/`taylor` need exactly one mapped instrument. `policy optimal` (var/bvar/lp) replaces the rule with a quadratic loss from `--loss-config` (required; `lambda` has no upstream default; `[loss.smoothing]` needs exactly one instrument) and certifies the optimum with the FOC norm in the summary. `policy moments` (var/bvar) compares unconditional second moments (Wold covariance) under baseline vs rule-or-loss — exactly one of the two — with optional business-cycle frequency bands. `policy history` (var/bvar) re-runs an observation window `--t-range lo:hi` (required, length ≤ H−1) under a rule or loss, built from forecast revisions, never identified shocks. `policy opp` (var/bvar) is the Barnichon–Mesters optimal policy perturbation δ*: gaps, not levels — `--targets` is required on the model-forecast route and refused on the external `--values-file` route; bands sit at 60/75/90% with deliberately reversed polarity (rejection at the lower level is the conservative call); `--constraints-file` (TOML floors/ZLB, requires `--instrument-path`) selects SLSQP by default with `--method projection` as the crude floor-only fallback. `policy opp-sequence` (var/bvar) runs OPP across forecast vintages in `--forecasts-dir` (≥ 2 dates) with the exact three-part revision decomposition (news + preference + aging = δt − δt−1). Every leaf re-derives its menu per invocation (no `--model` handles anywhere in the policy family); the thin-menu honesty signals (`rel_residual`, `spanned`, `error_path`) ship in the output data.

# Functions

| Leaf | Role | Output tables |
|---|---|---|
| `friedman policy counterfactual bvar` | Rule counterfactual on a BVAR menu (`--draws` posterior draws, TOML `--config` prior) | `policy_counterfactual_paths` (baseline vs counterfactual per variable/horizon, bands when propagated); `enforcing_policy_shocks_nu` (date-0 shock vector ν*); `implementation_error_path`; `counterfactual_summary` (rule, H, `rel_residual`, `spanned`, draw counts) |
| `friedman policy counterfactual lp` | Rule counterfactual on an LP menu (`--n-draws` independent-normal draws; TOML `--config` identification) | Same four counterfactual tables |
| `friedman policy counterfactual var` | Rule counterfactual on a VAR menu (`--replications` bootstrap, 0 = point only) | Same four counterfactual tables |
| `friedman policy optimal bvar` | Quadratic-loss optimal policy on a BVAR menu | `policy_counterfactual_paths` (baseline vs optimal); `enforcing_policy_shocks_nu`; `implementation_error_path` (stacked FOC-block residuals); `counterfactual_summary` (+ `loss_base`, `loss_cf`, `foc_norm`) |
| `friedman policy optimal lp` | Quadratic-loss optimal policy on an LP menu | Same four optimal-policy tables |
| `friedman policy optimal var` | Quadratic-loss optimal policy on a VAR menu | Same four optimal-policy tables |
| `friedman policy moments bvar` | Second moments under rule-or-loss on a BVAR menu; `--draw-source ce\|wold\|both` | `counterfactual_standard_deviations` (baseline vs CF sd per variable, bands); `counterfactual_correlations` (per pair; needs ≥ 2 variables); `moments_summary` (policy, H, VMA `tail_share`, draw source, band) |
| `friedman policy moments var` | Second moments under rule-or-loss on a VAR menu | Same three moments tables |
| `friedman policy history bvar` | Historical re-run over `--t-range` on a BVAR menu (rule XOR loss) | `counterfactual_history` (realized vs counterfactual per date/variable, bands); `history_summary` (rule, window, `spanned`, draw counts) |
| `friedman policy history var` | Historical re-run over `--t-range` on a VAR menu (rule XOR loss) | Same two history tables |
| `friedman policy opp bvar` | BM optimal perturbation δ* on a BVAR menu; model-forecast or external route; constrained OPP via `--constraints-file` | `opp_recommendation_delta` (δ* and gradient per horizon, bands, rejections); `objective_gap_paths` (gaps before/after); `instrument_paths_announced_vs_recommended`; `opp_summary` (baseline/OPP loss, origin, failures, solver diagnostics) |
| `friedman policy opp var` | BM optimal perturbation δ* on a VAR menu | Same four OPP tables |
| `friedman policy opp-sequence bvar` | OPP across vintages on a BVAR menu; `--forecasts-dir` of per-date gap CSVs | `opp_sequence_delta_by_date`; `opp_revision_decomposition` (news + preference + aging); `opp_sequence_summary` (span, loss path, counts) |
| `friedman policy opp-sequence var` | OPP across vintages on a VAR menu | Same three sequence tables |

Shared menu plumbing (all 14 leaves take the `data` CSV positional plus `--output`/`-o`, `--format`/`-f`, `--plot-save`, and `--plot`):

| Option | Leaves | Default | Description |
|---|---|---|---|
| `--horizon` | all 14 | `20` | Truncation horizon H (≥ 1; MW use H=100) |
| `--shocks` | all 14 | (required) | Identified policy-shock columns (indices or names) |
| `--outcomes` | all 14 | (required) | Outcome map `name=index-or-column` |
| `--instruments` | all 14 | — | Instrument map `name=index-or-column` |
| `--lags` / `-p` | all 14 | AIC (var), 4 (bvar/lp) | Lag order |
| `--normalize` | all 14 | `none` | `none`, `instrument-impact` |
| `--draws` / `-n` | bvar ×7 | `2000` | Posterior draws |
| `--config` | counterfactual/optimal bvar | — | TOML prior config |
| `--replications` | var ×7 | `0` | Bootstrap draws (0 = point only) |
| `--n-draws` | counterfactual/optimal lp | `500` | Independent-normal draws (not a joint posterior) |
| `--config` | counterfactual/optimal lp | — | TOML identification config |
| `--nonpolicy-shock` | counterfactual ×3, optimal ×3 | (required) | The ONE shock the rule/optimum responds to |
| `--negate` (flag) | counterfactual ×3, optimal ×3 | off | Flip the non-policy shock's sign |
| `--rule` | counterfactual ×3, moments ×2, history ×2 | — | Builtin: `rate-peg`, `inflation-target`, `output-gap`, `ngdp`, `taylor` (textbook rho/phi — use `--rule-config` for CMW taylor) |
| `--rule-config` | counterfactual ×3, moments ×2, history ×2 | — | TOML `[rule]` section (rate-target paths, CMW taylor, custom pi_var/y_var) |
| `--loss-config` | optimal ×3, moments ×2, history ×2, opp ×2, opp-sequence ×2 | (required except moments/history where rule XOR loss) | TOML `[loss]` section |
| `--method` | counterfactual ×3 | `auto` | Projection: `auto` (exact when square), `ls`, `exact` |
| `--use-draws` | counterfactual ×3, optimal ×3, moments ×2, history ×2 | `auto` | Propagate menu draws into bands: `auto`, `on`, `off` |
| `--baseline-draws` | counterfactual ×3, optimal ×3 | `fixed` | `fixed` (MW convention) or `match` (pair draw d with draw d; equal counts enforced) |
| `--quantiles` | counterfactual ×3, optimal ×3, moments ×2, history ×2 | `0.16,0.5,0.84` | Band quantiles in (0,1) |
| `--spanned-tol` | counterfactual ×3 | `0.05` | `rel_residual` threshold behind `spanned` (optimal hardcodes 0.05 with no flag) |
| `--draw-source` | moments ×2 | `ce` | Uncertainty source: `ce`, `wold`, `both` (matching counts enforced) |
| `--frequencies` | moments ×2 | `none` | `none`, `business-cycle` (2π/32..2π/6), or `lo,hi` radians |
| `--plot-view` | moments ×2 | `sd` | Plot panel: `sd`, `corr` |
| `--t-range` | history ×2 | (required) | Observation window `lo:hi`, length ≤ H−1 |
| `--targets` | opp ×2 | (required, model route) | Explicit targets `name=value` per outcome — gaps, NOT levels; refused on the external route |
| `--values-file` | opp ×2 | — | External gap-paths CSV (one column per outcome; replaces the model forecast) |
| `--sd` | opp ×2 | — | External route: per-outcome forecast sd (BM damped covariance); required there |
| `--rho` | opp ×2 | `0.9` | External route: BM damping ρ in Σ[j,k]=sd_j·sd_k·ρ^\|j−k\| |
| `--cross-corr-file` | opp ×2 | — | External route: full covariance CSV — ignores `--sd`/`--rho` (mutually exclusive) |
| `--min-sd` | opp ×2 | `0.0` | External route: sd floor (warns when it binds) |
| `--origin` | opp ×2 | — | Forecast origin label, e.g. `2008M4` |
| `--n-sim` | opp ×2 | `2000` | Simulation draws for `estimate_opp` bands (0 = point only; δ* is the draw median per BM) |
| `--levels` | opp ×2 | `0.6,0.75,0.9` | Band levels — BM reversed polarity |
| `--instrument-path` | opp ×2 | — | Announced instrument path, H comma values (required with `--constraints-file`) |
| `--constraints-file` | opp ×2 | — | TOML `[[constraint]]` tables → constrained OPP |
| `--method` | opp ×2 | `auto` | Constrained solver: `auto`, `slsqp`, `projection` (crude floor-only fallback) |
| `--matched-draws` (flag) | opp ×2, opp-sequence ×2 | off | Pair draw d across sources (equal counts enforced) |
| `--interp-quarterly` (flag) | opp ×2 | off | External route: interpolate annual SEP paths to quarterly |
| `--plot-view` | opp ×2 | `delta` | Plot panel: `delta`, `paths` |
| `--forecasts-dir` | opp-sequence ×2 | (required) | Directory of per-date gap-path CSVs (sorted filenames = dates; ≥ 2 dates; H rows each) |
| `--sd` | opp-sequence ×2 | (required) | Per-outcome forecast sd shared across dates |
| `--rho` | opp-sequence ×2 | `0.9` | BM damping rho |
| `--n-sim` | opp-sequence ×2 | `0` | Simulation draws per date (compounds cost) |
| `--levels` | opp-sequence ×2 | `0.6,0.75,0.9` | Band levels (BM reversed polarity) |
| `--plot-view` | opp-sequence ×2 | `fan` | Plot panel: `fan`, `decomposition` |

# Examples

```bash
cat > loss.toml <<'EOF'
[loss]
outcomes = ["infl", "ygap"]
lambda = [1.0, 0.5]
EOF
friedman policy counterfactual var :denmark --lags 1 --shocks 3 --nonpolicy-shock 1 --outcomes infl=1,ygap=2 --instruments rate=3 --rule rate-peg --horizon 8
friedman policy optimal var :denmark --lags 1 --shocks 3 --nonpolicy-shock 1 --outcomes infl=1,ygap=2 --instruments rate=3 --loss-config loss.toml --horizon 8
friedman policy moments var :denmark --lags 1 --shocks 3 --outcomes infl=1,ygap=2 --instruments rate=3 --rule rate-peg --horizon 40
friedman policy history var :denmark --lags 1 --shocks 3 --outcomes infl=1,ygap=2 --instruments rate=3 --rule rate-peg --t-range 20:25 --horizon 12
friedman policy opp var :denmark --lags 1 --shocks 3 --outcomes infl=1,ygap=2 --instruments rate=3 --loss-config loss.toml --targets infl=2.0,ygap=0 --horizon 8
mkdir -p vintages
printf 'infl,ygap\n0.5,0.2\n0.4,0.1\n0.3,0.0\n0.2,-0.1\n' > vintages/2024Q1.csv
printf 'infl,ygap\n0.6,0.3\n0.5,0.2\n0.4,0.1\n0.3,0.0\n' > vintages/2024Q2.csv
friedman policy opp-sequence var :denmark --lags 1 --shocks 3 --outcomes infl=1,ygap=2 --instruments rate=3 --loss-config loss.toml --forecasts-dir vintages --sd 0.5,0.5 --horizon 4
```

# See also

* [Policy Causal-Effect Menus](policy-menus.md) - the empirical and model menus these counterfactuals re-weight
* [Difference-in-Differences](did.md) - microeconometric treatment-effect estimation
* [Forecasting and Forecast Evaluation](../forecast/forecast.md) - Waggoner–Zha conditional forecasts as the parallel VAR-based scenario tool
