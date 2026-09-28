# Estimate

Fit econometric models from CSV data: multivariate and univariate time series, factor models, regime-switching and volatility models, the full regression family, panel estimators, and discrete-choice models. Every leaf reads a `data` CSV (or a bundled `:dataset`), prints coefficient and fit tables, and can persist the fit with `--save-model` for downstream `forecast`, `predict`, `irf`, `fevd`, and `hd` leaves.

* [Time-series and factor estimation](timeseries.md) - VAR, BVAR, VECM, SVAR, LP, TVP-VAR, MFVAR, ARIMA/SARIMA/ARFIMA/ARDL/NARDL/MIDAS, and static/dynamic/GDFM/structural factor models (20 leaves).
* [Regime-switching and volatility](regime-volatility.md) - Threshold, SETAR, STAR, Markov-switching, TVP regression, and ARCH/GARCH-family plus stochastic-volatility models (20 leaves).
* [Regression](regression.md) - OLS, IV, GMM/SMM, systems, penalized, robust, censored, sample-selection, quantile, RDD, and nonparametric regression (22 leaves).
* [Panel and discrete choice](panel-choice.md) - Panel regression, IV, ARDL, VAR, cointegrating regression, and binary/ordered/multinomial/count choice models (14 leaves).
