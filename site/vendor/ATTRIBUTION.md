# Vendored OKF viewer — attribution

The `viewer/` and `bundle/document.py` files in this directory are vendored
from the [open-knowledge-format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
reference agent (Copyright 2026 Google LLC, Apache License 2.0) at upstream
commit `ad30107`, instead of installing the full `reference-agent` package
(which would pull `google-adk` and `google-cloud-bigquery` just to render
the static viewer).

Upstream paths:

- `src/reference_agent/viewer/generator.py`
- `src/reference_agent/viewer/templates/viz.html`
- `src/reference_agent/viewer/static/viz.js`
- `src/reference_agent/viewer/static/viz.css`
- `src/reference_agent/bundle/document.py` (unmodified)

Local patches (each marked with a `FriedmanJP/Friedman-cli-OKF`
comment at the edit site):

`viewer/generator.py`:

1. Import `bundle.document` instead of `reference_agent.bundle.document`
   (vendored layout).
2. `_extract_links` resolves bundle-root-relative (`/...`) links against
   the bundle root so cross-domain links become graph edges; upstream
   skips them.
3. `_TYPE_PALETTE` gains colors for this bundle's `Feature` and `Package`
   types.
4. Nodes carry a `domain` (top-level directory) for the domain filter.
5. `generate_visualization` takes `repo_url` and fills `__BUNDLE_REPO__`
   for per-concept view-source links.

`viewer/templates/viz.html`:

6. Viewport meta tag for narrow screens.
7. Domain-filter `<select>` in the controls.
8. View-source row in the detail panel.
9. `window.BUNDLE_REPO` placeholder.

`viewer/static/viz.js`:

10. CDN-load guard rendering a notice instead of a dead page.
11. Domain filter population and handler.
12. Search covers description and body text (precomputed index).
13. Internal-link rewiring resolves relative (`x.md`, `../x.md`) links
    against the current concept and tolerates `#fragments`; internal
    hrefs use `#/concept/<id>` instead of `javascript:void(0)`.

`viewer/static/viz.css`:

14. `.status-approved` badge style (inherited; this bundle currently
    uses `draft`, for which the upstream `.status-draft` style applies).
15. Responsive stacking of the graph/detail panes below 900px.

Template + `viz.js`:

16. Concentric is the default graph layout (template option order and
    initial Cytoscape layout); cose remains available.
