---
type: Feature
title: Data Handles and Examples (list, load, import, export)
description: Bundled example datasets and typed-handle import/export for the Friedman CLI data pipeline.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/data.md
tags:
  - friedman-cli
  - data
  - handles
  - import
  - examples
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
    title: data workflow guide (handles, stems, dataset references)
  - id: src-data
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/data.jl
    title: src/commands/data.jl leaf handlers
---

# Summary

The preferred unit of work is a MEMs typed container (`TimeSeriesData`, `PanelData`, `CrossSectionData`) persisted as a **stem** — pass `macro`, not `macro.jld2`. Data leaves resolve a data slot as `macro.jld2` if it exists (preferred), else `macro.csv`, else the exact path. Every command that takes a `<data>` path also accepts a `:name` reference to a bundled dataset (`:fred_md`, `:grunfeld`, …; both separator spellings resolve). The fixed dataset set lives in `src/io.jl` (`EXAMPLE_DATASETS`); the `wiot` IO table is not listed here and is served by the `io` family instead. An unknown name is `data/unknown-dataset` (exit 3) with a nearest-match hint.

`data import` is the CSV → typed conversion (`-o out.jld2` or a stem); editing a CSV with `-o out.jld2` is `usage/invalid` (import first). `data export` is the inverse (typed handle → CSV; frequency/tcode/dates dropped with an stderr note). `data list` enumerates the catalog and `data load` materializes a named example (or `--path` CSV) to stdout/CSV.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman data list` | List bundled example datasets with type, dimensions, description | `available_datasets` |
| `friedman data load [name]` | Load a named example (or `--path` CSV) and export | none (writes CSV / renders data) |
| `friedman data import <data>` | Import CSV or `:example` to a typed `.jld2` handle | `imported_data` (kind, n_obs, n_vars, path, frequency) |
| `friedman data export <data>` | Export a typed handle to CSV (panel adds group/time cols) | none (writes CSV directly) |

`data list` takes no argument. Its options:

| Option | Default | Description |
|---|---|---|
| `--format, -f` | `table` | `table\|csv\|json` |
| `--output, -o` | `""` | Export results to file |

`data load` arguments and options:

| Argument | Required | Description |
|---|---|---|
| `name` | no | Example dataset name (omit with `--path`) |

| Option | Default | Description |
|---|---|---|
| `--output, -o` | `""` | Output CSV file path |
| `--format, -f` | `table` | `table\|csv\|json` |
| `--vars` | `""` | Comma-separated variable subset (unknown names: `data/column-range`) |
| `--country` | `""` | Country filter (PWT panel) |
| `--dates` | `""` | Column name for date labels (time-series only) |
| `--path` | `""` | CSV path alternative to named dataset; wins over `name` with stderr note |
| `--transform, -t` (flag) | off | Apply FRED transformation codes (`usage/invalid` on cross-section) |

Give either `<name>` or `--path`; neither is a usage error.

`data import` arguments and options:

| Argument | Required | Description |
|---|---|---|
| `data` | yes | CSV path, stem, or `:example` dataset (never an existing handle) |

| Option | Default | Description |
|---|---|---|
| `--kind` | `""` | `timeseries\|panel\|cross-section` (required for CSV; inferred for `:example`) |
| `--frequency` | `other` | `daily\|monthly\|quarterly\|annual\|mixed\|other` (`usage/invalid` with cross-section) |
| `--dates` | `""` | CSV column of date labels (timeseries) |
| `--id-col` | `""` | Panel group column (required for `--kind panel`) |
| `--time-col` | `""` | Panel time column (required for `--kind panel`) |
| `--vars` | `""` | Comma-separated variable subset |
| `--tcodes` | `""` | Comma-separated FRED tcode per variable |
| `--note` | `""` | Free-form note stored in the handle header |
| `--output, -o` | `""` | Output stem or path (default: input basename) |
| `--format, -f` | `table` | `table\|csv\|json` |

`--kind` mismatch on `:example` is `data/wrong-kind`; re-importing a handle is `usage/invalid`. Identifier/label columns (`--id-col`, `--time-col`, `--dates`) are metadata, not variables. Missing cells are rejected (`data/missing-values`) — drop or impute first.

`data export` arguments and options:

| Argument | Required | Description |
|---|---|---|
| `data` | yes | Handle stem or path (`TimeSeriesData`/`PanelData`/`CrossSectionData`) |

| Option | Default | Description |
|---|---|---|
| `--output, -o` | `""` | Output CSV path (default: `<stem>.csv`) |
| `--format, -f` | `table` | `table\|csv\|json` |

A raw CSV input is `data/wrong-kind`.

# Examples

```bash
friedman data list
friedman data load fred_md --output=macro_tmp.csv
friedman data load pwt --country=USA --output=us_data_tmp.csv
friedman data load --path=nile_tmp.csv
friedman data import :fred_md -o fred_md_demo
friedman data import grunfeld_tmp.csv --kind panel --id-col group --time-col time -o grunfeld_csv_demo
friedman data export fred_md_demo -o fred_md_tmp.csv
```

# See also

* [Inspect, Clean, Transform](clean.md) - describe, diagnose, fix, and reshape handles
* [Simulation (DGPs)](simulate.md) - synthetic samples with known truth
* [IO Tables and Sources](../io/tables.md) - home of the `:wiot` example table
