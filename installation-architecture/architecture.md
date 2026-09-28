---
type: Feature
title: Application Architecture
description: Execution and data flow, stem resolution, rendering paths, module structure, dependencies, and the v1 stability policy.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/architecture.md
tags:
  - architecture
  - data-flow
  - stems
  - modules
  - dependencies
  - stability
status: draft
stale_after: 2026-12-27T16:56:53Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:56:53Z
sources:
  - id: docs-architecture
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/architecture.md
    title: Architecture guide
  - id: src-friedman
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/Friedman.jl
    title: Module includes, build_app, run_cli
  - id: src-handles
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/handles.jl
    title: Stem resolver
  - id: project-toml
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/Project.toml
    title: Dependencies and compat
---

# Summary

`bin/friedman ARGS` activates the project, instantiates when the Manifest is absent, and runs `Friedman.main(ARGS)` → `run_cli(ARGS)` → `dispatch(APP, args)`, where `APP` is the registry-built tree memoized once at precompile. CSV is the import format, not the working format: commands take stems, `data import` converts to typed `.jld2` (MEMs `save_model`/`load_model`), estimators save `--save-model` handles, downstream leaves reload via `--model`/`--result`, and `show STEM` renders anything loadable. Results reach DataFrames through `long_table` (array-valued results), `DataFrame(model)` (coefficient models), or hand-built frames where MEMs has no matching type; `io` matrices and regime-transition matrices render wide. The machine surface — command tree, option surface, envelope schema, stable table keys, error taxonomy, exit codes — is the API: envelope v1 is frozen at v1.0.0, minors are additive-only, removals happen only at majors after a deprecation alias.

# Functions

| Stage | Component | Role |
|---|---|---|
| Launch | `bin/friedman` | Activate, instantiate-if-needed, `Friedman.main(ARGS)` |
| Entry | `run_cli` | Intercept `repl`, strip leading globals, dispatch, map errors to exits |
| Tree | `build_app` / `APP` | Register every top-level group once; memoized const |
| Dispatch | `dispatch_node` / `dispatch_leaf` | Token-match walk; tokenize → bind → handler |
| Data in | `data import --kind` | CSV/`:example` → typed `STEM.jld2` |
| Persist | `--save-model` / `--model` | Estimator → handle; downstream reload (skip re-estimation) |
| Result cache | `--save-result` / `--result` | Result object → handle; re-render without recompute |
| Render | `output_result` | `:table` PrettyTables / `:csv` CSV.write / `:json` envelope |
| Plot | `_maybe_plot` | `--plot` / `--plot-save` on every show path |

Stem rules (from `docs/src/architecture.md`, `src/handles.jl`):

| Direction | Rule |
|---|---|
| Save, no suffix | Append `.jld2` (native `save_model`) |
| Save `.jld2` | Native handle (incl. `data import -o out.jld2`) |
| Save `.fmod` | Interim Serialization handle (unregistered types) |
| Save `.csv` (data-edit only) | CSV export; frequency/tcode/dates dropped |
| Save `.jld2` from CSV edit | Refused (`usage/invalid`; run `data import` first) |
| Load data slot | `path.jld2` if exists, else `path.csv`, else exact path; else `data/file-not-found` |
| Load `--model` | `STEM.jld2` if exists (no CSV fallback), then type-check |
| Load `--result` / `show` | `STEM.jld2` if exists, else exact path; no CSV fallback |

Module structure (`src/`):

| Path | Role |
|---|---|
| `Friedman.jl` | Imports, includes, `build_app`, `APP`, `run_cli`, `main`, `julia_main` |
| `cli/types.jl`, `parser.jl`, `dispatch.jl`, `help.jl` | Command structs, tokenizer/binder, dispatcher, help printer |
| `io.jl` | Example datasets, `load_data`, emitters, global flags, path validation |
| `output/errors.jl`, `envelope.jl`, `render.jl` | Error taxonomy, envelope accumulator, renderers |
| `config.jl` | TOML loaders and `get_*` accessors |
| `model_handle.jl`, `handles.jl` | `.fmod`/native dispatch, stem resolver |
| `registry/spec.jl`, `adapter.jl`, `families.jl` | `CommandSpec`, `wrap_legacy` adapter, family promotion |
| `commands/*.jl` | One file per family (`shared.jl` first; `fitted.jl` = predict+residuals; `multipliers.jl` helpers only) |
| `repl.jl` | Interactive session |

Dependencies (from `Project.toml`, `docs/src/architecture.md`):

| Package | Purpose |
|---|---|
| `MacroEconometricModels` (=1.0.0) | Core econometric library |
| `CSV`, `DataFrames`, `PrettyTables`, `JSON3` | Loading, tables, terminal format, JSON |
| `JLD2` (explicit import) | Activates the MEMs JLD2 extension for native handles |
| `FFTW` | Activates the MEMs FFTW extension (GDFM/spectral) |
| `TOML`, `LinearAlgebra`, `Statistics`, `SparseArrays`, `Random`, `Logging`, `Serialization`, `Dates` | Stdlib: config, math, RNG, logging, `.fmod`, dates |
| JuMP + Ipopt | DSGE constrained optimization; bundled in release builds (no separate install) |
| PATHSolver | Never bundled; niche DSGE constrained path only (`Pkg.add("PATHSolver")` if needed) |

# Examples

```bash
friedman data import macro.csv --kind timeseries -o macro
friedman estimate multivariate var macro --lags 2 --save-model var
friedman irf var --model var --horizons 20 --save-result irf
friedman show irf
friedman forecast evaluate metrics macro --actual gdp --result fcst_var,fcst_bvar
```

# See also

* [Installation](installation.md) - getting the launcher and sysimage onto PATH
* [Testing & Releases](testing.md) - tiers that guard this structure
* [CLI Engine](../configuration/cli-engine.md) - tree, parser, and registry in depth
