---
type: Feature
title: Impulse responses
description: Structural impulse response functions for VAR, BVAR, TVP-VAR, LP, VECM, PVAR, FAVAR, and SDFM fits.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/irf.md
tags:
  - irf
  - impulse-responses
  - identification
  - svar
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:57:55Z
sources:
  - id: generated-irf
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/irf.md
    title: Generated irf reference (option and output tables)
  - id: guide-irf
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/irf.md
    title: irf guide (identification surface, bootstrap schemes, examples)
  - id: src-irf
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/irf.jl
    title: irf command implementation
---

# Summary

These 8 leaves trace dynamic responses to structural shocks: frequentist VAR IRFs with the full 22-method identification surface, Bayesian IRFs with 68% credible bands (plus Giacomini-Kitagawa robust Bayes), date-specific TVP-VAR-SV IRFs, multi-shock structural LP IRFs, VECM IRFs via the VAR representation, panel OIRF/GIRF, and factor-wide FAVAR/SDFM IRFs. Every leaf takes a required `data` CSV plus `--output`/`-o`, `--format`/`-f`, `--model` (skip re-estimation from a saved handle), `--result`/`--save-result` (except `pvar`, which has `--model` but no result handles), and `--plot`/`--plot-save`.

Output layout: `var`, `bvar`, `tvpvar`, `lp`, `vecm`, `favar`, and `sdfm` render one tidy `horizon|variable|shock|value|lower|upper` table (`var`/`bvar`/`tvpvar`/`vecm` filter to `--shock`; `lp` to `--shock`/`--shocks`; `favar`/`sdfm` return every shock). `pvar` and the Arias/Uhlig/identified-set paths use the older wide per-shock layout. Sign/narrative IRFs report the identified-set median with set-robust bands by default; `--identified-set` with `--summary` selects an alternative set summary.

# Functions

| Command | Description | Output tables |
|---|---|---|
| `friedman irf var` | Frequentist IRFs, full identification surface | `irf`, `irf_identified_set`, `arias_importance_sampling_diagnostics` |
| `friedman irf bvar` | Bayesian IRFs, 68% credible bands | `bayesian_irf`, `robust_bayes_bands`, `robust_bayes_diagnostics` |
| `friedman irf tvpvar` | Date-specific TVP-VAR-SV IRF | `tvpvar_irf` |
| `friedman irf lp` | Structural LP IRFs, multi-shock | `lp_irf` |
| `friedman irf vecm` | VECM IRFs via VAR representation | `vecm_irf` |
| `friedman irf pvar` | Panel OIRF/GIRF with bootstrap bands | `panel_var_oirf_*`, `panel_var_girf_*` |
| `friedman irf favar` | FAVAR IRFs, factor- or panel-wide | `favar_irf` |
| `friedman irf sdfm` | Structural DFM IRFs, panel-wide | `sdfm_irf` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `var` | `data` (required) | `--lags`/`-p` (auto), `--shock` (1), `--horizons` (20), `--id` (`cholesky`: 22 methods incl. sign/narrative/longrun/arias/uhlig/fastica/jade/sobi/dcov/hsic/student_t/mixture_normal/pml/skew_normal/markov_switching/garch_id/proxy/max-share/gmm-moments/narrative-adrr/lewis-tvv/sv-em), `--ci` (`bootstrap`: none\|bootstrap\|theoretical), `--replications` (1000), `--instrument` (proxy), `--target-var` (max-share), `--bootstrap` (`iid`: iid\|wild\|block), `--block-length` (0), `--wild-dist` (`rademacher`: rademacher\|mammen), `--bias-reps` (0), `--config`, `--summary` (`none`: none\|median-target\|modal-model\|joint-band\|sup-t-band); flags `--cumulative`, `--identified-set`, `--stationary-only`, `--bias-correct` |
| `bvar` | `data` (required) | `--lags`/`-p` (4), `--shock` (1), `--horizons` (20), `--id` (`cholesky`: cholesky\|sign\|narrative\|longrun\|robust-bayes), `--draws`/`-n` (2000), `--sampler` (`direct`: direct\|gibbs), `--config`; flag `--cumulative` |
| `tvpvar` | `data` (required) | `--date` (required, 1:T_eff), `--horizons` (20), `--shock` (1), `--lags`/`-p` (2), `--draws`/`-n` (2000), `--burnin` (1000), `--thin` (1), `--n-train` (0), `--k-q` (0.01), `--k-s` (0.1), `--k-w` (0.01), `--irf-draws` (500); flags `--no-tvp`, `--no-sv`, `--no-stationary-only` |
| `lp` | `data` (required) | `--shock` (1), `--shocks` (comma-list), `--horizons` (20), `--lags`/`-p` (4), `--var-lags` (=lags), `--id` (`cholesky`: cholesky\|sign\|narrative\|longrun), `--ci` (`none`: none\|bootstrap), `--replications` (200), `--conf-level` (0.95), `--vcov` (`newey_west`: newey_west\|white\|driscoll_kraay), `--config`; flag `--cumulative` |
| `vecm` | `data` (required) | `--lags`/`-p` (2, levels), `--rank`/`-r` (`auto`), `--deterministic` (`constant`: none\|constant\|trend), `--shock` (1), `--horizons` (20), `--id` (`cholesky`: cholesky\|sign\|narrative\|longrun\|svec\|lewis-tvv\|sv-em), `--ci` (`bootstrap`), `--replications` (1000), `--config` |
| `pvar` | `data` (required, panel) | `--id-col`, `--time-col`, `--lags`/`-p` (1), `--horizons` (10), `--irf-type` (`oirf`: oirf\|girf), `--boot-draws` (500), `--confidence` (0.95) |
| `favar` | `data` (required) | `--factors`/`-r` (auto), `--lags`/`-p` (2), `--key-vars`, `--horizons` (20), `--id` (`cholesky`), `--config`; flag `--panel-irf` |
| `sdfm` | `data` (required) | `--factors`/`-q` (auto), `--id` (`cholesky`: cholesky\|sign\|proxy\|lewis-tvv\|sv-em\|gmm-moments), `--q-method` (`hallin-liska`: hallin-liska\|bai-ng\|amengual-watson), `--method` (`fglr`: fglr\|gdfm-var), `--spectral` (`lag-window`: lag-window\|smoothed-periodogram), `--instrument`, `--var-lags` (1), `--horizons` (40), `--config`, `--ci` (`none`: none\|bootstrap), `--reps` (200) |

# Examples

```bash
friedman irf var :denmark --shock=1 --horizons=20
friedman irf var :denmark --id=sign --config=sign_restrictions.toml
friedman irf var :denmark --id=longrun --horizons=40
friedman irf var :denmark --ci=bootstrap --bootstrap=wild --wild-dist=mammen
friedman irf bvar :denmark --shock=1 --horizons=20 --draws=5000 --sampler=gibbs
friedman irf tvpvar :denmark --date=40 --shock=1 --horizons=20
friedman irf lp :denmark --shocks=1,2,3 --id=cholesky --horizons=30
friedman irf pvar :grunfeld --id-col=group --time-col=time --irf-type=girf
friedman irf favar :denmark --lags=2 --panel-irf
friedman irf sdfm :denmark --factors=2 --horizons=40
```

# See also

* [Variance decomposition](fevd.md) - variance shares of the same identified shocks
* [Historical decomposition](hd.md) - shock contributions over history
* [Time-series estimation](../estimate/timeseries.md) - fitting the VAR/BVAR/LP/VECM/FAVAR/SDFM inputs
