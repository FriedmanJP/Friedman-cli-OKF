---
type: Feature
title: Config Files and Schema (TOML)
description: TOML model specifications with schema validation, file/JSON/--set merge layers, --strict mode, and the get_* typed accessors.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/config.jl
tags:
  - configuration
  - toml
  - config
  - validation
  - priors
  - identification
status: draft
stale_after: 2026-12-27T16:56:53Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:56:53Z
sources:
  - id: src-config
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/config.jl
    title: TOML loaders, schema, merge, get_* parsers
  - id: docs-configuration
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/configuration.md
    title: Configuration guide (every section with fragments)
---

# Summary

Complex model specifications live in TOML files passed via `--config` (every leaf declaring it also gains `--config-json`/`--set`/`--strict` through `with_config_ergonomics`). Layers merge as file < `--config-json` < `--set` (dotted `key=value`, repeatable, values parsed as bool/int/float else string) and the merged result is validated once: unknown keys warn with a nearest-match suggestion, or error under `--strict`; bad enum values and malformed TOML/JSON are typed `config/*` errors (exit 4). Every key shown in the guide is read by a `get_*` parser; unlisted top-level sections are ignored as free-form.

# Functions

| Parser | Section | Role |
|---|---|---|
| `load_config` / `merge_config` | — | Load one file / merge file+JSON+`--set`, validate once |
| `validate_config_schema!` | — | Unknown-key warnings (errors under `--strict`), enum checks |
| `apply_set!` | — | Apply one `--set dotted.key=value` override |
| `get_prior` | `[prior]` | Minnesota prior: type, `lambda1..4`→`tau`/`lambda`/`decay` (lambda4 not forwarded), optimization flag |
| `get_identification` | `[identification]` | Sign/narrative method, sign matrix + horizons, narrative shock/periods/signs |
| `get_uhlig_params` | `[identification.uhlig]` | Penalty-ID tuning: starts, refine, iterations, tolerances |
| `get_lewis_tvv_params` | `[identification.lewis_tvv]` | Lewis TVV `weighting` (`one_step`/`two_step`/`cue`) |
| `get_sv_svar_params` | `[identification.sv_svar]` | SV-SVAR EM knobs: hetero shocks, maxiter, Gibbs burn/draws, init |
| `get_gmm` | `[gmm]` | LP-GMM moment/instrument names, or IV-GMM when `dep`+`theta0` set |
| `get_smm` | `[smm]` | SMM simulator (`ar1`/`arp`/`var1`/`iid_normal`), theta0, lags, bounds, weighting |
| `get_nongaussian` | `[nongaussian]` | Non-Gaussian SVAR method, contrast, distribution, regimes |
| `get_dsge` | `[model]`+`[solver]` | DSGE variables, parameters, `[[model.equations]]`, linear flag, VFI payload, solver |
| `get_dsge_constraints` | `[constraints]` | OccBin bounds and nonlinear constraints |
| `get_dsge_priors` | `[priors.<name>]` | Per-parameter `{dist, a, b}` Bayesian priors |
| `get_system` | `[[equations]]`+`[instruments]` | SUR/3SLS systems: dep/indep per equation, common or per-equation instruments |
| `get_statespace` | `[statespace]` | General linear-Gaussian system matrices (T/H/Z/Q/R/d/c/a1/P1/init_mode) with dimension checks |
| `get_determinacy` | `[determinacy]` | 1–2 swept params with lower/upper/points or explicit grids, method, div boundary |
| `get_policy_rule` / loss fns | `[rule]`+`[loss]` | Policy rule (`taylor`+`cmw` guard) and diagonal/AIT loss |
| `get_vecm_restriction` | `[vecm_restriction]` | Row-major H/A/b restriction matrices for VECM tests |
| `get_garch_midas` | `[garch_midas]` | `x_lf` low-frequency driver (only for `--rv macro`) |

Config-related invocation surface (appended to every `--config` leaf):

| Option/Flag | Type | Default | Description |
|---|---|---|---|
| `--config` | `String` | `""` | TOML config file path |
| `--config-json` | `String` | `""` | JSON object merged over `--config` |
| `--set` | `String` | `""` | Override `key=value`; repeatable; dotted keys OK |
| `--strict` | flag | `false` | Treat config schema warnings as errors (exit 4) |

Schema tables (from `src/config.jl`):

- `CONFIG_SCHEMA`: known sections `prior`, `identification`, `svar`, `svec`, `gmm`, `smm`, `nongaussian`, `model`, `solver`, `constraints`, `priors` (free param names).
- `CONFIG_NESTED_SCHEMA`: `prior.hyperparameters`, `prior.optimization`, `identification.sign_matrix/narrative/uhlig/lewis_tvv/sv_svar`.
- `CONFIG_ENUMS`: allow-lists for `prior.type`, `identification.method` (cholesky/sign/narrative/longrun/arias/uhlig/narrative-adrr/proxy/max-share/…), `gmm.weighting`, `smm.weighting`, `smm.model`, `nongaussian.*`, `solver.method`.

# Examples

```bash
friedman estimate multivariate bvar macro.csv --config bvar.toml
friedman irf var macro.csv --id sign --config sign.toml --format json
friedman estimate regression gmm macro.csv --config gmm.toml --set gmm.weighting=optimal --strict
friedman dsge solve rbc.toml --config-json '{"solver":{"order":2}}'
```

```toml
[prior]
type = "minnesota"
[prior.hyperparameters]
lambda1 = 0.2
lambda2 = 0.5
lambda3 = 1.0
[prior.optimization]
enabled = false
```

# See also

* [Handles & Output](output-envelope.md) - exit-4 taxonomy and `--seed` handling that configs interact with
* [CLI Engine & Registry](cli-engine.md) - `with_config_ergonomics` and `wrap_legacy` merge wiring
* [Architecture](../installation-architecture/architecture.md) - data-flow and stem rules behind handle paths in configs
