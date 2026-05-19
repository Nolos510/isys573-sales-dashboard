# Onboarding Guide

Welcome. This guide gets a graduate IS student or new maintainer from a fresh
clone to a generated dashboard, a green test suite, and a working mental model
of the codebase. It is grounded in the actual repository; everything below
matches what is on disk today.

For repository boundaries (what you may and may not modify, and how to open a
PR), read [`AGENTS.md`](../AGENTS.md). For column-level data details, read
[`docs/data_dictionary.md`](data_dictionary.md). For the contribution flow,
read [`docs/github_workflow_sop.md`](github_workflow_sop.md).

## 1. What This Project Is

The repository turns `data/sales.csv` (500 retail transactions from 2024)
into a single self-contained HTML report, `dashboard.html`. The report runs
entirely in the browser — there is no web server. The pipeline is Python +
Pandas + Plotly + a small amount of inline JavaScript for the quarter filter.

The top-level pieces you will touch most often:

- `dashboard.py` — loads the CSV, builds each chart, assembles the HTML.
- `tests/test_dashboard.py` — pytest suite covering the loader and every
  chart function.
- `data/sales.csv` — the read-only source of truth. Do not modify.
- `requirements.txt` — pinned minimum versions of pandas, plotly, pytest.
- `AGENTS.md` — boundaries and SOP for human and agent contributors.

## 2. Prerequisites

- Python 3.11 or newer (`python --version`).
- `pip` available on your `PATH`.
- A modern browser to open the generated HTML.

A virtual environment is recommended but not required.

## 3. Setup

```bash
git clone https://github.com/Nolos510/isys573-sales-dashboard.git
cd isys573-sales-dashboard

# Optional but recommended
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows PowerShell

pip install -r requirements.txt
```

`requirements.txt` pins three packages:

```text
pandas>=2.0
plotly>=5.18
pytest>=7.0
```

## 4. Running the Dashboard

From the repository root:

```bash
python dashboard.py
```

This reads `data/sales.csv`, prints a one-line load summary
(`N rows | N regions | N categories`), and writes `dashboard.html` next to
the script. Open that file in any browser — no server needed.

To write the output somewhere else:

```bash
python dashboard.py --output report.html
```

To point at a different CSV (must match the column contract — see the data
dictionary):

```bash
python dashboard.py --data path/to/other.csv
```

The CLI flags are defined in `dashboard.main()` via `argparse`; `--data`
defaults to `data/sales.csv` and `--output` defaults to `dashboard.html`.

## 5. Running the Tests

```bash
pytest tests/ -v
```

The suite is a single file, `tests/test_dashboard.py`, organized into
classes. Each class focuses on one part of the dashboard:

- `TestLoadData` — `load_data` returns 500 rows, parses `date` as datetime,
  adds the derived `quarter` and `month` columns, keeps `revenue` positive,
  surfaces four regions, and raises clear errors for missing files or a
  missing `discount_pct` column.
- `TestRegionChart` — `build_region_bar` returns a figure, has four bars for
  the full dataset, and respects a quarter-filtered subset.
- `TestMonthlyChart` — `build_monthly_line` returns at most 12 months and
  positive revenue values.
- `TestCategoryChart` — `build_category_pie` returns six categories.
- `TestTopProducts` — `build_top_products` defaults to N=10, accepts a custom
  N, and sorts ascending so the largest bar renders at the top of the
  horizontal layout.
- `TestDiscountImpact` — `build_discount_impact` uses the expected discount
  bands, surfaces transaction counts in hover data, and respects the quarter
  filter; `build_discount_kpis` returns percentage-formatted strings; the
  assembled HTML includes the discount section.

Run `pytest tests/ -v` before opening a PR, per `AGENTS.md`.

## 6. How The Quarter Filter Works

The dropdown labeled **📅 Filter by Quarter** lets the viewer switch among
`Full Year`, `Q1`, `Q2`, `Q3`, and `Q4`. The mechanism is intentionally
simple and runs entirely in the browser:

1. At load time, `dashboard.load_data` adds a derived `quarter` column to the
   DataFrame using `df["date"].dt.quarter.map({1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"})`.
2. `dashboard.build_html` iterates over `["Full Year", "Q1", "Q2", "Q3", "Q4"]`.
   For each quarter it filters the DataFrame (`df` for "Full Year",
   `df[df["quarter"] == q]` otherwise), then calls each chart builder to
   produce a Plotly figure and serializes the figure with `to_json()`.
3. KPI values (Total Revenue, Transactions, Avg Transaction, Top Region, Avg
   Discount, Discounted Transactions) are precomputed for each quarter and
   stored alongside the chart JSON.
4. All five sets of charts + KPIs are embedded in the HTML as a JavaScript
   object. The `applyFilter(quarter)` function in the page reads the right
   slice and calls `Plotly.react(...)` for each chart, plus rewrites the KPI
   row. No new HTTP request is made when the user changes the dropdown.

If a quarter has no rows, the dashboard renders an empty figure with the
title "No data for this period" and KPI placeholders (`$0`, `0`, `—`,
`0.0%`).

## 7. Chart Functions (Cheat Sheet)

All chart builders take a Pandas DataFrame (typically already filtered to a
quarter) and return a `plotly.graph_objects.Figure`.

| Function | Output | What it shows |
|---|---|---|
| `build_region_bar(df)` | Horizontal bar chart | Total revenue per region, sorted ascending so the largest bar appears at the top. Uses a fixed palette. |
| `build_monthly_line(df)` | Line chart with markers | Monthly revenue trend, sorted by `YYYY-MM`. |
| `build_category_pie(df)` | Donut chart (`hole=0.35`) | Revenue share by category. Hover shows revenue and share. |
| `build_top_products(df, n=10)` | Horizontal bar chart | Top N products by total revenue, colored by revenue using a blue scale. |
| `build_discount_impact(df)` | Bar chart | Revenue by discount band, with transaction count surfaced in hover. See section 8. |
| `build_discount_kpis(df)` | `(str, str)` | Average discount and share of discounted transactions, formatted as `"X.X%"`. |
| `kpi_card_html(label, value, color)` | HTML string | Single KPI card. Used inside the assembled page. |
| `build_html(df)` | HTML string | The full self-contained dashboard, including the quarter filter and all five charts. |

## 8. Discount Impact Analysis

The Discount Impact Analysis section is a first-class dashboard feature. It
is generated by `dashboard.build_discount_impact` and is rendered in the
wide chart slot at the bottom of the dashboard (`#chartDiscount`). It is
designed to answer "where are discounts concentrated?" without making
unsupported claims about lost revenue.

How the data is shaped:

- `discount_pct` is coerced to numeric and missing values are filled with 0.
- Transactions are bucketed into five readable bands using
  `pd.cut(..., bins=[-0.001, 0, 5, 10, 15, inf], labels=["0%", "0-5%", "5-10%", "10-15%", "15%+"], include_lowest=True)`.
- Each band's `revenue` is summed and its transaction count is recorded.
- The bar chart plots revenue on the y-axis with the band on the x-axis.
- Hover surfaces both revenue and transaction count via Plotly `customdata`.

Two KPI cards are powered by `build_discount_kpis(df)`:

- **Avg Discount** — the mean of `discount_pct` for the current quarter
  selection, formatted as `"X.X%"`.
- **Discounted Transactions** — the share of rows with `discount_pct > 0`,
  formatted as `"X.X%"`.

Both the chart and the KPIs are recomputed per quarter at build time, so
they update when the dropdown changes (see section 6).

`AGENTS.md` is explicit that "lost revenue" and similar counterfactuals are
not supported by the data; the Discount Impact section is intentionally
descriptive only.

## 9. Where To Go Next

- Read [`docs/data_dictionary.md`](data_dictionary.md) before touching any
  filter, KPI, or chart logic.
- Read [`docs/github_workflow_sop.md`](github_workflow_sop.md) before opening
  a PR — it walks through the human and agent flow described in
  `AGENTS.md`.
- Skim `dashboard.py` end-to-end. The file is short and follows a clear
  load → build-chart → assemble-HTML structure.
