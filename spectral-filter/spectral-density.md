---
type: Feature
title: Correlograms and Spectral Density
description: Sample ACF/PACF/CCF with Ljung-Box diagnostics, the raw periodogram, and Welch/smoothed/AR spectral density estimates.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/spectral.md
tags: [spectral, acf, pacf, ccf, periodogram, spectral-density, welch]
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
    title: Spectral narrative guide (estimators, reading correlograms)
  - id: spectral-src
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/spectral.jl
    title: Spectral command implementation
---

# Summary

Three single-series leaves describe second-order structure nonparametrically or semi-parametrically. `spectral acf` reports sample autocorrelation (ACF) and partial autocorrelation (PACF) by lag with cumulative Ljung-Box Q-statistics and p-values — ACF at lag k is the correlation of yt with yt−k, PACF at lag k conditions on the intermediate lags — and, with `--ccf-with`, appends the cross-correlation (CCF) against a second column. Slowly decaying ACF with a sharp PACF cutoff diagnoses autoregressive structure, and the reverse diagnoses moving-average structure. `spectral periodogram` reports the raw periodogram (squared DFT magnitude at each Fourier frequency): unbiased but inconsistent, so read peak locations from it and magnitudes from `density`. `spectral density` estimates the spectral density with a confidence band by frequency via `--method periodogram` (raw ordinates), `welch` (default; averaged overlapping segments), `smoothed` (kernel smoothing with `--bandwidth`), or `ar` (implied spectrum of a fitted autoregression). All three leaves take the CSV positional `data` plus `--format`/`-f`, `--output`/`-o`, `--plot-save`, and `--plot`.

# Functions

| Leaf | Purpose | Output tables |
|---|---|---|
| `friedman spectral acf` | ACF/PACF by lag with Ljung-Box Q and p-values; CCF with `--ccf-with` | `acf_pacf` (autocorrelation, partial autocorrelation, Q, p-value by lag); `cross_correlation` (CCF by lag; only with `--ccf-with`) |
| `friedman spectral periodogram` | Raw periodogram power by Fourier frequency (inconsistent by design) | `periodogram` |
| `friedman spectral density` | Spectral density with confidence band by frequency | `spectral_density` |

| Argument | Type | Required | Description |
|---|---|---|---|
| `data` | String | yes | Path to CSV data file |

| Option | Short | Leaves | Default | Description |
|---|---|---|---|---|
| `--column` | `-c` | all 3 | `1` | Column index (1-based) |
| `--max-lag` | — | acf | min(20, T−1) | Maximum lag |
| `--ccf-with` | — | acf | — | Column index for cross-correlation |
| `--method` | `-m` | density | `welch` | `periodogram`, `welch`, `smoothed`, `ar` |
| `--bandwidth` | — | density | auto | Smoothing bandwidth (smoothed method) |
| `--format` | `-f` | all 3 | `table` | `table`, `csv`, `json` |
| `--output` | `-o` | all 3 | — | Write to file instead of stdout |
| `--plot-save` | — | all 3 | — | Save interactive plot to HTML file |
| `--plot` (flag) | — | all 3 | off | Open interactive plot in browser |

# Examples

```bash
friedman spectral acf :nile --column 1 --max-lag 20
friedman spectral acf :fred_md --column 1 --ccf-with 2
friedman spectral periodogram :nile --column 1
friedman spectral density :nile --method welch
friedman spectral density :nile --method smoothed --bandwidth 0.1
```

# See also

* [Cross-Spectra and Transfer Functions](spectral-cross.md) - two-series coherence/phase/gain and theoretical filter responses
* [Trend-Cycle Filters and Nowcasting](../forecast/filter-nowcast.md) - the HP/BK/Hamilton filters whose frequency responses `transfer` evaluates
