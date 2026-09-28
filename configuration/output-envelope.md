---
type: Feature
title: Handles, Globals, and the JSON Envelope
description: Leading-only global flags, the frozen envelope-v1 JSON contract, exit-code taxonomy, stem resolution, data loaders, and table emitters.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/schema/envelope-v1.json
tags:
  - configuration
  - envelope
  - exit-codes
  - globals
  - handles
  - output
status: draft
stale_after: 2026-12-27T16:56:53Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:56:53Z
sources:
  - id: envelope-schema
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/schema/envelope-v1.json
    title: Frozen envelope-v1 JSON schema
  - id: src-envelope
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/output/envelope.jl
    title: Envelope accumulator
  - id: src-render
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/output/render.jl
    title: Table/CSV/JSON renderers
  - id: src-errors
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/output/errors.jl
    title: CliError taxonomy and exit-code map
  - id: src-io
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/io.jl
    title: Global flags, loaders, output_result/output_kv
  - id: src-handles
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/handles.jl
    title: Stem resolver and typed persist
---

# Summary

Stdout carries data only — one JSON envelope, one table, or one CSV — while all status goes to stderr (`--quiet` drops info; validity warnings bypass quiet). Four leading-only globals (`--quiet`/`-q`, `--no-color`, `--json`, `--seed`) are stripped before dispatch; `--json` injects `--format json` when no `--format` is present, and `--seed` calls `Random.seed!` and is recorded in the envelope `meta`. `--format json` accumulates every `output_result`/`output_kv` table into one envelope (`schema_version: 1`, frozen at v1.0.0): `command`, `status` ok/error with co-occurring `error`, `meta` (cli/julia/mems versions, seed, argv, elapsed, manifest), `data` (stable registry-declared table keys; family tables use `<name>_<variable-slug>`), `warnings`, `artifacts`. Failures in JSON mode still emit exactly one error envelope on stdout (the `run_cli` error net covers pre-dispatch usage errors). Non-finite floats serialize as `"NaN"`/`"Inf"`/`"-Inf"`, never null.

# Functions

| Item | Kind | Role |
|---|---|---|
| `--quiet` / `-q` | global flag | Drop info-level status; warnings/errors still surface |
| `--no-color` | global flag | Disable stderr styling (also honors `NO_COLOR`) |
| `--json` | global flag | Force `--format json` when no `--format` given |
| `--seed N` / `--seed=N` | global option | `Random.seed!(N)`; forwarded as estimators' `seed=`; recorded in manifest/meta |
| `--version` / `-V`, `--warranty`, `--conditions` | first-token | Version / GPL notices; fire only as the first token |
| `output_result` | emitter | Matrix/DataFrame → table (PrettyTables) / CSV / envelope table |
| `output_kv` | emitter | Pairs → metric/value table (no scalar sibling in the envelope) |
| `resolve_stem` | handle | Stem → `.jld2` preferred, `.csv` on data slots only, else exact path |
| `resolve_save_path` | handle | Suffixless save path → append `.jld2` |
| `load_data` | loader | CSV / handle / `:builtin` → DataFrame (`~` expanded, `FRIEDMAN_DATA_ROOT` confinement) |
| `parse_dataset_name` | loader | Normalize `:fred-md`/`fred_md` spellings; typed `data/unknown-dataset` |
| `dataset_to_dataframe` | loader | MEMs dataset → DataFrame (panels keep `group`/`time` ids) |
| `df_to_matrix` / `variable_names` | loader | Numeric-only matrix and column names |
| `save_model_dispatch` / `load_model_dispatch` | handle | `.jld2` native / `.fmod` interim / `model://` dispatch |
| `CliError` / `exit_class` | errors | `class/code` taxonomy; envelope `error.exit_code` equals process exit |

Exit codes:

| Code | Class | Meaning |
|---|---|---|
| 0 | — | Success |
| 2 | `usage/*` | Unknown command/option, parse error, bad value |
| 3 | `data/*` | Missing file, wrong kind, bad values, serialization |
| 4 | `config/*` | Config/TOML errors |
| 5 | `model/*` | Convergence, identification, solve, singular (incl. mapped MEMs domain errors) |
| 6 | `env/*` | Model-version mismatch, missing completions, environment |
| 1 | other | Internal/bug |

Behavior notes:

- `wrap_legacy` type-checks loaded handles against registry `data_kinds`/`model_types`/`result_types` before the handler runs (`data/wrong-kind`, `model/wrong-kind`, `data/wrong-result`, all exit 3/5). `--result` cannot combine with `--model` or a data path (`usage/invalid`).
- Save rules: no suffix → append `.jld2`; `.csv` on data-edit output exports (metadata dropped); writing `.jld2` from CSV without `data import` is `usage/invalid`.
- Data-edit of CSV with `-o out.jld2` is refused; `data import` itself is exempt.
- MEMs `MacroModelError` subtypes map to `model/*` (exit 5); untyped orientation `ArgumentError`s match on message → `data/orientation` (exit 3).

# Examples

```bash
friedman --seed 7 estimate multivariate var macro.csv --lags 2 --format json
friedman --quiet --json irf var --model var --horizons 20
friedman estimate multivariate var macro.csv --format csv --output var.csv
friedman data simulate var --periods 200 --format json | jq .data.simulated_data.rows[0]
```

# See also

* [Config Files & Schema](config-files.md) - `config/*` exit-4 sources and `--strict`
* [CLI Engine & Registry](cli-engine.md) - dispatch pipeline and the `schema` self-description
* [Model Handles](../infra/model-handles.md) - handle inspection and verification leaves
