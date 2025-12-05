# Engineering Track: Versioning & Stability

Status: initial stub. Baseline: Python >= 3.14.

- Semantic Versioning: MAJOR.MINOR.PATCH
- Public API:
  - Operator algebra and protocols are stable (>>, |, &, +)
  - Techne modules may evolve with connectors and extras
- Deprecations: no legacy support for <3.14; remove shims aggressively
- Compatibility: rely on numpy >=2.2; optional deps declared via extras
