# Forecasting, Fitted Values, and Filters

Out-of-sample forecasts across every model family with evaluation and combination, in-sample fitted values and residuals completing the fit–diagnose loop, trend-cycle and seasonal filters, and mixed-frequency nowcasting.

* [Forecasting and Forecast Evaluation](forecast.md) - Point and conditional (Waggoner–Zha) forecasts from multivariate, factor, regime, univariate, and volatility models, plus model-agnostic accuracy metrics, comparison tests, and combination.
* [In-Sample Fitted Values](predict.md) - What each fitted model implies for the estimation sample: conditional means, variances, state paths, and per-category probabilities across 38 leaves.
* [Model Residuals](residuals.md) - What each fitted model leaves unexplained: response, standardized, and per-category residuals across 40 leaves, including SETAR/STAR which have no predict leaf.
* [Trend-Cycle Filters and Nowcasting](filter-nowcast.md) - HP, boosted HP, Hamilton, Beveridge–Nelson, Baxter–King, and X-13 decompositions plus DFM/BVAR/bridge nowcasts, news decomposition, and nowcast-model forecasts.
