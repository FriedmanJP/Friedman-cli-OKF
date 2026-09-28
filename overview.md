---
type: Package
title: Friedman-cli
description: A command-line interface for macroeconometric research and analysis, wrapping MacroEconometricModels.jl.
resource: https://github.com/FriedmanJP/Friedman-cli
tags: [macroeconometrics, cli, time-series, dsge, forecasting]
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T17:07:02Z
sources:
  - id: upstream-readme
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/README.md
    title: Upstream README (feature summary and installation)
  - id: upstream-cli-reference
    resource: https://github.com/FriedmanJP/Friedman-cli/tree/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated
    title: Generated per-command reference (21 files, 477 leaves)
  - id: upstream-src
    resource: https://github.com/FriedmanJP/Friedman-cli/tree/66bb97e50df7679fff068b78ed628da8c531e4f4/src
    title: Upstream source tree
---

# Summary

Friedman-cli is a command-line interface for macroeconometric research
and analysis. It wraps MacroEconometricModels.jl behind 21 top-level
commands and 477 leaf commands covering estimation, testing, impulse
analysis, forecasting, data handling, input-output analysis, DSGE
modelling, causal policy evaluation, and spectral methods, plus the
configuration, envelope, and installation machinery shared by every
command. Every leaf emits one JSON envelope (or a table/CSV rendering
of it) and exits with a documented status code.

# Feature map

| Domain | Contents |
|---|---|
| [Estimate](estimate/timeseries.md) | [Time-series and factor](estimate/timeseries.md), [regression](estimate/regression.md), [regime/volatility](estimate/regime-volatility.md), [panel and discrete-choice](estimate/panel-choice.md) estimation |
| [Test](test/unit-root.md) | [Unit-root](test/unit-root.md), [cointegration](test/cointegration.md), [diagnostics](test/diagnostics.md), [panel/VAR/IV/DiD](test/panel-var.md) tests |
| [Impulse](impulse/irf.md) | [Impulse responses](impulse/irf.md), [FEVD](impulse/fevd.md), [historical decomposition](impulse/hd.md) |
| [Forecast](forecast/forecast.md) | [Forecasting and evaluation](forecast/forecast.md), [fitted values](forecast/predict.md), [residuals](forecast/residuals.md), [filters and nowcasting](forecast/filter-nowcast.md) |
| [Data](data/handles.md) | [Handles and examples](data/handles.md), [simulation](data/simulate.md), [cleaning and transforms](data/clean.md) |
| [Input-output](io/tables.md) | [Tables and sources](io/tables.md), [classical analysis](io/classical.md), [networks and MRIO](io/networks.md) |
| [DSGE](dsge/core.md) | [Core](dsge/core.md), [Bayesian estimation](dsge/bayes.md), [HA-DSGE](dsge/hadsge.md), [family models](dsge/family.md) |
| [Causal policy](causal-policy/did.md) | [Difference-in-differences](causal-policy/did.md), [counterfactuals and optimal policy](causal-policy/policy-counterfactual.md), [causal-effect menus](causal-policy/policy-menus.md) |
| [Spectral filter](spectral-filter/spectral-density.md) | [Correlograms and spectral density](spectral-filter/spectral-density.md), [cross-spectra](spectral-filter/spectral-cross.md) |
| [Infrastructure](infra/model-handles.md) | [Model handles](infra/model-handles.md), [serve and show](infra/serve-show.md), [REPL and completions](infra/repl-completions.md) |
| [Configuration](configuration/config-files.md) | [Config files](configuration/config-files.md), [envelope and globals](configuration/output-envelope.md), [CLI engine](configuration/cli-engine.md) |
| [Installation & architecture](installation-architecture/installation.md) | [Installation](installation-architecture/installation.md), [architecture](installation-architecture/architecture.md), [testing](installation-architecture/testing.md) |

# Usage

Install with the upstream installer:

```sh
curl -fsSL https://github.com/FriedmanJP/Friedman-cli/raw/main/install.sh | sh
```

Then estimate a VAR on a CSV file:

```sh
friedman estimate multivariate var macro.csv --lags 2
```

Pick a domain from the feature map above for the estimators, command
tables, and worked examples behind each command family.
