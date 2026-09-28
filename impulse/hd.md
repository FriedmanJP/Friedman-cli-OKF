---
type: Feature
title: Historical decomposition
description: Per-period structural-shock contributions reconstructing each observed series for VAR, BVAR, LP, VECM, FAVAR, and SDFM fits.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/hd.md
tags:
  - hd
  - historical-decomposition
  - identification
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:57:55Z
sources:
  - id: generated-hd
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/hd.md
    title: Generated hd reference (option and output tables)
  - id: guide-hd
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/hd.md
    title: hd guide (coverage notes, panel/factor space, examples)
  - id: src-hd
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/hd.jl
    title: hd command implementation
---

# Summary

These 6 leaves split each observed series into per-period contributions from every structural shock plus initial conditions: frequentist VAR HD, posterior-mean Bayesian HD, structural LP HD, VECM HD via the VAR representation, FAVAR HD, and structural DFM HD in panel or factor space. Every leaf takes a required `data` CSV plus `--output`/`-o`, `--format`/`-f`, `--model`, `--result`/`--save-result`, and `--plot`/`--plot-save`.

Every leaf emits one table per variable with columns `period|actual|initial|contrib_<shock>…`, each carrying a decomposition check (contributions plus initial conditions reconstruct the series). `sdfm` defaults to `--space panel` (N variables into q shocks plus an idiosyncratic column, droppable with `--no-idiosyncratic`); `--space factor` decomposes the q factors with no idiosyncratic column. There is no `hd pvar` leaf: upstream has no `historical_decomposition` method for `PVARModel`, and the guide documents it as not shipped rather than wrapping an unsupported API. Likewise there is no `hd tvpvar`.

# Functions

| Command | Description | Output tables |
|---|---|---|
| `friedman hd var` | Frequentist historical decomposition | `historical_decomposition_*` |
| `friedman hd bvar` | Posterior-mean Bayesian HD | `bayesian_hd_*` |
| `friedman hd lp` | HD via structural local projections | `lp_historical_decomposition_*` |
| `friedman hd vecm` | VECM HD via VAR representation | `vecm_historical_decomposition_*` |
| `friedman hd favar` | FAVAR historical decomposition | `favar_historical_decomposition_*` |
| `friedman hd sdfm` | Structural DFM HD, panel or factor space | `sdfm_historical_decomposition_*` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `var` | `data` (required) | `--lags`/`-p` (auto), `--id` (`cholesky`: cholesky\|sign\|narrative\|longrun\|arias\|uhlig\|proxy\|max-share\|gmm-moments\|narrative-adrr\|lewis-tvv\|sv-em), `--config`, `--instrument` (proxy), `--target-var` (max-share) |
| `bvar` | `data` (required) | `--lags`/`-p` (4), `--id` (`cholesky`: cholesky\|sign\|narrative\|longrun), `--draws`/`-n` (2000), `--sampler` (`direct`: direct\|gibbs), `--config` |
| `lp` | `data` (required) | `--lags`/`-p` (4), `--var-lags` (=lags), `--id` (`cholesky`: cholesky\|sign\|narrative\|longrun), `--vcov` (`newey_west`: newey_west\|white\|driscoll_kraay), `--config` |
| `vecm` | `data` (required) | `--lags`/`-p` (2, levels), `--rank`/`-r` (`auto`), `--deterministic` (`constant`: none\|constant\|trend), `--id` (`cholesky`: cholesky\|sign\|narrative\|longrun\|svec\|lewis-tvv\|sv-em), `--config` |
| `favar` | `data` (required) | `--factors`/`-r` (auto), `--lags`/`-p` (2), `--key-vars`, `--horizons` (20), `--id` (`cholesky`), `--config` |
| `sdfm` | `data` (required) | `--factors`/`-q` (auto), `--id` (`cholesky`: cholesky\|sign\|proxy\|lewis-tvv\|sv-em\|gmm-moments), `--q-method` (`hallin-liska`: hallin-liska\|bai-ng\|amengual-watson), `--method` (`fglr`: fglr\|gdfm-var), `--spectral` (`lag-window`: lag-window\|smoothed-periodogram), `--instrument`, `--var-lags` (1), `--horizons` (20), `--config`, `--space` (`panel`: panel\|factor); flag `--no-idiosyncratic` (panel only) |

# Examples

```bash
friedman hd var :denmark --id=cholesky
friedman hd var :denmark --id=longrun --lags=4
friedman hd var :denmark --id=sign --config=sign_restrictions.toml
friedman hd bvar :denmark --draws=2000
friedman hd lp :denmark --id=sign --config=sign_restrictions.toml --vcov=white
friedman hd vecm :denmark --rank=2 --deterministic=constant --lags=4
friedman hd favar :denmark --lags=2 --key-vars=LRM,LRY,LPY
friedman hd sdfm :denmark --factors=2 --horizons=20
friedman hd sdfm :denmark --factors=2 --space=factor
```

# See also

* [Impulse responses](irf.md) - dynamic responses of the same identified shocks
* [Variance decomposition](fevd.md) - variance shares of the same identified shocks
* [Time-series estimation](../estimate/timeseries.md) - fitting the VAR/BVAR/LP/VECM/FAVAR/SDFM inputs
