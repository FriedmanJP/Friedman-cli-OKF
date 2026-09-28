---
type: Feature
title: Data Inspection, Cleaning, and Transforms
description: Describe, diagnose, fix, subset, balance, transform, filter, and validate CLI datasets.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/data.md
tags:
  - friedman-cli
  - data
  - cleaning
  - transforms
  - filters
  - validation
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
    title: data workflow guide (cleaning, tcodes, filters, validation)
  - id: src-data
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/data.jl
    title: src/commands/data.jl leaf handlers
---

# Summary

Nine leaves inspect and reshape datasets in place by type: a typed handle is cleaned/transformed as the same type (`*_clean.jld2`, `*_transformed.jld2` by default), CSV input still writes CSV, and a CSV edit with `-o out.jld2` is `usage/invalid` (run `data import` first). `describe`/`diagnose` accept a CSV path, a `:example` name, or a typed handle stem. NaN-padded series such as `mp_shocks` keep `NaN` outside each series' published sample (zero is a valid shock value): use `describe` (`first_valid`/`last_valid`), then `dropna --vars ...` or `keeprows --rows ...` to cut a finite sample. `validate` takes a model-type string (`--model var`), not a saved-model handle, and prints its verdict to stderr with no envelope table.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman data describe <data>` | Per-variable summary statistics (finite obs only) | `descriptive_statistics` |
| `friedman data diagnose <data>` | NaN/Inf counts and constant-series flag per variable | `data_diagnostics` |
| `friedman data fix <data>` | Clean via listwise / interpolate / mean | persists `*_clean` object |
| `friedman data dropna <data>` | Drop rows containing NaN/Inf (all-empty is `data/invalid`) | `cleaned_data` |
| `friedman data keeprows <data>` | Keep rows by index range/list (`--rows` required, `end` = last) | `filtered_data` |
| `friedman data balance <data>` | Balance a panel via DFM imputation | `balanced_panel` |
| `friedman data transform <data>` | Apply FRED tcodes 1-7 (one code per variable) | persists `*_transformed` object |
| `friedman data filter <data>` | Trend-cycle filter (`hp\|hamilton\|bn\|bk\|bhp`), time-series only | `data_filter` |
| `friedman data validate <data>` | Validate suitability for a model type (stderr verdict) | none |

All nine take a required `data` argument (handle stem or CSV path). Shared options on every leaf: `--format, -f` (`table`, default) and `--output, -o` (`""`). Leaf-specific options:

| Leaf | Option | Default | Description |
|---|---|---|---|
| `fix` | `--method, -m` | `listwise` | `listwise\|interpolate\|mean` |
| `dropna` | `--vars` | `""` | Column names to check, comma-separated (default: all); unknown name is `data/column-range` |
| `keeprows` | `--rows` | `""` (required) | Row indices, e.g. `1:100`, `1,5,10` |
| `balance` | `--method` | `dfm` | `dfm` |
| `balance` | `--factors, -r` | `3` | Number of factors |
| `balance` | `--lags, -p` | `2` | Factor VAR lags |
| `transform` | `--tcodes` | `""` | Comma-separated FRED codes; count must match variables, codes 1-7 |
| `filter` | `--method, -m` | `hp` | `hp\|hamilton\|bn\|bk\|bhp` |
| `filter` | `--component` | `cycle` | `cycle\|trend` |
| `filter` | `--lambda, -l` | `1600.0` | Smoothing parameter (HP/BHP) |
| `filter` | `--horizon` | `8` | Forecast horizon (Hamilton) |
| `filter` | `--lags, -p` | `4` | Lags (Hamilton/BN) |
| `filter` | `--columns, -c` | `""` | Column indices, comma-separated (default: all) |
| `validate` | `--model` | `""` | Model type: `var\|bvar\|vecm\|arima\|garch\|sv\|lp\|gmm\|factor` |

FRED codes: 1 level, 2 first difference, 3 second difference, 4 log, 5 first difference of log, 6 second difference of log, 7 first difference of percent change. `transform` on a `CrossSectionData` handle is `data/wrong-kind`, as is `filter` on a panel handle (time-series only).

# Examples

```bash
friedman data describe :stackloss
friedman data diagnose :mp_shocks
friedman data fix :denmark --method=interpolate --output=denmark_clean_tmp.csv
friedman data dropna :mp_shocks --vars=ygap,infl,ffr
friedman data keeprows :nile --rows=1:100
friedman data balance :grunfeld --factors=3 --lags=2
friedman data transform :denmark --tcodes=5,5,1,6,1
friedman data filter :nile --method=hp --component=cycle
friedman data filter :nile --method=hamilton --horizon=8 --lags=4
friedman data validate :denmark --model=var
```

# See also

* [Handles and Examples](handles.md) - import CSVs to typed handles first
* [Simulation (DGPs)](simulate.md) - synthetic samples with known truth
