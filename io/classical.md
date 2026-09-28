---
type: Feature
title: Classical Input-Output Analysis (Leontief, Ghosh, Multipliers, Linkages)
description: Leontief/Ghosh inverses, multipliers, linkages, SDA, extraction, footprints, price, impact, and network statistics.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/io.md
tags:
  - friedman-cli
  - io
  - leontief
  - ghosh
  - multipliers
  - linkages
  - sda
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:57:28Z
sources:
  - id: gen-io
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/io.md
    title: Generated io reference (flag surface and output tables)
  - id: guide-io
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/io.md
    title: io workflow guide (classical leaves and output conventions)
  - id: src-io
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/io.jl
    title: src/commands/io.jl leaf handlers
---

# Summary

Classical linear IO over the Leontief inverse `L = (I - A)^-1` (demand-driven, `A = Z x^-1`) and the Ghosh inverse `G = (I - B)^-1` (supply-driven, `B = x^-1 Z`). Square matrices render wide (first column `sector`, then one column per sector); vector results render one row per sector. All leaves accept the shared IO input options (`--data`, `--n-sectors`, `--n-fd`, `--sectors`; default `:wiot`) plus `--format`/`--output`; leaves reading downloaded MRIO tables add `--parser csv|icio`.

Resolved open question — multipliers coverage: the counted leaf is `friedman io multipliers` (registered at `src/commands/io.jl` path `["io","multipliers"]`, in `generated/io.md`). `src/commands/multipliers.jl` is helpers-only — the legacy top-level `multipliers nardl` was folded into `estimate univariate nardl` at v1.0.0 (see the path-replacement map in `src/registry/families.jl` and the INVENTORY.md note "NO multipliers top-level"); there is no `generated/multipliers.md` and no separate leaf to count. The word "multipliers" in `estimate.md` output tables (`ardl_long_run_coefficients`, `nardl_*`) denotes tables of the NARDL/ARDL leaves, not leaves. No double-count.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman io leontief` | Demand-driven `A` and `L` | `technical_coefficients_a`, `leontief_inverse_l` |
| `friedman io ghosh` | Supply-driven `B` and `G` | `allocation_coefficients_b`, `ghosh_inverse_g` |
| `friedman io multipliers` | Output/income/employment multipliers, Type I & II | `io_multipliers` |
| `friedman io linkages` | Backward/forward linkages + Rasmussen Ui/Uj indices | `linkages` |
| `friedman io key-sectors` | Rasmussen quadrant classification only | `key_sectors` |
| `friedman io sda` | Structural decomposition of change between two periods | `structural_decomposition` |
| `friedman io extract` | Hypothetical extraction: output loss from removing sectors | `hypothetical_extraction_loss`, `hypothetical_extraction_summary` |
| `friedman io footprint` | Consumption-based footprint of a satellite account | `footprint`, `footprint_by_sector` (+ `regional_footprint`, `intensities_s`, `emission_multipliers`) |
| `friedman io price` | Leontief cost-push (or Ghosh dual) price model | `price_model` |
| `friedman io impact` | Final-demand scenario through `L` | `impact_summary`, `impact_by_sector` |
| `friedman io network-stats` | Domar weights, Herfindahl, APL, degrees, up/down-streamness | `network_stats_summary`, `network_stats_sectors` |

Leaf-specific options (beyond the shared input set and `--format`/`--output`):

| Leaf | Option | Default | Description |
|---|---|---|---|
| `leontief` | `--matrix` | `L` | `L` (inverse) / `A` (technical coefs) / `both` |
| `ghosh` | `--matrix` | `G` | `G` (inverse) / `B` (allocation coefs) / `both` |
| `multipliers` | `--kind` | `output` | `output` (column sums of `L`) / `income` (VA-weighted) / `employment` (jobs-weighted; needs account) |
| `multipliers` | `--type` | `I` | Type I (open) / Type II (household-closed) |
| `linkages` | `--forward` | `ghosh` | Forward basis: `ghosh` (row sums of `G`) / `leontief` |
| `key-sectors` | `--forward` | `ghosh` | Same basis; quadrant counts on stderr |
| `sda` | `--data2` | `""` | Second-period table (default: same as `--data`) |
| `sda` | `--method` | `additive` | `additive` (exact, zero residual) / `multiplicative` |
| `sda` | `--factors` | `""` | Comma-separated SDA factors (kebab); omit for legacy `L_effect`/`Y_effect` |
| `sda` | `--on` | `output` | `output` or satellite account name (emission SDA: intensity/technology/final_demand) |
| `sda` | `--plot` / `--plot-save` | off | Browser plot / save HTML |
| `extract` | `--sectors-extract` | `""` (required) | Sector names or 1-based indices, comma-separated |
| `extract` | `--mode` | `complete` | `complete\|backward\|forward\|partial` |
| `extract` | `--share` | `1.0` | Partial extraction share in (0, 1] |
| `extract` | `--region` | `""` | Extract a whole MRIO region block |
| `extract` | `--plot` / `--plot-save` | off | Browser plot / save HTML |
| `footprint` | `--account` | `""` | Satellite account (default: first available, e.g. CO2) |
| `footprint` | `--by` | `sector` | `sector` / `region` (MRIO production vs consumption) |
| `footprint` | `--detail` (flag) | off | Also emit intensities `S` and emission multipliers `M = SL` |
| `price` | `--dva` / `--dtax` | `""` | VA-coef / production-tax shocks: comma list or `sector=value` |
| `price` | `--mode` | `leontief` | `leontief` (cost-push dual) / `ghosh` (descriptive dual) |
| `price` | `--parser` / `--plot` / `--plot-save` | `csv` / off | MRIO parser / browser plot / save HTML |
| `impact` | `--dy` | `""` (required) | Final-demand change: comma list or `sector=value` |
| `impact` | `--kind` | `output` | `output\|va\|income\|employment\|<satellite>` |
| `impact` | `--type` | `I` | Type I (open) / Type II (household-closed) |
| `impact` | `--parser` / `--plot` / `--plot-save` | `csv` / off | MRIO parser / browser plot / save HTML |
| `network-stats` | `--parser` / `--plot` / `--plot-save` | `csv` / off | MRIO parser / browser plot / save HTML |

# Examples

```bash
friedman io leontief --matrix both
friedman io ghosh --matrix both
friedman io multipliers --kind output --type I
friedman io multipliers --kind employment
friedman io linkages --forward leontief
friedman io key-sectors
friedman io sda --on CO2
friedman io extract --sectors-extract Manufacturing --mode partial --share 0.5
friedman io footprint --account CO2 --detail
friedman io price --dva 0.1,0
friedman io impact --dy 10,0
friedman io network-stats
```

# See also

* [Tables and Sources](tables.md) - load and balance the tables these leaves read
* [Networks and Trade](networks.md) - nonlinear Baqaee-Farhi and MRIO trade leaves
