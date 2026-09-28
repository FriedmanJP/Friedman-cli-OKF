---
type: Feature
title: Panel, VAR, IV, and DiD tests
description: Panel specification, VAR/PVAR diagnostics, weak-instrument-robust IV inference, and difference-in-differences checks.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/test.md
tags:
  - test
  - panel
  - var
  - granger
  - iv
  - did
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

These 25 leaves cover panel specification (`hausman`, `f-fe`, `breusch-pagan`, `pesaran-cd`, `wooldridge-ar`, `modified-wald`, `pmg-hausman`, `dh-causality`, `panic`), VAR/PVAR specification and comparison (`granger`, `lagselect`, `lm`, `lr`, `stability`, `hansen-j`, `mmsc`, `lagselect`, `stability`), weak-instrument-robust IV inference (`weak-instrument`, `anderson-rubin`, `wild-cluster`), and DiD diagnostics (`bacon`, `pretrend`, `negweight`, `honest`). Panel leaves read long-format CSVs with `--id-col`/`--time-col` (defaulting to the first/second columns); IV leaves share the `estimate regression iv` layout (`--endogenous`, `--instruments`, other numeric columns exogenous with a `const` for the intercept).

Key readings: Hausman and Breusch-Pagan nulls point in opposite directions (rejecting both means fixed effects, not a contradiction); Pesaran-CD rejection invalidates every first-generation panel unit-root p-value on that panel; Granger pairs are directional (`--cause`/`--effect` indices, not names); `lr`/`lm` take two datasets (`data1` restricted, `data2` unrestricted); the inverted Anderson-Rubin set need not be an interval (`bounded|unbounded|disjoint|whole-line|empty`, single endogenous regressor only). Note `test serial breusch-pagan` is grouped here, not with the heteroskedasticity tests, because it is the panel random-effects LM test. The four `test did` leaves carry no `--result`/`--save-result`; all other leaves here do.

LEAVES open question (intermediates): `panel`, `multivariate`, `pvar`, `iv`, and `did` are CLI path segments only — no `##` headers exist for them in the generated reference, so each `###` entry below is counted exactly once.

# Functions

## Panel specification (9 leaves)

| Command | H0 | Output tables |
|---|---|---|
| `friedman test panel hausman` | RE consistent (pick FE on rejection) | `hausman_specification_test` |
| `friedman test panel f-fe` | no fixed effects | `f_test_for_fixed_effects` |
| `friedman test serial breusch-pagan` | no random effects (panel LM) | `breusch_pagan_lm_test` |
| `friedman test panel pesaran-cd` | cross-sectional independence | `pesaran_cd_test` |
| `friedman test panel wooldridge-ar` | no first-order serial correlation | `wooldridge_ar_test` |
| `friedman test panel modified-wald` | homoskedastic FE errors | `modified_wald_test` |
| `friedman test panel pmg-hausman` | long-run homogeneity (PMG/DFE vs MG) | `pmg_hausman_specification_test` |
| `friedman test panel dh-causality` | no causality for any unit | `dumitrescu_hurlin_panel_causality` |
| `friedman test panel panic` | panel unit root (Bai-Ng PANIC) | `panic_test_bai_ng` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `hausman` | `data` (required, long panel) | `--dep`, `--indep`, `--id-col`, `--time-col` |
| `f-fe` | `data` (required, long panel) | `--dep`, `--indep`, `--id-col`, `--time-col` |
| `breusch-pagan` | `data` (required, long panel) | `--dep`, `--indep`, `--id-col`, `--time-col` |
| `pesaran-cd` | `data` (required, long panel) | `--dep`, `--indep`, `--id-col`, `--time-col` |
| `wooldridge-ar` | `data` (required, long panel) | `--dep`, `--indep`, `--id-col`, `--time-col` |
| `modified-wald` | `data` (required, long panel) | `--dep`, `--indep`, `--id-col`, `--time-col` |
| `pmg-hausman` | `data` (required, long panel) | `--id-col`, `--time-col`, `--dep`, `--indep`, `--efficient` (`pmg`: pmg\|dfe), `--trend` (`constant`: none\|constant\|trend), `--p` (1), `--q` (1), `--maxiter` (100), `--tol` (1e-8) |
| `dh-causality` | `data` (required, long panel) | `--id-col`, `--time-col`, `--cause` (required), `--effect` (required), `--p` (1), `--bootstrap` (0), `--seed` (1234) |
| `panic` | `data` (required, T×N) | `--factors` (`auto`), `--method` (`pooled`: pooled\|individual), `--id-col`/`--time-col` (optional) |

## VAR and PVAR diagnostics (9 leaves)

| Command | H0 / role | Output tables |
|---|---|---|
| `friedman test multivariate granger` | no Granger causality (directional) | `granger_causality`, `var_granger_causality_all_pairwise` |
| `friedman test multivariate lagselect` | lag order by IC | `lag_order_selection`, `optimal_lag` |
| `friedman test multivariate lm` | nested VAR restrictions | `lagrange_multiplier_test` |
| `friedman test multivariate lr` | nested VAR restrictions | `likelihood_ratio_test` |
| `friedman test multivariate stability` | companion eigenvalues inside unit circle | `companion_matrix_eigenvalues` |
| `friedman test pvar hansen-j` | valid overidentifying restrictions | `hansen_j_test` |
| `friedman test pvar mmsc` | lag order by Andrews-Lu criteria | `mmsc_results` |
| `friedman test pvar lagselect` | lag order by information criteria | `lag_selection_results` |
| `friedman test pvar stability` | panel companion stability | `panel_var_companion_matrix_eigenvalues` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `granger` | `data` (required) | `--cause` (1), `--effect` (2), `--lags`/`-p` (2), `--rank`/`-r` (`auto`), `--deterministic` (`constant`), `--model` (`vecm`: var\|vecm); flag `--all` (var only) |
| `lagselect` | `data` (required) | `--max-lags` (12), `--criterion` (`aic`: aic\|bic\|hqc) |
| `lm` | `data1`, `data2` (both required) | `--lags1`/`--lags2` (auto) |
| `lr` | `data1`, `data2` (both required) | `--lags1`/`--lags2` (auto) |
| `stability` | `data` (required) | `--lags`/`-p` (auto AIC) |
| `hansen-j` | `data` (required, long panel) | `--id-col`, `--time-col`, `--lags`/`-p` (1) |
| `mmsc` | `data` (required, long panel) | `--id-col`, `--time-col`, `--max-lags` (4), `--criterion` (`bic`: bic\|aic\|hqic) |
| `lagselect` | `data` (required, long panel) | `--id-col`, `--time-col`, `--max-lags` (4), `--criterion` (`bic`: bic\|aic\|hqic) |
| `stability` | `data` (required, long panel) | `--id-col`, `--time-col`, `--lags`/`-p` (1) |

## IV diagnostics (3 leaves)

| Command | H0 / role | Output tables |
|---|---|---|
| `friedman test iv weak-instrument` | strong instruments (F vs Stock-Yogo) | `weak_instrument_diagnostics` |
| `friedman test iv anderson-rubin` | beta = `--beta0` (robust at any strength) | `anderson_rubin_test`, `anderson_rubin_confidence_set`, `anderson_rubin_set_summary` |
| `friedman test iv wild-cluster` | beta_j = `--null` (few-cluster bootstrap) | `wild_cluster_bootstrap` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `weak-instrument` | `data` (required) | `--dep`, `--endogenous` (required), `--instruments` (required), `--cov-type` (`hc1`), `--threshold` (10.0) |
| `anderson-rubin` | `data` (required) | `--dep`, `--endogenous` (required), `--instruments` (required), `--cov-type` (`hc1`: ols\|hc0\|hc1\|hc2\|hc3\|cluster), `--clusters`, `--beta0` (0), `--level` (0.95), `--n-grid` (1001), `--span` (20.0); flag `--no-ci` |
| `wild-cluster` | `data` (required) | `--dep`, `--clusters` (required), `--coefficient`, `--null` (0.0), `--boot-reps` (999), `--boot-weights` (`rademacher`: rademacher\|webb), `--level` (0.95), `--ci-gridpoints` (25), `--enumerate-signs` (`auto`: auto\|yes\|no); flags `--no-impose-null`, `--no-ci` |

## DiD diagnostics (4 leaves)

| Command | Role | Output tables |
|---|---|---|
| `friedman test did bacon` | Goodman-Bacon 2×2 decomposition | `bacon_decomposition_goodman_bacon_2021` |
| `friedman test did pretrend` | joint pre-trend test | `pre_trend_test` |
| `friedman test did negweight` | negative-weight check (dCDH) | `negative_weight_check_de_chaisemartin_d_haultfoeuille_2020`, `weight_details` |
| `friedman test did honest` | HonestDiD sensitivity (Rambachan-Roth) | `honestdid_sensitivity_rambachan_roth_2023` |

| Leaf | Arguments | Key options (default) |
|---|---|---|
| `bacon` | `data` (required, panel) | `--outcome`/`--treatment` (required), `--id-col`, `--time-col`; no `--result`/`--save-result` |
| `pretrend` | `data` (required, panel) | `--outcome`/`--treatment` (required), `--id-col`, `--time-col`, `--leads` (3), `--horizon` (5), `--lags`/`-p` (4), `--cluster` (`unit`: unit\|time\|twoway), `--conf-level` (0.95), `--method` (`did`: did\|event-study), `--did-method` (`twfe`: twfe\|cs\|sa\|bjs\|dcdh); no `--result`/`--save-result` |
| `negweight` | `data` (required, panel) | `--treatment` (required), `--id-col`, `--time-col`; no `--result`/`--save-result` |
| `honest` | `data` (required, panel) | `--outcome`/`--treatment` (required), `--id-col`, `--time-col`, `--mbar` (1.0), `--leads` (3), `--horizon` (5), `--lags`/`-p` (4), `--cluster` (`unit`), `--conf-level` (0.95), `--method` (`did`), `--did-method` (`twfe`); no `--result`/`--save-result` |

# Examples

```bash
friedman test panel hausman sim_panel.csv --dep=y --indep=x1,x2
friedman test serial breusch-pagan sim_panel.csv --dep=y --indep=x1,x2
friedman test panel pesaran-cd sim_panel.csv --dep=y --indep=x1,x2
friedman test multivariate lagselect :denmark --max-lags=4 --criterion=aic
friedman test multivariate granger :denmark --cause=1 --effect=2
friedman test pvar hansen-j sim_pvar.csv --id-col=id --time-col=time --lags=1
friedman test iv weak-instrument sim_iv.csv --dep=y --endogenous=x2 --instruments=z2,z3
friedman test iv anderson-rubin sim_iv.csv --dep=y --endogenous=x2 --instruments=z2,z3
friedman test iv wild-cluster sim_cluster.csv --dep=y --clusters=cluster --coefficient=x2
```

# See also

* [Unit roots and long memory](unit-root.md) - panel unit-root tests used with these panels
* [Regression diagnostics](diagnostics.md) - OLS residual and specification diagnostics
* [Panel and discrete-choice estimation](../estimate/panel-choice.md) - the panel fits under test
* [VAR estimation](../estimate/timeseries.md) - the VAR fits under test
