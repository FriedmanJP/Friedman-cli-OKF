---
type: Reference
title: Bundle update log
description: Chronological history of changes to this OKF bundle.
---

# Update log

## 2026-09-28

- Initial bundle (draft): Feature concepts covering all 477 CLI leaves
  across 12 domains, pinned to upstream Friedman-cli `66bb97e5`.
  All concepts carry `status: draft` pending human review.
- Vendored the OKF reference-agent viewer (upstream `ad30107`) with the
  template's 16 local patches; added `scripts/validate_okf.py` and the
  `okf-validate` / `site` CI workflows.
