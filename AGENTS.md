# AGENTS.md

## Purpose

This document defines agent boundaries, procedures, and quality standards for
anyone, human or AI, contributing to this repository.

Always review this file before making changes. Update it when repository
practices, boundaries, workflows, or tooling expectations change.

## Project Overview

This repository generates an interactive retail sales dashboard from
`data/sales.csv`. The dashboard is built with Python, Pandas, and Plotly.
The output is a single self-contained HTML report named `dashboard.html`.
No web server is required.

## Target Repository

- Primary fork: `Nolos510/isys573-sales-dashboard`
- Upstream/class repository: `samgill172/isys573-sales-dashboard`
- Work should happen in the primary fork unless a human explicitly says
  otherwise.

## Tech Stack

- Python 3.11+
- pandas >= 2.0
- plotly >= 5.18
- pytest >= 7.0

## Build And Test

```bash
# Install dependencies
pip install -r requirements.txt

# Generate dashboard
python dashboard.py

# Run tests
pytest tests/ -v

# Custom output path
python dashboard.py --output report.html
```

## Project Structure

```text
isys573-sales-dashboard/
|-- data/
|   `-- sales.csv          # Source data; never modify without approval
|-- tests/
|   `-- test_dashboard.py  # pytest test suite
|-- dashboard.py           # Main script and dashboard generator
|-- requirements.txt
|-- AGENTS.md              # Canonical agent instructions
`-- .github/
    |-- copilot-instructions.md
    `-- agents/
        `-- test-agent.md  # Custom QA agent
```

## Agent Boundaries

Agents may modify:
- `dashboard.py`
- `tests/`
- `docs/`
- `.github/copilot-instructions.md`
- `AGENTS.md`

Agents must not modify:
- `data/sales.csv`
- generated secrets, API keys, tokens, or credentials
- dependency files such as `requirements.txt` or `pyproject.toml` unless the
  issue explicitly requires it
- unrelated dashboard behavior outside the explicit scope of the issue or
  contribution

Ask first before:
- adding new data sources
- adding external API calls
- changing dependencies
- changing the dashboard from a generated HTML report into a web app

Never:
- push directly to `main`
- modify `data/sales.csv` without explicit human approval
- add a web server such as Flask, FastAPI, or Streamlit
- make unsupported business claims or speculative analytics
- calculate metrics such as "lost revenue" unless the data and issue
  explicitly support that calculation

## GitHub Workflow SOP

Before making changes:
1. Review the latest `AGENTS.md`.
2. Confirm the target repository is `Nolos510/isys573-sales-dashboard`.
3. Confirm the current repository is not the upstream
   `samgill172/isys573-sales-dashboard`.
4. Pull or start from the latest `main` branch.
5. Create a descriptive feature branch from `main`.
6. Do not push directly to `main`.

After making changes:
1. Run the relevant tests.
2. If dashboard behavior changed, generate or verify `dashboard.html`.
3. Summarize changed files, tests run, assumptions made, and any manual
   verification.
4. Open a draft pull request for human review.
5. Do not merge without explicit human approval.
6. Update `AGENTS.md` if repository boundaries or SOPs changed.

## Code Standards

- Follow PEP 8.
- Use simple, readable Python matching the existing project style.
- Use type hints on function signatures.
- Add docstrings for public functions.
- Use `pathlib.Path` for file paths.
- Prefer Pandas and Plotly patterns already present in the repo.
- Keep dashboard output as a single self-contained HTML file.
- Preserve the quarter-filter dropdown functionality.
- Use `plotly.express` or `plotly.graph_objects`; avoid deprecated Plotly APIs.
- Format monetary values for display as `$x,xxx` unless the issue says
  otherwise.

## Data Contract

`data/sales.csv` is the read-only source of truth.

Required columns:
- `date`
- `region`
- `category`
- `product`
- `units_sold`
- `unit_price`
- `discount_pct`
- `revenue`
- `channel`
- `sales_rep`

Column expectations:
- `date`: ISO format, `YYYY-MM-DD`
- `discount_pct`: numeric discount percentage from the CSV
- `revenue`: pre-calculated revenue from the CSV; do not overwrite or infer it

## Testing Requirements

- All new filtering logic must have pytest coverage.
- New dashboard transformations should have focused tests in
  `tests/test_dashboard.py`.
- Existing tests must continue to pass.
- Run `pytest tests/ -v` before opening a PR.
- Run `python dashboard.py` when dashboard generation behavior changes.

## Documentation Expectations

Documentation should be user-friendly and grounded in the actual repo.

Docs should explain:
- what the dashboard does
- how to run the dashboard
- how to run tests
- what each data column means
- what assumptions the dashboard makes
- the expected GitHub workflow for human and agent contributors

Documentation agents must not invent columns, values, commands, or features.

## Agent Fallbacks

If a requested agent workflow is blocked by account, network, rate-limit, or
session restrictions, document the interruption and continue only with an
approved fallback workflow. The fallback should keep the same issue scope,
boundaries, tests, and human review expectations.
