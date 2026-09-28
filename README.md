# Friedman-cli-OKF

An [Open Knowledge Format (OKF v0.2)](https://github.com/GoogleCloudPlatform/open-knowledge-format)
knowledge bundle describing every feature and command of
[Friedman-cli](https://github.com/FriedmanJP/Friedman-cli).

## Status

Built 2026-09-28: 39 `type: Feature` concepts across 12 domain
directories covering all 477 CLI leaves, pinned to upstream
Friedman-cli `66bb97e5`. All concepts carry `status: draft` pending
human review.

Browse the rendered bundle at
<https://api.friedman.jp/Friedman-cli-OKF/> — a self-contained
OKF viewer (concept graph + detail panels) built with the vendored
`reference_agent` visualizer from
[open-knowledge-format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
(see [site/vendor/ATTRIBUTION.md](site/vendor/ATTRIBUTION.md)).
Rebuild locally with `python3 site/build.py` (requires `pyyaml`); CI
rebuilds it and deploys to `api.friedman.jp/Friedman-cli-OKF/` on every
`main` push (requires the `API_PAGES_TOKEN` repo secret).

## Layout

This repository is itself the OKF bundle (bundle at repo root):

```text
index.md                  # bundle root index (carries okf_version)
log.md                    # bundle update history
overview.md               # type: Package — what Friedman-cli is
estimate/                 # time-series, regression, regime/volatility, panel
test/                     # unit-root, cointegration, diagnostics, panel/var
impulse/                  # irf, fevd, hd
forecast/                 # forecast, predict, residuals, filter/nowcast
data/                     # handles, simulate, clean
io/                       # tables, classical, networks/mrio
dsge/                     # core, bayes, hadsge, family
causal-policy/            # did, counterfactuals, menus
spectral-filter/          # density, cross-spectra
infra/                    # model handles, serve/show, repl/completions
configuration/            # config files, envelope, cli engine
installation-architecture/ # installation, architecture, testing
scripts/validate_okf.py   # bundle conformance checker (also runs in CI)
```

Each domain directory will have an `index.md`; each feature area will
have one `type: Feature` concept with a command table in the body.

## Sources of truth

- OKF v0.2 specification: <https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md>
- Upstream CLI: <https://github.com/FriedmanJP/Friedman-cli>
- Template bundle: <https://github.com/FriedmanJP/MacroEconometricModels-OKF>

## License

Apache License, Version 2.0 — see [LICENSE](LICENSE).
Copyright 2026 Wookyung Chung.
