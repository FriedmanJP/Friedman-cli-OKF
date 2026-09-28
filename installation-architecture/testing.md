---
type: Feature
title: Testing Tiers and Release Record
description: Fast engine/handler tests, golden files, real-MEMs integration tier, subprocess e2e battery, drift gates, and the Keep-a-Changelog history.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/test/runtests.jl
tags:
  - testing
  - golden
  - e2e
  - integration
  - changelog
  - releases
status: draft
stale_after: 2026-12-27T16:56:53Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:56:53Z
sources:
  - id: test-runners
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/test/runtests.jl
    title: Fast-tier runner (engine + handlers on mocks)
  - id: test-integration
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/test/integration/runtests.jl
    title: Real-MEMs integration runner
  - id: test-e2e
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/test/test_e2e.jl
    title: T4 subprocess battery
  - id: test-tools
    resource: https://github.com/FriedmanJP/Friedman-cli/tree/66bb97e50df7679fff068b78ed628da8c531e4f4/test/tools
    title: Drift gates and golden regen tooling
  - id: changelog
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/CHANGELOG.md
    title: Keep-a-Changelog history
---

# Summary

Three tiers: fast (`test/runtests.jl` — engine units plus handler tests against `test/mocks.jl`, no MacroEconometricModels needed), integration (`test/integration/runtests.jl` — the gate for handler changes, run against real MEMs with hermetic DGP fixtures in `test/integration/dgp.jl`, asserting envelope schema-validity, scalar sanity, and non-empty shapes), and e2e (`test/test_e2e.jl` — T4 subprocess battery, active when `CI=1` or `FRIEDMAN_E2E=1`, asserting stdout is exactly one JSON document per invocation). `test/golden/` pins byte-level output (render envelope/table/CSV, spectral, filter, estimate/forecast, error envelopes); `test/tools/` holds drift gates (`check_table_keys.jl` for W3 envelope-key stability, `check_handle_kinds.jl`, `check_mock_surface.jl`, `check_plot_coverage.jl`, `validate_envelopes.py` conformant draft-07 validation, `regen_golden.jl`). The CHANGELOG (Keep a Changelog + SemVer; pre-v0.6.0 in git tags) records v1.0.0 as the freeze: 477 leaves / 21 top-levels, MEMs exact `=1.0.0`, Julia 1.13, family promotion, `var`→`multivariate` rename, frozen envelope v1, removed snake_case aliases and `FRIEDMAN_LEGACY_OUTPUT`.

# Functions

| Tier | Command | What it proves |
|---|---|---|
| Fast | `julia --project test/runtests.jl` | Engine (types/parser/help/dispatch), handlers on mocks, single-JSON-per-invocation, golden byte-equality |
| Integration | `julia --project test/integration/runtests.jl` | Real-MEMs envelopes schema-valid, scalars sane, tables non-empty; closed-form VAR checks (`var_irf`, `var_fevd`, `lyapunov_gamma0`) |
| E2E (T4) | `CI=1 julia --project test/runtests.jl` | Subprocess stdout is exactly one JSON document; real launcher path |

Test-tree layout:

| Path | Contents |
|---|---|
| `test/runtests.jl` | Fast runner (includes engine files + `mocks.jl` directly) |
| `test/test_commands.jl` | Handler suites (estimate/test/irf/… incl. kebab-only C055 checks) |
| `test/test_handles.jl` | Stem resolution and handle-type suites |
| `test/test_repl.jl` | Session injection/caching suites |
| `test/test_e2e.jl` | T4 subprocess battery (gated on `CI`/`FRIEDMAN_E2E`) |
| `test/golden/` | Pinned outputs (`render.*`, `spectral.*`, `filter.*`, `estimate.*`, `forecast.*`, error envelopes) |
| `test/integration/runtests.jl` (+`_full.jl`, `dgp.jl`, `fixtures/`) | Real-MEMs gate with hermetic generators |
| `test/integration/schema_validate.jl` | In-repo envelope subset validator |
| `test/tools/` | `check_table_keys`, `check_handle_kinds`, `check_mock_surface`, `check_plot_coverage`, `dump_input_schemas`, `regen_golden`, `validate_envelopes.py` |
| `test/schema_validator.jl`, `support.jl`, `mocks.jl` | Shared validators, helpers, mock MEMs surface |

Release record notes (from `CHANGELOG.md` head):

- v1.0.0 (2026-09-20): first major; depth-2 leaves gain family middle segments (`estimate volatility garch`, `test unit-root adf`; family `other` stays flat); `did test *` → `test did *`; 11 HouseholdSystem leaves → top-level `hadsge`; `multipliers nardl` folds onto `estimate univariate nardl`; removed spellings exit 2 naming the new path.
- `data simulate` (21 leaves): each emits `simulated_data` + flattened `population_truth` + `simulation_settings`; `--seed` builds the `Xoshiro` the simulators require.
- Julia 1.13: ~1.8x faster cold runs vs 1.12; tempfile stdout capture stays (`redirect_stdout(IOBuffer)` unavailable).

# Examples

```bash
julia --project test/runtests.jl
julia --project test/integration/runtests.jl
CI=1 julia --project test/runtests.jl
FRIEDMAN_T3_DUMP_ENVELOPES=/tmp/env-dump julia --project test/integration/runtests.jl
python3 test/tools/validate_envelopes.py /tmp/env-dump
```

# See also

* [Installation](installation.md) - source checkout these commands run from
* [Architecture](architecture.md) - the structure under test
* [Handles & Output](../configuration/output-envelope.md) - envelope schema the validators enforce
