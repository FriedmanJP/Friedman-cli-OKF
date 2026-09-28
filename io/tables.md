---
type: Feature
title: IO Tables and Sources (catalog, download, load, aggregate, balance)
description: MRIO source catalog, network download, table parsing, aggregation, and RAS/GRAS balancing.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/io.md
tags:
  - friedman-cli
  - io
  - input-output
  - mrio
  - download
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
    title: io workflow guide (loading data, sources, download)
  - id: src-io
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/io.jl
    title: src/commands/io.jl leaf handlers
---

# Summary

Every IO analysis leaf runs offline out of the box: with no `--data`, the bundled **`:wiot`** example (the Miller & Blair 2009 2-sector table, with `employment` and `CO2` satellite accounts) is used. Analysis leaves share the input options `--data` (CSV path, `:wiot` default, another `:example`, or a saved `.jld2`/`model://` handle), `--n-sectors` (required for CSV: `Z` is the first `n_sectors` columns), `--n-fd` (final-demand columns, default 1), and `--sectors` (CSV labels). A plain CSV carries no satellite accounts (needed for `employment` multipliers and `footprint`); use `:wiot` or a full MRIO archive. `io download` is the only network-touching leaf and respects `--offline` (exit 6 `env/network`); SHA-256 verification is on by default but the upstream checksum registry ships unpopulated, so unverified downloads warn rather than fail.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman io sources` | List downloadable IO/MRIO sources (offline catalog) | `io_mrio_sources` |
| `friedman io download` | Download an IO/MRIO archive (network; respects `--offline`) | `download_summary`, `download_log` |
| `friedman io load` | Parse/inspect a table: dimensions, balance, per-sector totals | `io_table_summary`, `sectors` |
| `friedman io aggregate` | Aggregate over regions and/or sector types | `io_table_summary`, `sectors` |
| `friedman io balance` | Repair intermediate flows via RAS/GRAS | `io_table_summary`, `sectors` |

`sources` options: `--format, -f` (`table`), `--output, -o` (`""`).

`download` options:

| Option | Default | Description |
|---|---|---|
| `--source` | `""` (required) | `oecd\|wiod\|exiobase3\|eora26\|gloria` |
| `--storage` | `""` (required) | Destination folder for downloaded archives |
| `--source-version` | `""` | Source version (e.g. OECD `v2023`; not `--version`, the reserved CLI global) |
| `--years` | `""` | Comma-separated year filter (default: all) |
| `--system` | `pxp` | EXIOBASE `pxp` (product-by-product) / `ixi` (industry-by-industry) |
| `--email` / `--password` | `""` | Account credentials (EORA26 only) |
| `--offline` (flag) | off | Refuse network access (exit 6) |
| `--overwrite` (flag) | off | Re-download existing files |
| `--no-verify` (flag) | off | Skip SHA-256 checksum verification |
| `--format, -f` / `--output, -o` | `table` / `""` | Output format / file |

`load` options (shared input set plus ICIO parser flags):

| Option | Default | Description |
|---|---|---|
| `--data` / `--n-sectors` / `--n-fd` / `--sectors` | `""` / `0` / `1` / `""` | Shared IO input options (see Summary) |
| `--parser` | `csv` | `csv` (`parse_io`) / `icio` (OECD ICIO text; `.zip` needs ZipFile) |
| `--year` / `--member` | `""` | ICIO year / member filter |
| `--no-aggregate-cn-mx` (flag) | off | ICIO: do not aggregate CN/MX processing units |
| `--check` (flag) | off | ICIO: run parser balance checks |
| `--save-model` | `""` | Save parsed table to a handle (`.jld2` native, `.fmod` interim) |
| `--format, -f` / `--output, -o` | `table` / `""` | Output format / file |

`aggregate` options: shared input set plus `--parser` (`csv`), `--region-map` (`old=new` pairs, comma-separated), `--sector-map` (`old=new` sector-type pairs), `--save-model`, `--format`/`--output`.

`balance` options: shared input set plus `--parser` (`csv`), `--method` (`ras`: `ras` non-negative / `gras` sign-preserving), `--tol` (`1e-10`), `--maxiter` (`1000`), `--save-model`, `--format`/`--output`.

# Examples

```bash
friedman io sources
friedman io download --source oecd --storage ./io_data --source-version v2023 --years 2018
friedman io download --source exiobase3 --storage ./io_data --system pxp
friedman io load
friedman io load --data :wiot
friedman io aggregate --region-map "USA=NAFTA,MEX=NAFTA"
friedman io balance --method gras
```

# See also

* [Classical IO](classical.md) - multipliers, linkages, SDA, extraction, footprints
* [Networks and Trade](networks.md) - Baqaee-Farhi networks and MRIO trade
* [Handles and Examples](../data/handles.md) - `:example` dataset conventions
