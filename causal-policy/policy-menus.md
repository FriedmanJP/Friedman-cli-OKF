---
type: Feature
title: Policy Causal-Effect Menus
description: Empirical (VAR/BVAR/LP/sign) and square model (DSGE/HA news) policy causal-effect menus, sequence-space jacobians, spanning checks, and forecast sufficiency.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/policy.md
tags: [policy, causal-effects-menu, mckay-wolf, news-shocks, jacobian, spanning, sufficiency]
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
    title: Policy narrative guide (McKay-Wolf/BM semantics, TOML, examples)
  - id: policy-src
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/policy.jl
    title: Policy command implementation
---

# Summary

The McKay–Wolf idea: the causal effects of identified policy shocks form a *menu*, and a rule counterfactual re-weights that menu so an alternative rule holds along the response to one non-policy shock — Lucas-robust, with no re-estimation under the new rule. Square-vs-thin is the central axis: a *square* menu (as many policy shocks as horizons) supports an exact solve, while a *thin* empirical menu gives a least-squares projection whose implementation error (`rel_residual`, `spanned`, `error_path`) ships in the output data. The four `policy effects` leaves each estimate their own menu from the data positional (no `--model` handle anywhere in the policy family — nothing is serializable, containers are re-derived per invocation) and print a tidy menu (`variable|role|shock|horizon|value`) plus a summary (`H`, `n_shocks`, `shock_labels`, `is_square`, `source`, `normalize`, `n_draws`). The two `policy news` leaves build square model menus — DSGE via one QZ solve of dimension n+H−1, HA from sequence-space jacobians — and `policy jacobian ha` exposes the standalone household jacobian behind the HA route. `policy spanning var` asks whether the model choice matters for one counterfactual (thin empirical vs full news menu), and `policy sufficiency dsge` is the population forecast-sufficiency laboratory that underwrites `policy history`. Reproducibility rides the global `--seed`; variables are referenced by `--outcomes name=index-or-column` / `--instruments` maps on empirical routes and `name=model_symbol` maps on structural routes.

# Functions

| Leaf | Estimator / route | Output tables |
|---|---|---|
| `friedman policy effects bvar` | BVAR menu, `--draws` posterior draws, TOML `--config` prior | `policy_causal_effects_menu` (entries by outcome, instrument, horizon); `policy_causal_effects_summary` (shape, normalization, dropped-draw honesty counts) |
| `friedman policy effects lp` | Local-projection menu, `--n-draws` independent-normal draws (pointwise approximation, not a joint posterior) | Same menu + summary tables |
| `friedman policy effects sign` | Sign-identified menu, `--replications` candidate rotations, TOML `--config` sign restrictions (required) | Same menu + summary tables |
| `friedman policy effects var` | Frequentist VAR menu, `--replications` bootstrap draws (0 = point only) | Same menu + summary tables |
| `friedman policy news dsge` | Square DSGE news menu perturbing `--policy-shock`; linear `--solver` only (nonlinear menus unsupported upstream) | Same menu + summary tables (solver diagnostics) |
| `friedman policy news ha` | Square HA news menu from sequence-space jacobians; `--instruments` defaults to `rate=r` | Same menu + summary tables (rule-closure diagnostics) |
| `friedman policy jacobian ha` | Household jacobian `dJ/dinput` for `--input r\|w` vs `--jac-output` aggregate, tidy `row\|col\|value` with T² rows; no plot recipe | `sequence_space_jacobian` |
| `friedman policy spanning var` | Thin empirical (VAR) vs full DSGE-news counterfactual path for one rule; `--model-outcomes`/`--model-instruments` must match `--outcomes`/`--instruments` names in order | `spanning_thin_vs_full_counterfactual_paths`; `spanning_verdict` (`spanned`, max `gap_rel` vs `--tol`, `loading_inside`, `rel_residual_emp`) |
| `friedman policy sufficiency dsge` | Population FEV ratios (Wold-info over full-info) per observable and horizon; consumes no data; invertibility is sufficient, not necessary | `forecast_sufficiency_fev_ratios`; `sufficiency_summary` (observable set, horizon, verdict) |

All `policy effects` leaves share one argument and the menu plumbing:

| Argument | Type | Required | Description |
|---|---|---|---|
| `data` | String | yes | Path to CSV data file |

| Option | Leaves | Default | Description |
|---|---|---|---|
| `--horizon` | effects ×4 | `20` | Truncation horizon H (≥ 1; MW use H=100) |
| `--shocks` | effects ×4 | (required) | Identified policy-shock columns (indices or names, comma-separated) |
| `--outcomes` | effects ×4 | (required) | Outcome map `name=index-or-column`, e.g. `infl=2,ygap=1` |
| `--instruments` | effects ×4 | — | Instrument map `name=index-or-column`, e.g. `rate=3` |
| `--lags` / `-p` | effects ×4 | AIC (var/sign), 4 (bvar/lp) | Lag order |
| `--normalize` | effects ×4 | `none` | `none`, `instrument-impact` (rescale so the first instrument's impact is +1) |
| `--output` / `-o`, `--format` / `-f` | effects ×4 | `table` | Export path; `table`, `csv`, `json` |
| `--draws` / `-n` | effects bvar | `2000` | Posterior draws |
| `--config` | effects bvar | — | TOML prior config |
| `--n-draws` | effects lp | `500` | Independent-normal N(value, se) draws |
| `--config` | effects lp | — | TOML identification config |
| `--replications` | effects sign | `1000` | Candidate rotations |
| `--config` | effects sign | (required) | TOML sign-restriction config |
| `--replications` | effects var | `0` | Bootstrap draws (0 = point only) |

Structural-route options:

| Option | Leaf | Default | Description |
|---|---|---|---|
| `model` (arg) | news dsge, sufficiency dsge | — | DSGE model file (TOML or .jl ModelSpec) |
| `model` (arg) | news ha, jacobian ha | — | HA model (builtin name or .jl HA ModelSpec) |
| `data` + `model` (args) | spanning var | — | CSV data file plus DSGE model file for the full news menu |
| `--policy-shock` | news dsge, spanning var | (required) | Exogenous shock the news menu perturbs |
| `--outcomes` | news dsge/ha | (required) | `name=model_variable` symbol map |
| `--instruments` | news dsge/ha | (`rate=r` on ha) | `name=model_variable` symbol map |
| `--horizon` | news dsge/ha | `100` | News horizon H |
| `--solver` | news dsge, spanning var | `gensys` | `gensys`, `klein`, `blanchard-kahn` |
| `--chunk` | news dsge | `0` | Shock columns per solve (0 = all at once) |
| `--t-horizon` | news ha | `300` | Sequence-space truncation (≥ H; < H+50 warns) |
| `--rule-closure` | news ha | `administered` | `administered`, `market` (market is huggett-only; its wedge is exactly neutral by construction) |
| `--dx` | news ha, jacobian ha | `0.0001` | Finite-difference step |
| `--behavioral-m` / `--behavioral-theta` | news dsge/ha | NaN (off) | Gabaix cognitive discounting / sticky expectations in [0,1]; news leaves only |
| `--input` | jacobian ha | `r` | Price input: `r`, `w` |
| `--jac-output` | jacobian ha | (required) | Household aggregate to differentiate, e.g. `C` or `A` |
| `--t-horizon` | jacobian ha | `300` | Jacobian dimension T (table is T² rows) |
| `--nonpolicy-shock` | spanning var | (required) | Baseline non-policy shock |
| `--model-outcomes` / `--model-instruments` | spanning var | — | SAME names in SAME order as `--outcomes`/`--instruments` (exact symbol equality) |
| `--rule` / `--rule-config` | spanning var | — | Builtin counterfactual rule / TOML `[rule]` section |
| `--tol` | spanning var | `0.1` | Spanned-verdict tolerance on `gap_rel` |
| `--n-sim` | spanning var | `200` | Draw propagation for gap bands |
| `--quantiles` | spanning var | `0.16,0.5,0.84` | Band quantiles in (0,1) |
| `--lags` / `-p` | spanning var | AIC | VAR lag order |
| `--replications` | spanning var | `0` | Bootstrap draws on the empirical menu |
| `--horizon` | spanning var | `20` | Truncation horizon H |
| `--shocks` / `--outcomes` / `--instruments` | spanning var | (required/—) | Same empirical maps as `policy effects` |
| `--observables` | sufficiency dsge | (required) | Comma-separated model variables the econometrician sees |
| `--horizon` | sufficiency dsge | `40` | FEV comparison horizon |
| `--method` | sufficiency dsge | `gensys` | DSGE solve method |

`policy spanning var` and `policy sufficiency dsge` also take `--output`/`--format`/`--plot-save`/`--plot`; `policy news` and `policy jacobian ha` take `--output`/`--format` only (no plot flags).

# Examples

```bash
friedman policy effects var :denmark --lags 1 --shocks 3 --outcomes infl=1,ygap=2 --instruments rate=3 --horizon 8
friedman policy effects bvar :denmark --lags 1 --shocks 3 --outcomes infl=1,ygap=2 --instruments rate=3 --horizon 8 --draws 500
friedman policy effects lp :denmark --lags 1 --shocks 3 --outcomes infl=1,ygap=2 --instruments rate=3 --horizon 8
cat > nk.toml <<'EOF'
[model]
parameters = { rho = 0.8, kappa = 0.3, phi = 1.5, sigma = 0.01 }
endogenous = ["ygap", "infl", "rate"]
exogenous = ["e", "mp"]
linear = true
[[model.equations]]
expr = "ygap[t] = rho * ygap[t-1] - 0.2 * rate[t] + sigma * e[t]"
[[model.equations]]
expr = "infl[t] = 0.5 * infl[t-1] + kappa * ygap[t]"
[[model.equations]]
expr = "rate[t] = phi * infl[t] + 0.01 * mp[t]"
EOF
friedman policy news dsge nk.toml --policy-shock mp --outcomes infl=infl,ygap=ygap --instruments rate=rate --horizon 8
friedman policy news ha huggett --outcomes c=C --horizon 4 --t-horizon 40
friedman policy jacobian ha huggett --input r --jac-output C --t-horizon 20
friedman policy spanning var :denmark nk.toml --lags 1 --shocks 3 --nonpolicy-shock 1 --outcomes infl=1,ygap=2 --instruments rate=3 --model-outcomes infl=infl,ygap=ygap --model-instruments rate=rate --policy-shock mp --rule rate-peg --horizon 8
friedman policy sufficiency dsge nk.toml --observables infl,rate --horizon 12
```

# See also

* [Policy Counterfactuals and Optimal Policy](policy-counterfactual.md) - rule and loss counterfactuals, OPP, and historical re-runs built on these menus
* [Difference-in-Differences](did.md) - microeconometric treatment-effect estimation
* [Forecasting and Forecast Evaluation](../forecast/forecast.md) - Waggoner–Zha conditional forecasts as the parallel VAR-based scenario tool
