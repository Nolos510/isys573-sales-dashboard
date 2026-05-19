# GitHub Workflow SOP

This SOP describes how human contributors and AI agents (GitHub Copilot,
Claude, or any other automated contributor) make changes to this repository.
It is a practical companion to [`AGENTS.md`](../AGENTS.md); when the two
disagree, `AGENTS.md` wins.

The flow is the same for humans and agents. Agents have additional
boundaries (see section 6) but follow the same branch → PR → review →
merge sequence.

## 1. Repository Targets

- **Primary fork (default working repo):** `Nolos510/isys573-sales-dashboard`
- **Upstream / class repository:** `samgill172/isys573-sales-dashboard`

Per `AGENTS.md`, all work happens in the primary fork unless a human
explicitly says otherwise. Before any change, confirm that `origin` points
at the primary fork and not the upstream:

```bash
git remote -v
```

## 2. Before You Start

For every task, in this order:

1. Read the latest `AGENTS.md`. If anything in `AGENTS.md` contradicts a
   habit you picked up earlier, follow `AGENTS.md`.
2. Confirm the target repository is `Nolos510/isys573-sales-dashboard` and
   that you are not on the upstream class repo.
3. Sync `main`:
   ```bash
   git checkout main
   git pull --ff-only
   ```
4. Create a descriptive branch off `main`. The branch name should hint at
   the change type and scope, for example:
   - `feature/sales-rep-leaderboard`
   - `fix/region-bar-axis`
   - `docs/user-friendly-dashboard-documentation`
   - `tests/discount-impact-coverage`
5. Never push directly to `main` (this rule is in `AGENTS.md` and is
   non-negotiable).

## 3. Making The Change

Scope discipline matters more than speed:

- Stay inside the boundaries declared in `AGENTS.md` → **Agent Boundaries**.
  Agents (and humans collaborating with agents) may modify `dashboard.py`,
  `tests/`, `docs/`, `.github/copilot-instructions.md`, and `AGENTS.md`
  itself. Agents must not modify `data/sales.csv`, dependency files such as
  `requirements.txt` or `pyproject.toml` (unless the issue explicitly
  requires it), secrets, or unrelated dashboard behavior.
- If the issue is documentation-only, restrict your diff to `docs/`. Do not
  edit `dashboard.py`, `tests/`, `data/sales.csv`, `requirements.txt`, or
  `dashboard.html`, even to fix unrelated nits.
- Ask first before adding new data sources, external API calls, dependency
  changes, or any move away from "self-contained HTML report" toward a web
  server (Flask, FastAPI, Streamlit — see `AGENTS.md` → "Never").
- Follow the code standards in `AGENTS.md` (PEP 8, type hints, docstrings,
  `pathlib.Path`, existing Pandas/Plotly patterns, `$x,xxx` money format).
- Preserve the quarter-filter dropdown. Many tests and downstream consumers
  rely on it.

## 4. Before Opening A PR

Run the verification steps that match the kind of change you made.

| Change type | What to run | Why |
|---|---|---|
| Dashboard logic (`dashboard.py`) | `pytest tests/ -v` and `python dashboard.py` | Required by `AGENTS.md`. Re-generates `dashboard.html` so you can eyeball it. |
| Test changes (`tests/`) | `pytest tests/ -v` | Confirms new and existing tests pass. |
| Docs only (`docs/`, `AGENTS.md`, `README.md`) | Render each Markdown file locally and click through internal links | Catches broken relative links and stale references. |
| Dependency changes (requires human approval first) | `pytest tests/ -v` and `python dashboard.py` | Validates the new versions still work end-to-end. |

Also confirm with `git status` and `git diff` that no files outside the
declared scope are staged. For a docs-only change, a one-liner check:

```bash
git diff --name-only main...HEAD | grep -v '^docs/' && echo "OUT OF SCOPE" || echo "ok"
```

## 5. Opening The Pull Request

1. Push the branch to `origin` (the primary fork):
   ```bash
   git push -u origin <branch-name>
   ```
2. Open a **draft** pull request into `main` of
   `Nolos510/isys573-sales-dashboard`. Drafts make it clear that you want
   review, not auto-merge.
3. Write a PR description that includes, at minimum:
   - A short summary of what changed and why.
   - The files added or modified.
   - The verification you ran (tests, dashboard regeneration, manual
     checks).
   - Any assumptions you made.
   - The issue it closes (`Closes #N`), if applicable.
4. Request human review. Agents should never self-approve or merge.

A minimal PR description template:

```markdown
## Summary
<one or two sentences>

## Files Changed
- path/to/file

## Verification
- `pytest tests/ -v` — passed
- `python dashboard.py` — regenerated dashboard.html (if relevant)
- <any manual checks>

## Assumptions
- <anything not obvious from the diff>

## Related Issue
Closes #N
```

## 6. Rules That Apply Specifically To Agents

These come from `AGENTS.md` and are enforced on every agent-authored PR:

- Read `AGENTS.md` before making changes; update it when repository
  practices, boundaries, workflows, or tooling expectations change.
- Do not modify `data/sales.csv` without explicit human approval.
- Do not add a web server (Flask, FastAPI, Streamlit, etc.).
- Do not make unsupported business claims or speculative analytics. For
  example, do not compute "lost revenue" or "discount ROI" — the dataset
  does not support those claims.
- Do not invent columns, values, commands, or features. Documentation
  agents must verify every example against the actual repo.
- Document any fallback used when a tool or service is unavailable, and
  keep the same issue scope, boundaries, tests, and human review
  expectations under the fallback.

When acting as a documentation agent specifically:

- Read `data/sales.csv`, `dashboard.py`, and `tests/test_dashboard.py`
  before writing. Verify column names, function names, chart titles, CLI
  flags, and test class names against the real files.
- New documentation goes under `docs/` as new files. Do not touch code,
  tests, data, dependencies, or generated HTML.

## 7. After Review

1. Address review comments in the same branch with additional commits.
   Force-pushing rewrites history that reviewers have already read; prefer
   additive commits.
2. When the PR is approved, a human merges it. Agents do not merge.
3. If the change altered boundaries, workflow, or tooling expectations,
   update `AGENTS.md` in the same PR or in an immediate follow-up.

## 8. Quick Reference

```bash
# Sync
git checkout main && git pull --ff-only

# New branch
git checkout -b <branch-name>

# Verify scope (docs-only example)
git diff --name-only main...HEAD | grep -v '^docs/' && echo "OUT OF SCOPE" || echo "ok"

# Test
pytest tests/ -v

# Regenerate dashboard (when code changed)
python dashboard.py

# Push and open draft PR
git push -u origin <branch-name>
# then open a draft PR into main on github.com
```

If anything here ever drifts from `AGENTS.md`, fix this SOP — `AGENTS.md` is
the canonical source.
