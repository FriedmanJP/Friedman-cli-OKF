---
type: Feature
title: Difference-in-Differences
description: Staggered-adoption DiD estimation (TWFE plus heterogeneity-robust CS/SA/BJS/dCDH), LP event studies, and the LP-DiD estimator.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/did.md
tags: [did, event-study, lp-did, staggered-adoption, att, causal-inference]
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:58:15Z
sources:
  - id: generated-did
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/did.md
    title: Generated did reference (options, defaults, output tables)
  - id: did-guide
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/did.md
    title: DiD narrative guide (estimators, examples, diagnostics)
  - id: did-src
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/did.jl
    title: DiD command implementation
---

# Summary

Three leaves estimate treatment effects from a staggered-adoption panel CSV (positional `data`; `--id-col`/`--time-col` default to the first/second columns; `--outcome` and `--treatment` are required). `did estimate` reports the average treatment effect on the treated (ATT) by event time under two-way fixed effects by default, with heterogeneity-robust alternatives `--method cs` (Callaway–Sant'Anna), `sa` (Sun–Abraham), `bjs` (Borusyak–Jaravel–Spiess imputation), and `dcdh` (de Chaisemartin–D'Haultfoeuille). `did event-study` runs a local-projection event study whose pre-treatment leads test parallel trends and whose lags trace the dynamic response. `did lp-did` implements the Dube–Girardi–Jorda–Taylor LP-DiD estimator with clean-comparison, reweighting, and matching machinery. The four `test did` diagnostics (Bacon decomposition, pretrend, negative weights, HonestDiD) are separate leaves owned by the test domain, spelled `friedman test did …`.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman did estimate` | ATT by event time; `--method twfe` (default), `cs`, `sa`, `bjs`, `dcdh` | `did_estimation` (ATT, SE, CI by event time); `group_time_att_callaway_sant_anna` (cohort-by-event-time ATT matrix, CS only) |
| `friedman did event-study` | LP event study: leads test parallel trends, lags trace dynamics | `event_study_lp` (coefficient, SE, CI by event time) |
| `friedman did lp-did` | LP-DiD with clean comparisons, reweighting, matching | `lp_did_dube_et_al_2023` (coefficient, SE, CI, N by event time); pooled pre/post effects on stderr unless `--only-pooled`/`--only-event` |

All three leaves take one argument and share the display/export surface:

| Argument | Type | Required | Description |
|---|---|---|---|
| `data` | String | yes | Path to panel CSV data file |

| Option / Flag | Leaves | Default | Description |
|---|---|---|---|
| `--outcome` | all | (required) | Outcome variable column name |
| `--treatment` | all | (required) | Treatment indicator column name |
| `--id-col` | all | first column | Panel unit ID column |
| `--time-col` | all | second column | Time column |
| `--covariates` | all | — | Comma-separated covariate column names |
| `--cluster` | all | `unit` | `unit`, `time`, `twoway` |
| `--conf-level` | all | `0.95` | Confidence level |
| `--output` / `-o`, `--format` / `-f` | all | `table` | Export path; `table`, `csv`, `json` |
| `--plot-save` | all | — | Save plot to HTML file |
| `--plot` (flag) | all | off | Open interactive plot in browser |

Estimator-specific options:

| Option / Flag | Leaf | Default | Description |
|---|---|---|---|
| `--method` | estimate | `twfe` | `twfe`, `cs`, `sa`, `bjs`, `dcdh` |
| `--leads` | estimate | `0` | Pre-treatment periods |
| `--horizon` | estimate, event-study, lp-did | `5` | Post-treatment periods/horizon |
| `--control-group` | estimate | `never_treated` | `never_treated`, `not_yet_treated` |
| `--n-boot` | estimate | `200` | Bootstrap replications (dcdh only) |
| `--base-period` | estimate | `varying` | `varying`, `universal` (Callaway–Sant'Anna only) |
| `--leads` | event-study | `3` | Pre-treatment leads |
| `--lags` / `-p` | event-study | `4` | Control lags |
| `--pre-window` | lp-did | `3` | Pre-treatment window |
| `--post-window` | lp-did | `0` | Post-treatment window (0 = use horizon) |
| `--ylags` | lp-did | `0` | Outcome lags |
| `--dylags` | lp-did | `0` | Differenced outcome lags |
| `--pmd` | lp-did | — | Pre-treatment matching: `ccs`, `ipw`, or integer |
| `--nonabsorbing` | lp-did | — | Non-absorbing treatment (integer periods) |
| `--reweight` (flag) | lp-did | off | Reweight observations |
| `--nocomp` (flag) | lp-did | off | No composition adjustment |
| `--notyet` (flag) | lp-did | off | Use not-yet-treated as controls |
| `--nevertreated` (flag) | lp-did | off | Use never-treated as controls |
| `--firsttreat` (flag) | lp-did | off | Use first-treatment timing |
| `--oneoff` (flag) | lp-did | off | One-off treatment specification |
| `--only-pooled` (flag) | lp-did | off | Only report pooled estimates |
| `--only-event` (flag) | lp-did | off | Only report event-time estimates |

# Examples

```bash
friedman data simulate did --n 10 --periods 12 --seed 7 --format csv --output did_panel.csv
friedman did estimate did_panel.csv --outcome=y --treatment=D
friedman did estimate did_panel.csv --outcome=y --treatment=D --method=cs --control-group=not_yet_treated
friedman did estimate did_panel.csv --outcome=y --treatment=D --method=sa --cluster=twoway
friedman did estimate did_panel.csv --outcome=y --treatment=D --method=dcdh --n-boot=500
friedman did event-study did_panel.csv --outcome=y --treatment=D --leads=3 --horizon=5
friedman did lp-did did_panel.csv --outcome=y --treatment=D --horizon=5 --reweight --pmd=ipw
friedman did lp-did did_panel.csv --outcome=y --treatment=D --horizon=5 --notyet --only-pooled
```

# See also

* [Policy Causal-Effect Menus](policy-menus.md) - structural and VAR-based causal menus behind policy counterfactuals
* [Policy Counterfactuals and Optimal Policy](policy-counterfactual.md) - rule counterfactuals built on identified policy shocks
