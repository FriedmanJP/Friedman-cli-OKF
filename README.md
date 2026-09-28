# Friedman-cli-OKF

An [Open Knowledge Format (OKF v0.2)](https://github.com/GoogleCloudPlatform/open-knowledge-format)
knowledge bundle describing every feature and command of
[Friedman-cli](https://github.com/FriedmanJP/Friedman-cli).

## Status

Scaffolding. Deep research into upstream `Friedman-cli` in progress;
bundle directories will mirror the CLI's command tree once the
research phase lands.

## Layout (planned)

This repository will itself be the OKF bundle (bundle at repo root),
following the structure of
[MacroEconometricModels-OKF](https://github.com/FriedmanJP/MacroEconometricModels-OKF):

```text
index.md                  # bundle root index (carries okf_version)
log.md                    # bundle update history
overview.md               # type: Package — what Friedman-cli is
<domain>/                 # one directory per CLI command area
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
