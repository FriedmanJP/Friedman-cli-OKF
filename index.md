---
okf_version: "0.2"
---

# Friedman-cli — OKF knowledge bundle

An [OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format)
bundle describing the commands and feature areas of
[Friedman-cli](https://github.com/FriedmanJP/Friedman-cli).
Start at the package overview, then drill into a domain.

## Package overview

* [Friedman-cli overview](overview.md) - What the CLI is, its feature map, and how to install it.

## Domains

* [Estimate](estimate/index.md) - Single- and multi-equation estimation: VAR, BVAR, VECM, SVAR, local projections, ARIMA, GMM, panel, count, volatility, and shrinkage estimators.
* [Test](test/index.md) - Specification and hypothesis tests: unit roots, cointegration, structural breaks, residual diagnostics, and panel tests.
* [Impulse](impulse/index.md) - Impulse responses, forecast-error variance decompositions, and historical decompositions.
* [Forecast](forecast/index.md) - Forecasting, forecast evaluation and scenarios, model prediction, residuals, filtering, and nowcasting.
* [Data](data/index.md) - Data management, DGP simulation, handles, and importing data into the CLI.
* [Input-output](io/index.md) - Input-output analysis: Leontief/Ghosh models, multipliers, linkages, multiregional tables, and trade.
* [DSGE](dsge/index.md) - DSGE modelling: solution, Bayesian estimation, continuous-time and heterogeneous-agent models, and OLG.
* [Causal policy](causal-policy/index.md) - Causal inference and policy analysis: difference-in-differences, counterfactuals, optimal policy, and menus.
* [Spectral filter](spectral-filter/index.md) - Spectral analysis and frequency-domain filtering.
* [Infrastructure](infra/index.md) - Model handles, the MCP server, handle rendering, the REPL, and shell completions.
* [Configuration](configuration/index.md) - Configuration files, the output envelope, global flags, dispatch, and the CLI engine.
* [Installation & architecture](installation-architecture/index.md) - Installation, release layout, system architecture, and the test suite.

## License

This bundle is licensed under the [Apache License, Version 2.0](LICENSE),
matching the upstream [open-knowledge-format](https://github.com/GoogleCloudPlatform/open-knowledge-format) project.
