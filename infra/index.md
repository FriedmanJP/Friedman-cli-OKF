# Infra

Model handles, session serving, result rendering, shell completions, and the interactive REPL — the cross-cutting machinery every estimator leaf relies on.

* [Model Handles](model-handles.md) - Inspect (`model info`) and bit-for-bit verify (`model reproduce`) `.jld2`, `.fmod`, and `model://` handles.
* [Serve & Show](serve-show.md) - Expose every leaf as an MCP tool (`serve --mcp`) and render any loadable handle (`show`).
* [REPL & Completions](repl-completions.md) - Interactive session with data injection and result caching, plus `completions bash|fish|zsh` scripts.
