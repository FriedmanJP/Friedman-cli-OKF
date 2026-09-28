---
type: Feature
title: Unit-root and long-memory tests
description: ADF, KPSS, PP, Ng-Perron, break-robust and panel unit-root tests plus GPH/local-Whittle long-memory and variance-ratio tests.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/test.md
tags:
  - test
  - unit-root
  - stationarity
  - panel-unit-root
  - long-memory
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:57:55Z
sources:
  - id: generated-test
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/test.md
    title: Generated test reference (option and output tables)
  - id: guide-test
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/test.md
    title: test guide (null hypotheses, decision logic, pitfalls)
  - id: src-test
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/test.jl
    title: test command implementation
---

# Summary

These 21 leaves classify integration order: single-series unit-root/stationarity tests (`adf`, `kpss`, `pp`, `np`, `ers`, `dfgls`), break-robust variants (`za`, `lm-unitroot`, `adf-2break`, `fourier-adf`, `fourier-kpss`), seasonal roots (`hegy`), first-generation panel tests (`llc`, `ips`, `breitung`, `hadri`), second-generation panel tests (`cips`, `moon-perron`), semiparametric long-memory estimators (`gph`, `local-whittle`), and the random-walk `variance-ratio` test. Every leaf takes a required `data` CSV plus `--format`/`-f`, `--output`/`-o`, `--result` (replay a saved handle), and `--save-result`.

Read nulls in opposite pairs: ADF/PP/NP/ERS/DFGLS test H0 of a unit root (rejection means stationary) while KPSS tests H0 of stationarity; the confirmatory pattern is ADF-rejects plus KPSS-fails-to-reject. Panel unit-root leaves read a wide T×N matrix (columns are units), unlike the long-format panel cointegration leaves. Deterministic-term vocabularies differ per leaf (`none|constant|trend|both` vs `constant|trend` vs `level|trend`) and are enforced, not coerced.

LEAVES open question (intermediates): `unit-root` is a CLI path segment only — the generated reference has no `##` header for it, so each `###` entry below is counted exactly once. LEAVES open question (inventory): `INVENTORY.md` heads this command as "(91)" because it counts the four `test did` leaves under `did`, and its prose additionally omits `coint fisher-johansen`, `influence`, and `panel dh-causality` by name; LEAVES.md's 95 stands.

# Functions

## Single-series unit roots (11 leaves)

| Command | H0 | Output tables |
|---|---|---|
| `friedman test unit-root adf` | unit root | `adf_test` |
| `friedman test unit-root kpss` | stationary | `kpss_test` |
| `friedman test unit-root pp` | unit root | `phillips_perron_test` |
| `friedman test unit-root np` | unit root (Ng-Perron M-suite) | `ng_perron_test` |
| `friedman test unit-root ers` | unit root (point-optimal) | `ers_point_optimal_test` |
| `friedman test unit-root dfgls` | unit root (GLS-detrended) | `df_gls_test` |
| `friedman test unit-root za` | unit root with one break | `zivot_andrews_test` |
| `friedman test unit-root lm-unitroot` | unit root (breaks under null) | `lm_unit_root_test` |
| `friedman test unit-root adf-2break` | unit root with two breaks | `adf_2_break_test` |
| `friedman test unit-root fourier-adf` | unit root with smooth breaks | `fourier_adf_test` |
| `friedman test unit-root fourier-kpss` | stationary with smooth breaks | `fourier_kpss_test` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `adf` | `data` (required) | `--column`/`-c` (1), `--max-lags` (auto AIC), `--trend` (`constant`: none\|constant\|trend\|both) |
| `kpss` | `data` (required) | `--column`/`-c` (1), `--trend` (`constant`: constant\|trend) |
| `pp` | `data` (required) | `--column`/`-c` (1), `--trend` (`constant`: none\|constant\|trend) |
| `np` | `data` (required) | `--column`/`-c` (1), `--trend` (`constant`: constant\|trend) |
| `ers` | `data` (required) | `--column`/`-c` (1); flag `--trend` (constant-only default; needs 30+ obs) |
| `dfgls` | `data` (required) | `--column`/`-c` (1), `--regression` (`constant`: constant\|trend), `--lags` (`aic`: aic\|bic\|N), `--max-lags` (auto) |
| `za` | `data` (required) | `--column`/`-c` (1), `--trend` (`both`: intercept\|trend\|both), `--trim` (0.15) |
| `lm-unitroot` | `data` (required) | `--column`/`-c` (1), `--breaks` (0: 0\|1\|2), `--regression` (`level`: level\|trend), `--lags` (`aic`), `--max-lags` (auto), `--trim` (0.15) |
| `adf-2break` | `data` (required) | `--column`/`-c` (1), `--model` (`level`: level\|trend\|regime), `--lags` (`aic`), `--max-lags` (auto), `--trim` (0.10) |
| `fourier-adf` | `data` (required) | `--column`/`-c` (1), `--regression` (`constant`: constant\|trend), `--fmax` (3), `--lags` (`aic`), `--max-lags` (auto), `--trim` (0.15) |
| `fourier-kpss` | `data` (required) | `--column`/`-c` (1), `--regression` (`constant`), `--fmax` (3), `--bandwidth` (auto) |

## Seasonal and panel unit roots (7 leaves)

| Command | H0 | Output tables |
|---|---|---|
| `friedman test unit-root hegy` | unit root at each seasonal frequency | `hegy_seasonal_unit_root_test`, `hegy_summary` |
| `friedman test unit-root llc` | every unit has a unit root | `levin_lin_chu_test` |
| `friedman test unit-root ips` | every unit has a unit root | `ips_per_unit_adf_statistics`, `im_pesaran_shin_test` |
| `friedman test unit-root breitung` | every unit has a unit root | `breitung_panel_unit_root_test` |
| `friedman test unit-root hadri` | all units stationary | `hadri_panel_stationarity_test` |
| `friedman test unit-root cips` | unit root (cross-section dependence) | `pesaran_cips_test` |
| `friedman test unit-root moon-perron` | unit root (factor dependence) | `moon_perron_test` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `hegy` | `data` (required) | `--column`/`-c` (1), `--frequency` (4: quarterly\|12 monthly), `--deterministic` (`const-trend-seas`: none\|const\|const-seas\|const-trend\|const-trend-seas), `--lags` (`auto`) |
| `llc` | `data` (required, wide T×N) | `--deterministic` (`constant`: none\|constant\|trend), `--lags` (`auto`), `--max-lags`, `--criterion` (`aic`: aic\|bic\|tstat); flag `--cs-demean` |
| `ips` | `data` (required, wide T×N) | `--deterministic` (`constant`), `--lags` (`auto`), `--max-lags`, `--criterion` (`aic`); flag `--cs-demean` |
| `breitung` | `data` (required, wide T×N) | `--deterministic` (`constant`), `--lags` (0, integer); flag `--cs-demean` |
| `hadri` | `data` (required, wide T×N) | `--deterministic` (`constant`: constant\|trend) |
| `cips` | `data` (required, wide T×N) | `--lags` (`auto`), `--deterministic` (`constant`: constant\|trend), `--id-col`/`--time-col` (optional) |
| `moon-perron` | `data` (required, wide T×N) | `--factors` (`auto`), `--id-col`/`--time-col` (optional) |

## Long memory and random walk (3 leaves)

| Command | H0 | Output tables |
|---|---|---|
| `friedman test gph` | d = 0 (log-periodogram) | `gph_test` |
| `friedman test local-whittle` | d = 0 (semiparametric Whittle) | `local_whittle_test` |
| `friedman test variance-ratio` | random walk (all ratios = 1) | `variance_ratio_test`, `joint_random_walk_test` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `gph` | `data` (required) | `--column`/`-c` (1), `--bandwidth`/`-m` (floor(sqrt(T))), `--trim` (0) |
| `local-whittle` | `data` (required) | `--column`/`-c` (1), `--bandwidth`/`-m` (floor(sqrt(T))) |
| `variance-ratio` | `data` (required) | `--column`/`-c` (1), `--horizons` (`2,4,8,16`), `--method` (`lomackinlay`) |

# Examples

```bash
friedman test unit-root adf :nile --trend=constant
friedman test unit-root adf :nile --trend=trend --max-lags=8
friedman test unit-root kpss :nile --trend=constant
friedman test unit-root pp :nile --trend=constant
friedman test gph :nile --column=1 --bandwidth=32 --trim=1
friedman test local-whittle :nile --bandwidth=32
friedman test unit-root llc :denmark --deterministic=trend
friedman test unit-root ips :denmark --lags=2
friedman test variance-ratio :nile --horizons=2,5,10,20
```

# See also

* [Cointegration and stability](cointegration.md) - what to run after finding I(1) series
* [Regression diagnostics](diagnostics.md) - BDS, white-noise, and portmanteau tests
* [Univariate estimation](../estimate/timeseries.md) - ARIMA/ARFIMA/ARDL fits for classified series
