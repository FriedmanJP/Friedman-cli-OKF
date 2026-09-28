---
type: Feature
title: Cross-Spectra and Transfer Functions
description: Two-series coherence/phase/gain and the theoretical frequency response of HP, BK, Hamilton, and ideal filters.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/spectral.md
tags: [spectral, cross-spectrum, coherence, phase, gain, transfer-function]
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:58:15Z
sources:
  - id: generated-spectral
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/spectral.md
    title: Generated spectral reference (options, defaults, output tables)
  - id: spectral-guide
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/spectral.md
    title: Spectral narrative guide (cross-spectra, transfer functions)
  - id: spectral-src
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/spectral.jl
    title: Spectral command implementation
---

# Summary

Two leaves relate series in the frequency domain or evaluate a filter with no data at all. `spectral cross` runs cross-spectral analysis of two columns: the co-spectrum (in-phase covariance) and quadrature spectrum (out-of-phase covariance) by frequency, plus coherence (frequency-domain squared correlation), phase (lead-lag shift in radians; phase divided by frequency gives the time lag), and gain (regression slope of the second series on the first at each frequency). Coherence near one means the second series is predictable from the first at that frequency up to phase and scale. `spectral transfer` evaluates the theoretical transfer function — gain and phase by frequency — of a named filter on a grid of `--nobs` observations; it takes no data file. Gain near one marks frequencies the filter keeps, gain near zero marks those it kills; comparing the HP gain against the `ideal` band-pass shows the HP filter's leakage and compression. Both leaves share the `--format`/`-f`, `--output`/`-o`, `--plot-save`, `--plot` surface.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman spectral cross` | Co-/quadrature spectrum, coherence, phase, gain of two columns by frequency | `cross_spectral_analysis` |
| `friedman spectral transfer` | Theoretical gain and phase by frequency of `--filter hp\|bk\|hamilton\|ideal`; no data file | `filter_transfer_function` |

| Argument | Type | Required | Leaves | Description |
|---|---|---|---|---|
| `data` | String | yes | cross | Path to CSV data file |

| Option | Leaves | Default | Description |
|---|---|---|---|
| `--var1` | cross | `1` | First variable column index |
| `--var2` | cross | `2` | Second variable column index |
| `--filter` | transfer | `hp` | `hp`, `bk`, `hamilton`, `ideal` |
| `--lambda` | transfer | `1600.0` | Filter parameter (e.g. HP λ) |
| `--nobs` | transfer | `200` | Observations for the frequency grid |
| `--format` / `-f` | both | `table` | `table`, `csv`, `json` |
| `--output` / `-o` | both | — | Write to file instead of stdout |
| `--plot-save` | both | — | Save interactive plot to HTML file |
| `--plot` (flag) | both | off | Open interactive plot in browser |

# Examples

```bash
friedman spectral cross :fred_md --var1 1 --var2 2
friedman spectral transfer --filter hp --lambda 1600 --nobs 200
friedman spectral transfer --filter ideal --nobs 200
```

# See also

* [Correlograms and Spectral Density](spectral-density.md) - single-series ACF, periodogram, and spectral density
* [Trend-Cycle Filters and Nowcasting](../forecast/filter-nowcast.md) - the HP/BK/Hamilton filters whose frequency responses `transfer` evaluates
