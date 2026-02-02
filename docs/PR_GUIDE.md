# PR Guide

This guide helps non-developers create clean pull requests (PRs) with minimal merge risk.

## 1) Decide the base
- Default: branch from `main`.
- If your change depends on another PR, branch from that PR's branch and list the dependency in the PR description.

## 2) Create a branch
Example:
- `docs/guardrails-update`
- `mode-a/refine-template`
- `tests/mode-c-samples`

## 3) Make focused changes
- Keep the change set small and consistent.
- If you change a template, update related samples in `tests/`.
- If you add new terms, update `docs/glossary.md`.

## 4) Manual checks (required)
- Templates: inputs/outputs still match Mode definitions.
- Guardrails: no risky advice or absolute statements.
- Consistency: no contradictions across `docs/` and `scenarios/`.
- Samples: updated when structure changes.

## 5) Commit
- Use short, consistent messages:
  - `docs: update guardrails wording`
  - `mode-b: refine output template`
  - `tests: add mode c sample`

## 6) Push and open PR
- Push your branch to origin.
- Open a PR and fill the template completely.
- If your PR depends on another PR, clearly state it in **Dependencies**.

## 7) Review and merge
- Request at least one reviewer.
- Address feedback promptly.
- Merge in the recommended order if dependencies exist.
