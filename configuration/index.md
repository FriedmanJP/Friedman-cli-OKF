# Configuration

Cross-cutting invocation surface with no generated leaves of its own: TOML config files and their `get_*` parsers, global flags, the versioned JSON envelope and exit taxonomy, handle I/O, and the CLI engine itself.

* [Config Files & Schema](config-files.md) - TOML sections, `file < json < --set` merging, `--strict`, and every `get_*` accessor.
* [Handles & Output](output-envelope.md) - Global flags, envelope-v1, exit codes, stems, loaders, and table emitters.
* [CLI Engine & Registry](cli-engine.md) - Command tree, tokenizer, dispatch, help, `CommandSpec` adapter, families, and `schema`.
