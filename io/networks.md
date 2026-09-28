---
type: Feature
title: IO Production Networks and MRIO Trade
description: Baqaee-Farhi nonlinear counterfactuals, the io bf standard-form node, and MRIO trade accounting.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/io.md
tags:
  - friedman-cli
  - io
  - baqaee-farhi
  - production-networks
  - mrio
  - trade
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
    title: io workflow guide (Baqaee-Farhi and MRIO trade sections)
  - id: src-io
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/io.jl
    title: src/commands/io.jl leaf handlers
---

# Summary

`io bf` is an intermediate node (not a leaf): its 7 sub-leaves calibrate a Baqaee-Farhi nested-CES `ProductionNetwork` from the IO table and run exact nonlinear counterfactuals on it. Every `bf` leaf shares the network-calibration options `--theta` (production elasticity, scalar or per-sector list, default `1.0`), `--sigma` (consumption elasticity, `1.0`), `--epsilon`/`--eta` (two-nest elasticities, `1.0`), `--nests` (`single`/`two`), `--factors` (`single` sum VA rows / `va-cats` one factor per VA row), `--mu` (markups >= 1, `1.0` = efficient), and `--no-check` (allow clipped negative cost shares above 1%), plus `--parser`, `--model` (load a saved handle, skip re-estimation; `network` uses `--save-model` instead), `--plot`/`--plot-save`, and the shared IO input set with `--format`/`--output`. The scalar `io baqaee-farhi` leaf is the simpler 2019 interface (Domar weights, influence vector, centralities, optional second-order Hessian; Cobb-Douglas default makes Hulten exact). MRIO trade leaves (`bilateral-trade`, `export-decomposition`, `vertical-specialization`) need a multi-region table (e.g. via `io download` + `--parser icio`); the single-region `:wiot` example has no second region to address.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman io baqaee-farhi` | 2019 Domar/influence/centralities (+ optional Hessian) | `baqaee_farhi_2019_decomposition`, `second_order_hessian_beyond_hulten` |
| `friedman io bf network` | Calibrate the `ProductionNetwork` | `production_network_summary`, `production_network_sectors` |
| `friedman io bf equilibrium` | Exact nested-CES counterfactual equilibrium | `bf_equilibrium_summary`, `bf_equilibrium_sectors` |
| `friedman io bf local` | Local Hulten weights + second-order Hessian | `bf_local_hulten`, `bf_local_hessian` |
| `friedman io bf elasticities` | Factor/goods-price and Domar-share incidence at base point | `price_incidence`, `factor_price_incidence` |
| `friedman io bf shock-curve` | One-sector shock: exact vs Hulten vs second-order over a grid | `bf_shock_curve` |
| `friedman io bf wedges` | 2020 Theorem 1 technology vs allocative-efficiency split | `bf_wedge_decomp`, `bf_wedge_domar` |
| `friedman io bf misallocation` | Prop. 5 Harberger misallocation distance | `bf_misallocation_summary`, `bf_misallocation_sectors` |
| `friedman io bilateral-trade` | Bilateral intermediate/final/total trade, exporter to importer | `bilateral_trade_summary`, `bilateral_trade_by_sector` |
| `friedman io export-decomposition` | KWW (2014) DVA/RDV/FVA/PDC decomposition of gross exports | `kww_export_aggregates`, `kww_export_by_sector` |
| `friedman io vertical-specialization` | Hummels-Ishii-Yi / KWW import content of exports | `vertical_specialization`, `vertical_specialization_by_sector` |

Leaf-specific options beyond the shared sets in the Summary:

| Leaf | Option | Default | Description |
|---|---|---|---|
| `baqaee-farhi` | `--theta` / `--sigma` (Float64) | `1.0` / `1.0` | Scalar substitution elasticities |
| `baqaee-farhi` | `--second-order` (flag) | off | Also emit the sector x sector Hessian |
| `equilibrium` | `--dlog-a` / `--dlog-l` / `--dlog-mu` | `""` | Productivity / factor-supply / markup shocks (scalar or list; default 0) |
| `equilibrium` | `--method` / `--tol` / `--maxiter` / `--damping` | `newton` / `1e-10` / `500` / `0.5` | Inner price solver (`newton\|fixedpoint`) and settings |
| `local` | `--hessian` | `auto` | Form n x n Hessian: `auto` (n<=500) / `full` / `none` |
| `local` | `--no-elasticities` (flag) | off | Skip the attached BFElasticities block |
| `shock-curve` | `--sector` | `""` (required) | Shocked sector: name or 1-based index |
| `shock-curve` | `--range` / `--points` | `-0.5,0.5` / `41` | (lo,hi) grid for dlogA / grid points (>= 2) |
| `wedges` | `--dlog-a` / `--dlog-l` / `--dlog-mu` | `""` | Shock bundle (scalar or list; default 0) |
| `misallocation` | `--point` | `efficient` | Evaluation point: `efficient\|observed` |
| `misallocation` | `--hessian` | `auto` | Form n x n H_mu: `auto\|full\|none` |
| `bilateral-trade` | `--exporter` / `--importer` | `""` (required) | Region name or 1-based index |
| `bilateral-trade` | `--kind` | `total` | `total\|intermediate\|final` |
| `export-decomposition` | `--region` | `""` | Region name/index (required when nregions > 1) |
| `export-decomposition` | `--plot` / `--plot-save` | off | Browser plot / save HTML |
| `vertical-specialization` | `--region` | `""` | Region name/index (required when nregions > 1) |
| `vertical-specialization` | `--plot` / `--plot-save` | off | Browser plot / save HTML |

# Examples

```bash
friedman io baqaee-farhi --theta 0.5 --sigma 0.9 --second-order
friedman io bf network
friedman io bf equilibrium --dlog-a 0.01,0
friedman io bf local --hessian full
friedman io bf elasticities
friedman io bf shock-curve --sector 1 --range -0.2,0.2
friedman io bf wedges --dlog-a 0.01,0 --dlog-mu 0,0.02
friedman io bf misallocation --point observed
friedman io export-decomposition --region 1
friedman io vertical-specialization --region 1
```

# See also

* [Tables and Sources](tables.md) - download the multi-region tables trade leaves need
* [Classical IO](classical.md) - linear multipliers, linkages, SDA
