---
type: Feature
title: Serve (MCP) and Show (handle rendering)
description: Serve every registry leaf as a Model Context Protocol tool over stdio, and render any loadable data/model/result handle with show.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/serve.md
tags:
  - infra
  - mcp
  - serve
  - show
  - handles
status: draft
stale_after: 2026-12-27T16:56:53Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:56:53Z
sources:
  - id: generated-serve
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/serve.md
    title: Generated serve reference (1 leaf)
  - id: generated-show
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/show.md
    title: Generated show reference (1 leaf)
  - id: src-serve
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/serve.jl
    title: MCP JSON-RPC server implementation
  - id: src-show
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/show.jl
    title: show handle renderer
---

# Summary

`friedman serve` is a singleton leaf (no subcommands) that projects the whole registry as MCP tools: `tools/list` mirrors every leaf with its draft-07 `inputSchema`, and `tools/call` reconstructs an argv, runs it through `run_cli` with `--format json` forced, and returns the JSON envelope verbatim as text content (`isError` on nonzero exit). `friedman show` is the read side of the handle system: it resolves one stem and renders whatever it holds — descriptive statistics for data containers, `long_table`/`DataFrame`/field dump for models and results, keys-only table for bundles.

# Functions

| Leaf | Summary | Output tables |
|---|---|---|
| `friedman serve` | Serve every command as an MCP tool over stdio (`--mcp`) | none (stdout is the JSON-RPC channel) |
| `friedman show` | Render any loadable handle (data, model, or result) | `show_payload`, `show_summary` |

`serve` flags (no arguments, no options):

| Flag | Short | Description |
|---|---|---|
| `--mcp` | — | MCP server: JSON-RPC 2.0 on stdio; tools/list mirrors the registry, tools/call returns the JSON envelope verbatim |

`show` arguments:

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | `String` | yes | Handle stem or path |

`show` options:

| Option | Short | Type | Default | Choices | Description |
|---|---|---|---|---|---|
| `--output` | `-o` | `String` | `""` | — | Write to file instead of stdout |
| `--format` | `-f` | `String` | `table` | `table`, `csv`, `json` | table\|csv\|json |
| `--plot-save` | — | `String` | `""` | — | Save interactive plot to HTML file |

`show` flags:

| Flag | Short | Description |
|---|---|---|
| `--plot` | — | Open interactive plot if a recipe exists |

Behavior notes (from source):

- `serve` without `--mcp` is `usage/missing` (exit 2); `--mcp` is the only supported mode. The server speaks line-delimited JSON-RPC 2.0 (`initialize`, `tools/list` with optional `prefix` filter, `tools/call`, `ping`); `serve` itself is excluded from the tool list. Request handling is serial.
- MCP argv reconstruction: positionals in declared order (stops at the first absent one), then options as `--name value`, then flags when `true`; unknown keys are passed through so the strict parser answers with its typed did-you-mean error.
- The session `model://` store lives exactly as long as the serve loop; each tool call runs under stdout redirection to a tempfile (Julia 1.13 has no `redirect_stdout(IOBuffer)`) while responses go to the `output` IO captured at loop start.
- `show` resolves via `resolve_stem(; slot=:result)`: `STEM.jld2` if it exists, else the exact path — no CSV fallback. `:timeseries`/`:panel`/`:cross_section` emit descriptive stats; `:io` and other kinds fall through to `long_table`/`DataFrame`/field dump (never `to_matrix` on IO data). `--plot`/`--plot-save` call `_maybe_plot`; a missing recipe is `model/unsupported` (exit 5).

# Examples

```bash
friedman serve --mcp
friedman show var
friedman show irf --format json
friedman show macro --plot --plot-save macro.html
```

# See also

* [Model Handles](model-handles.md) - header inspection and bit-for-bit verification of the same handles
* [REPL & Completions](repl-completions.md) - interactive alternative to the serve session
* [CLI Engine](../configuration/cli-engine.md) - registry, `schema`, and the dispatch pipeline behind MCP
