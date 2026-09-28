# Impulse

Structural innovation accounting: impulse responses, forecast-error variance shares, and shock contributions over history. All three commands identify structural shocks from a fitted multivariate model (`--id`, `--config`) or re-estimate from CSV, and accept `--model` handles saved by `estimate`.

* [Impulse responses](irf.md) - Dynamic responses to structural shocks for VAR, BVAR, TVP-VAR, LP, VECM, PVAR, FAVAR, and SDFM fits (8 leaves).
* [Variance decomposition](fevd.md) - Forecast-error variance shares by shock, including Bayesian, LP-bias-corrected, generalized, and panel variants (7 leaves).
* [Historical decomposition](hd.md) - Per-period shock contributions reconstructing each observed series, plus initial conditions (6 leaves).
