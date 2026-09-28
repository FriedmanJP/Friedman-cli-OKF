---
type: Feature
title: Forecast-error variance decomposition
description: Variance shares by structural shock for VAR, BVAR, LP, VECM, PVAR, FAVAR, and SDFM fits, plus identification-free generalized FEVD.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/fevd.md
tags:
  - fevd
  - variance-decomposition
  - identification
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:57:55Z
sources:
  - id: generated-fevd
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/fevd.md
    title: Generated fevd reference (option and output tables)
  - id: guide-fevd
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/fevd.md
    title: fevd guide (generalized FEVD, output formats, examples)
  - id: src-fevd
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/fevd.jl
    title: fevd command implementation
---

# Summary

These 7 leaves report each structural shock's share of forecast-error variance by horizon: identified VAR FEVD (with the Pesaran-Shin `--generalized` flag), posterior-mean Bayesian FEVD, bias-corrected LP FEVD (Gorodnichenko-Lee 2019), VECM FEVD via the VAR representation, panel FEVD, FAVAR FEVD, and factor-space SDFM FEVD. Every leaf takes a required `data` CSV plus `--output`/`-o`, `--format`/`-f`, `--model`, `--result`/`--save-result` (except `pvar`, which has `--model` but no result handles), and `--plot`/`--plot-save`.

Output layout: `var`, `vecm`, `favar`, and `sdfm` render one tidy `horizon|variable|shock|value` table with shares in [0,1]; `bvar`, `lp`, and `pvar` use the older wide layout (columns are shocks, rows are horizons). `--generalized` (VAR only) sidesteps identification entirely — its correlated-shock shares do not sum to 1 unless `--normalize` rescales them, a convention rather than a derivation. There is no `fevd tvpvar` leaf upstream: TVP-VAR variance shares are not wrapped.

# Functions

| Command | Description | Output tables |
|---|---|---|
| `friedman fevd var` | Identified or generalized VAR FEVD | `fevd`, `generalized_fevd`, `fevd_by_variable_*` |
| `friedman fevd bvar` | Posterior-mean Bayesian FEVD | `bayesian_fevd_*` |
| `friedman fevd lp` | Bias-corrected structural LP FEVD | `lp_fevd_*` |
| `friedman fevd vecm` | VECM FEVD via VAR representation | `vecm_fevd` |
| `friedman fevd pvar` | Panel VAR FEVD | `panel_var_fevd_*` |
| `friedman fevd favar` | FAVAR FEVD | `favar_fevd` |
| `friedman fevd sdfm` | Structural DFM FEVD (factor space) | `sdfm_fevd` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `var` | `data` (required) | `--lags`/`-p` (auto), `--horizons` (20), `--id` (`cholesky`: cholesky\|sign\|narrative\|longrun\|arias\|uhlig\|proxy\|max-share\|gmm-moments\|narrative-adrr\|lewis-tvv\|sv-em), `--config`, `--instrument` (proxy), `--target-var` (max-share); flags `--generalized`, `--normalize` |
| `bvar` | `data` (required) | `--lags`/`-p` (4), `--horizons` (20), `--id` (`cholesky`: cholesky\|sign\|narrative\|longrun), `--draws`/`-n` (2000), `--sampler` (`direct`: direct\|gibbs), `--config` |
| `lp` | `data` (required) | `--horizons` (20), `--lags`/`-p` (4), `--var-lags` (=lags), `--id` (`cholesky`: cholesky\|sign\|narrative\|longrun), `--vcov` (`newey_west`: newey_west\|white\|driscoll_kraay), `--config` |
| `vecm` | `data` (required) | `--lags`/`-p` (2, levels), `--rank`/`-r` (`auto`), `--deterministic` (`constant`: none\|constant\|trend), `--horizons` (20), `--id` (`cholesky`: cholesky\|sign\|narrative\|longrun\|svec\|lewis-tvv\|sv-em), `--config` |
| `pvar` | `data` (required, panel) | `--id-col`, `--time-col`, `--lags`/`-p` (1), `--horizons` (10) |
| `favar` | `data` (required) | `--factors`/`-r` (auto), `--lags`/`-p` (2), `--key-vars`, `--horizons` (20), `--id` (`cholesky`), `--config` |
| `sdfm` | `data` (required) | `--factors`/`-q` (auto), `--id` (`cholesky`: cholesky\|sign\|proxy\|lewis-tvv\|sv-em\|gmm-moments), `--q-method` (`hallin-liska`: hallin-liska\|bai-ng\|amengual-watson), `--method` (`fglr`: fglr\|gdfm-var), `--spectral` (`lag-window`: lag-window\|smoothed-periodogram), `--instrument`, `--var-lags` (1), `--horizons` (20), `--config` |

# Examples

```bash
friedman fevd var :denmark --horizons=20 --id=cholesky
friedman fevd var :denmark --id=sign --config=sign_restrictions.toml
friedman fevd var :denmark --horizons=20 --generalized
friedman fevd var :denmark --horizons=20 --generalized --normalize
friedman fevd bvar :denmark --horizons=20 --draws=5000 --sampler=gibbs
friedman fevd lp :denmark --horizons=20 --id=cholesky
friedman fevd vecm :denmark --rank=2 --deterministic=constant --lags=4
friedman fevd pvar :grunfeld --id-col=group --time-col=time --horizons=10
friedman fevd sdfm :denmark --factors=2 --horizons=20
```

# See also

* [Impulse responses](irf.md) - dynamic responses of the same identified shocks
* [Historical decomposition](hd.md) - shock contributions over history
* [Time-series estimation](../estimate/timeseries.md) - fitting the VAR/BVAR/LP/VECM/FAVAR/SDFM inputs
