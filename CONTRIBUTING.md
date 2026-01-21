# Contributing Guide

This repository defines a facilitation AI agent through documents and templates.
Because multiple contributors will work in parallel, follow the rules below to keep
the content consistent, safe, and easy to reuse.

## 1) Scope and goals
- Primary outputs: templates, workflows, and guardrails for Modes A/B/C.
- Priority: usable on-site phrasing, consistent structure, and safety constraints.
- Non-goals: building a full product or providing high-risk expert advice.

## 2) Repository map
- `README.md`: high-level overview and basic flow.
- `docs/`: mission, guardrails, glossary, roadmap, and structure.
- `scenarios/`: mode-specific guides and input/output templates.
- `tests/`: sample inputs and expected outputs (create if missing).
- `.github/`: issue and PR templates.

## 3) Roles and responsibilities
- Maintainer: approves scope changes, guardrails, and roadmap updates.
- Editor: ensures templates and language quality; keeps structure aligned.
- Contributor: proposes changes via PR, adds tests or samples for changes.

## 4) Work workflow (Issues -> Branch -> PR -> Review -> Merge)
1) Open an issue or task describing the problem and target files.
2) Create a branch from `main`.
3) Make changes with minimal, focused commits.
4) Open a PR with context, screenshots or examples if needed.
5) At least one reviewer approves before merge.

## 5) Branch naming
Use short, descriptive branches:
- `docs/guardrails-update`
- `mode-b/live-intervention-template`
- `tests/mode-c-samples`

## 6) Commit message style
Use a simple, consistent prefix:
- `docs: update mode a input template`
- `mode-b: add intervention options`
- `tests: add mode c sample cases`

## 7) PR checklist
- Guardrails still apply and are not violated.
- Inputs and outputs are aligned (Mode A/B/C templates match).
- New terms are added to `docs/glossary.md`.
- Related docs are updated if meaning changes.
- Samples/tests are added or updated when structure changes.

## 8) Content rules (critical)
- Do not exceed the scope of provided inputs.
- Mark assumptions explicitly when required.
- Keep outputs usable as "ready-to-read" facilitator language.
- Maintain the exact output structure in templates (order and headings).
- Provide A/B/C options when the template requires choices.

## 9) Writing style guide
- Use short, clear Korean sentences.
- Prefer lists and numbered steps for operational clarity.
- Avoid vague verbs (e.g., "support") without concrete actions.
- Keep terminology consistent with `docs/glossary.md`.
- Avoid personal judgement about participants or stakeholders.
- For full writing rules, see `docs/style_guide.md`.

## 10) Testing and validation
There is no automated test runner yet. Use these manual checks:
- Template integrity: inputs/outputs still match Mode definitions.
- Guardrails: no risky advice or absolute statements.
- Consistency: no contradictions across `docs/` and `scenarios/`.
- Samples: if a template changes, add or update a sample in `tests/`.

## 11) Release and change management
- For major changes, update `README.md` and `docs/phase_plan.md`.
- Add a short "What changed" section in the PR description.
- If a change affects public usage, update the relevant mode README.

## 12) Suggested issue template (copy/paste)
Title: [Mode/Doc] Short summary
Body:
- Problem:
- Proposed change:
- Affected files:
- Risks/assumptions:

## 13) Suggested PR template (copy/paste)
Summary:
- What changed:
- Why:
- Related issue:

Checklist:
- [ ] Guardrails respected
- [ ] Templates aligned
- [ ] Glossary updated (if needed)
- [ ] Samples/tests updated (if needed)
