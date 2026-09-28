---
type: Feature
title: Cointegration and stability tests
description: Johansen, residual-based, panel, and bounds cointegration tests, VECM restriction tests, break tests, and bubble detectors.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/test.md
tags:
  - test
  - cointegration
  - vecm
  - structural-breaks
  - bubbles
status: draft
stale_after: 2026-12-27T00:00:00Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:57:55Z
sources:
  - id: generated-test
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/test.md
    title: Generated test reference (option and output tables)
  - id: guide-test
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/test.md
    title: test guide (null hypotheses, decision logic, pitfalls)
  - id: src-test
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/test.jl
    title: test command implementation
---

# Summary

These 27 leaves test long-run relationships (`coint` system, residual-based, panel, and bounds tests; `vecm` restriction tests; `nardl-symmetry`; `park-added`) and parameter stability (`stability` break, CUSUM, factor-break, bubble, and cointegration-stability tests). Every leaf takes a required `data` CSV plus `--format`/`-f`, `--output`/`-o`, `--result`, `--save-result`, except `stability nyblom` and `stability recursive-residuals`, which omit `--result`/`--save-result`.

Null directions vary and must be read per leaf: cointegration tests use H0 of no cointegration (low p supports a relationship), the bounds test has no p-value at all (F/t against I(0)/I(1) bands), VECM leaves test H0 that the economic restriction holds, and `hansen-instability`/`park-added` test H0 of stable/genuine cointegration. CUSUM leaves report a path-plus-band verdict, not a p-value; Nyblom reports statistics against Hansen 5% critical values. VECM restriction matrices live in a `[vecm_restriction]` TOML section, row-major (`H` p×s with s ≥ r; `b` p×r with exactly r columns).

LEAVES open question (intermediates): `coint`, `vecm`, and `stability` are CLI path segments only — no `##` headers exist for them in the generated reference, so each `###` entry below is counted exactly once.

# Functions

## Cointegration (9 leaves)

| Command | H0 | Output tables |
|---|---|---|
| `friedman test coint johansen` | rank ≤ r (trace and max-eigenvalue) | `johansen_trace_test`, `johansen_max_eigenvalue_test` |
| `friedman test coint engle-granger` | no cointegration | `engle_granger_test` |
| `friedman test coint phillips-ouliaris` | no cointegration (Z_t, Z_alpha) | `phillips_ouliaris_test`, `phillips_ouliaris_summary` |
| `friedman test coint gregory-hansen` | no cointegration with one shift | `gregory_hansen_test` |
| `friedman test coint ardl-bounds` | no level relationship (bounds, no p-value) | `ardl_bounds_test_i_0_i_1_bounds_no_p_value`, `ardl_bounds_test_summary` |
| `friedman test coint kao` | no panel cointegration | `kao_cointegration`, `kao_cointegration_summary` |
| `friedman test coint pedroni` | no panel cointegration | `pedroni_cointegration`, `pedroni_cointegration_summary` |
| `friedman test coint westerlund` | no panel error correction | `westerlund_cointegration`, `westerlund_cointegration_summary` |
| `friedman test coint fisher-johansen` | no panel cointegration (combined ranks) | `fisher_johansen_panel_cointegration_test`, `fisher_johansen_summary` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `johansen` | `data` (required) | `--lags`/`-p` (2), `--trend` (`constant`: none\|constant\|trend) |
| `engle-granger` | `data` (required) | `--dep`, `--trend` (`constant`: none\|constant\|trend), `--lags` (`aic`: aic\|bic\|tstat\|N), `--max-lags` |
| `phillips-ouliaris` | `data` (required) | `--dep`, `--trend` (`constant`), `--kernel` (`bartlett`: bartlett\|parzen\|qs\|tukey-hanning), `--bandwidth` (`nw`: nw\|andrews\|nw94\|number) |
| `gregory-hansen` | `data` (required) | `--model` (`C`: C\|C/T\|C/S), `--lags` (`aic`: aic\|bic\|N), `--max-lags` (auto), `--trim` (0.15) |
| `ardl-bounds` | `data` (required) | `--dep`, `--p`/`--q` (`auto`), `--max-p`/`--max-q` (4), `--ic` (`aic`: aic\|bic), `--trend` (`none`: none\|const\|trend), `--case` (3, PSS 1..5), `--level` (0.05: 0.10\|0.05\|0.025\|0.01), `--cv-source` (`pss`) |
| `kao` | `data` (required, long panel) | `--id-col`, `--time-col`, `--dep`, `--indep` |
| `pedroni` | `data` (required, long panel) | `--id-col`, `--time-col`, `--dep`, `--indep`, `--trend` (`constant`: constant\|trend) |
| `westerlund` | `data` (required, long panel) | `--id-col`, `--time-col`, `--dep`, `--indep`, `--trend` (`constant`) |
| `fisher-johansen` | `data` (required, long panel) | `--id-col`, `--time-col`, `--vars` (≥2 series), `--deterministic` (`constant`: none\|constant\|trend), `--lags` (2), `--combine` (`mw`: mw\|choi) |

## VECM restrictions and relatives (7 leaves)

| Command | H0 | Output tables |
|---|---|---|
| `friedman test vecm beta` | beta = H·phi | `vecm_restriction_h` |
| `friedman test vecm alpha` | alpha = A·psi | `vecm_restriction_a` |
| `friedman test vecm joint` | joint beta and alpha restriction | `vecm_joint_h_a` |
| `friedman test vecm known-beta` | beta = b (fully specified) | `vecm_known_b` |
| `friedman test vecm weak-exog` | weak exogeneity of `--vars` | `vecm_weak_exogeneity` |
| `friedman test nardl-symmetry` | long/short-run symmetry (per regressor) | `nardl_symmetry_tests_h0_long_run_short_run`, `nardl_symmetry_test_summary` |
| `friedman test park-added` | genuine cointegration (H(p,q)) | `park_added_variables_test` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `beta` | `data` (required) | `--config` ([vecm_restriction] H), `--lags`/`-p` (2), `--rank`/`-r` (`auto`), `--deterministic` (`constant`), `--method` (`johansen`: johansen\|engle_granger), `--significance` (0.05) |
| `alpha` | `data` (required) | `--config` ([vecm_restriction] A), `--lags`/`-p` (2), `--rank`/`-r` (`auto`), `--deterministic` (`constant`), `--method` (`johansen`), `--significance` (0.05) |
| `joint` | `data` (required) | `--config` (H and A matrices), `--lags`/`-p` (2), `--rank`/`-r` (`auto`), `--deterministic` (`constant`), `--method` (`johansen`), `--significance` (0.05) |
| `known-beta` | `data` (required) | `--config` ([vecm_restriction] b), `--lags`/`-p` (2), `--rank`/`-r` (`auto`), `--deterministic` (`constant`), `--method` (`johansen`), `--significance` (0.05) |
| `weak-exog` | `data` (required) | `--vars` (names/indices, no config), `--lags`/`-p` (2), `--rank`/`-r` (`auto`), `--deterministic` (`constant`), `--method` (`johansen`), `--significance` (0.05) |
| `nardl-symmetry` | `data` (required) | `--dep`, `--asymmetric` (`all` or indices), `--p`/`--q` (`auto`), `--max-p`/`--max-q` (4), `--ic` (`aic`), `--case` (3) |
| `park-added` | `data` (required) | `--dep`, `--method` (`fmols`: fmols\|ccr\|dols), `--trend` (`const`: none\|const\|linear), `--kernel`/`--bandwidth` (fit HAC), `--leads`/`--lags` (`auto`), `--q-add` (2, test df), `--hac-kernel`/`--hac-bandwidth` (test HAC) |

## Stability and breaks (11 leaves)

| Command | H0 | Output tables |
|---|---|---|
| `friedman test stability chow` | constant coefficients at break(s) | `chow_test` |
| `friedman test stability andrews` | no break at unknown date | `andrews_break_test` |
| `friedman test stability bai-perron` | m breaks selected by IC | `bai_perron_test` |
| `friedman test stability cusum` | stability (path stays in band) | `cusum_path`, `cusum_summary` |
| `friedman test stability cusumsq` | variance stability (path in band) | `cusumsq_path`, `cusumsq_summary` |
| `friedman test stability recursive-residuals` | — (reports the residuals) | `recursive_residuals`, `recursive_residuals_summary` |
| `friedman test stability factor-break` | stable factor loadings | `factor_break_test`, `per_series_break_diagnostics` |
| `friedman test stability sadf` | unit root vs one bubble | `explosive_episodes_sadf`, `sadf_summary` |
| `friedman test stability gsadf` | unit root vs multiple bubbles | `explosive_episodes_gsadf`, `gsadf_summary` |
| `friedman test stability hansen-instability` | stable cointegration (L_c) | `hansen_instability_test` |
| `friedman test stability nyblom` | stable GARCH parameters | `nyblom_individual_stability`, `nyblom_joint_stability` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `chow` | `data` (required) | `--dep`, `--cov-type` (`hc1`), `--break-at` (required index or list), `--type` (`breakpoint`: breakpoint\|forecast), `--level` (0.05) |
| `andrews` | `data` (required) | `--response` (1), `--test` (`supwald`: sup/exp/mean × wald/lr/lm), `--trimming` (0.15) |
| `bai-perron` | `data` (required) | `--response` (1), `--max-breaks` (5), `--trimming` (0.15), `--criterion` (`bic`: bic\|lwz) |
| `cusum` | `data` (required) | `--dep`, `--cov-type` (`hc1`), `--level` (0.05) |
| `cusumsq` | `data` (required) | `--dep`, `--cov-type` (`hc1`), `--level` (0.05) |
| `recursive-residuals` | `data` (required) | `--dep`, `--cov-type` (`hc1`); no `--result`/`--save-result` |
| `factor-break` | `data` (required, T×N) | `--factors` (2), `--method` (`breitung_eickmeier`: breitung_eickmeier\|chen_dolado_gonzalo\|han_inoue), `--id-col`/`--time-col` (optional) |
| `sadf` | `data` (required) | `--column`/`-c` (1), `--r0` (`auto`), `--adflag` (0), `--mc-reps` (999), `--cv` (`asymptotic`: asymptotic\|wildboot), `--seed` (20240716) |
| `gsadf` | `data` (required) | `--column`/`-c` (1), `--r0` (`auto`), `--adflag` (0), `--mc-reps` (999), `--cv` (`asymptotic`), `--seed` (20240716) |
| `hansen-instability` | `data` (required) | `--dep`, `--method` (`fmols`), `--trend` (`const`), `--kernel` (`bartlett`), `--bandwidth` (`andrews`), `--leads`/`--lags` (`auto`) |
| `nyblom` | `data` (required) | `--column`/`-c` (1), `--model` (`garch`: garch\|egarch\|gjr-garch), `--p`/`--q` (1); no `--result`/`--save-result` |

# Examples

```bash
friedman test coint johansen :denmark --lags=2 --trend=constant
friedman test coint engle-granger :denmark --dep=LRM --lags=aic
friedman test coint ardl-bounds :denmark --dep=LRM --p=1 --q=1 --case=3 --level=0.05
friedman test vecm weak-exog :denmark --vars=IDE --rank=1
friedman test nardl-symmetry :denmark --dep=LRM --asymmetric=all --p=1 --q=1
friedman test stability andrews :denmark --response=1 --test=supwald --trimming=0.15
friedman test stability bai-perron :denmark --response=1 --max-breaks=5
friedman test stability chow :stackloss --dep=stack.loss --break-at=10
```

# See also

* [Unit roots and long memory](unit-root.md) - integration-order pre-tests
* [Regression diagnostics](diagnostics.md) - OLS residual and specification diagnostics
* [VECM estimation](../estimate/timeseries.md) - fitting the cointegrated system under test
