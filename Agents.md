# Agents.md

## Purpose

This document defines agent boundaries, procedures, and quality standards for anyone (human or AI) contributing to this repository.

**Always review this file before making any changes, and update it as appropriate whenever repository practices change.**

---

## Project Context

- This repository generates an interactive retail sales dashboard from `data/sales.csv`.
- The dashboard is built using Python, Pandas, and Plotly.
- Output is a single self-contained HTML file (`dashboard.html`).

## Agent Boundaries

Agents may modify:
- `dashboard.py`
- `tests/`
- `docs/`
- `.github/copilot-instructions.md`
- `Agents.md` (this file)

Agents must not modify:
- `data/sales.csv`
- Any generated secrets, API keys, tokens, or credentials
- Dependency files (requirements.txt, pyproject.toml, etc.) unless the issue explicitly requires it
- Unrelated dashboard behavior outside the explicit scope of the issue or contribution

## Workflow & Standard Operating Procedure

Before making changes:
1. Confirm the target repository is `Nolos510/isys573-sales-dashboard`.
2. Confirm you are **not** on the upstream `samgill172/isys573-sales-dashboard`.
3. Pull the latest `main` branch.
4. Create a descriptive feature branch from `main`.
5. **Do not** push directly to `main`.

After making changes:
1. Run the relevant tests.
2. If dashboard behavior changed, generate or verify `dashboard.html`.
3. Summarize:
    - Changed files
    - Tests run
    - Assumptions made
4. Open a draft pull request for human review.
5. Do **not** merge without explicit human approval.
6. Update this Agents.md if repository boundaries or SOPs have changed.

## Code Quality Expectations

- Use existing project style and write simple, readable Python.
- Use type hints and docstrings for public functions.
- Prefer Pandas and Plotly patterns already present in the repo.
- Keep dashboard output as a single, self-contained HTML file.
- Add or update tests in `tests/` for any new or changed behavior.
- Avoid unsupported business claims or speculative analytics.

## Documentation Expectations

- All documentation should be user-friendly and reflect the actual repo state.
- Docs must explain:
    - What the dashboard does
    - How to run the dashboard
    - How to run tests
    - What each data column means
    - What assumptions the dashboard makes
- Do **not** invent columns, values, or features not present in the repo.

---

> **Always update and review this file in sync with repo practices. All contributors are required to check Agents.md before any action.**
