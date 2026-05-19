# Data Dictionary — `data/sales.csv`

This document describes every column in `data/sales.csv`, the read-only source
of truth for the ISYS 573 retail sales dashboard. All values below were
verified directly against the CSV in this repository (500 transactions across
calendar year 2024).

`data/sales.csv` must not be modified without explicit human approval (see
[`AGENTS.md`](../AGENTS.md)).

## Dataset At A Glance

| Property | Value |
|---|---|
| File path | `data/sales.csv` |
| Row count | 500 transactions (one row per transaction) |
| Column count | 10 |
| Date range | 2024-01-01 through 2024-12-30 |
| Regions | 4 (East, Midwest, South, West) |
| Categories | 6 (Apparel, Beauty, Electronics, Home & Garden, Sports, Toys) |
| Channels | 3 (In-Store, Online, Wholesale) |
| Distinct products | 48 |
| Distinct sales reps | 10 |
| Header row | Yes, first line |
| Encoding | UTF-8 |
| Delimiter | Comma |

## Columns

The columns appear in the CSV in the order shown below. The "Required by"
column lists the load-time validation in `dashboard.load_data` — every column
marked **load_data** must be present or the loader raises `ValueError`.

| # | Column | Data type (Pandas) | Description | Example value | Required by |
|---|---|---|---|---|---|
| 1 | `date` | `datetime64[ns]` (parsed from `YYYY-MM-DD`) | Calendar date of the transaction. Parsed via `pd.read_csv(..., parse_dates=["date"])`. Used to derive `quarter` (Q1–Q4) and `month` (`YYYY-MM`) at load time. | `2024-01-01` | load_data |
| 2 | `region` | `object` (string) | U.S. sales region. One of: `East`, `Midwest`, `South`, `West`. | `West` | load_data |
| 3 | `category` | `object` (string) | Product category. One of: `Apparel`, `Beauty`, `Electronics`, `Home & Garden`, `Sports`, `Toys`. | `Sports` | load_data |
| 4 | `product` | `object` (string) | Specific product name. 48 distinct values in the dataset (e.g., `Gym Bag`, `Scented Candle`, `Building Blocks`, `Wool Socks`, `Nail Polish Kit`). | `Gym Bag` | load_data |
| 5 | `units_sold` | `int64` | Number of units sold in the transaction. Observed range in the data: 1–50. | `47` | load_data |
| 6 | `unit_price` | `float64` | List price per unit, in U.S. dollars before discount. Observed range in the data: `9.90`–`349.85`. | `152.09` | load_data |
| 7 | `discount_pct` | `int64` | Discount applied to the transaction, expressed as a whole-number percent. Observed values in the data: `0`, `5`, `10`, `15`, `20`. Used as-is by `dashboard.build_discount_impact` and `dashboard.build_discount_kpis`; do not interpret it as a fraction. | `0` | load_data |
| 8 | `revenue` | `float64` | Pre-calculated transaction revenue in U.S. dollars. **Treat as authoritative — `AGENTS.md` requires that revenue not be overwritten or re-derived.** Observed range in the data: `19.11`–`16,234.78`. | `7148.23` | load_data |
| 9 | `channel` | `object` (string) | Sales channel. One of: `In-Store`, `Online`, `Wholesale`. | `In-Store` | load_data |
| 10 | `sales_rep` | `object` (string) | Name of the sales representative who closed the transaction. 10 distinct reps in the dataset (`Alice Monroe`, `Bob Chen`, `Carlos Rivera`, `Diana Park`, `Edward Walsh`, `Fiona Grant`, `George Osei`, `Hannah Kim`, `Ivan Petrov`, `Julia Santos`). | `Hannah Kim` | — |

`sales_rep` is present in the CSV but is not in the required-columns set that
`load_data` validates. It is still loaded into the DataFrame and is available
for future analyses.

## Derived Columns

The loader (`dashboard.load_data`) adds two columns after reading the CSV.
They are not part of the source file but are present on every DataFrame
returned by the loader.

| Column | Data type | Description | Example value |
|---|---|---|---|
| `quarter` | `object` (string) | Calendar quarter of the `date`, mapped from `date.dt.quarter` to `"Q1" / "Q2" / "Q3" / "Q4"`. Drives the dashboard's quarter-filter dropdown. | `Q1` |
| `month` | `object` (string) | Year-month period of the `date`, formatted as `YYYY-MM` via `date.dt.to_period("M").astype(str)`. Drives the monthly revenue trend line. | `2024-01` |

## Example Rows

The five rows below are copied verbatim from the top of `data/sales.csv`:

```csv
date,region,category,product,units_sold,unit_price,discount_pct,revenue,channel,sales_rep
2024-01-01,West,Sports,Gym Bag,47,152.09,0,7148.23,In-Store,Hannah Kim
2024-01-03,Midwest,Home & Garden,Scented Candle,49,272.77,0,13365.73,In-Store,Bob Chen
2024-01-04,West,Toys,Building Blocks,15,31.97,0,479.55,In-Store,Bob Chen
2024-01-04,East,Apparel,Wool Socks,5,57.37,0,286.85,Online,Ivan Petrov
2024-01-04,East,Apparel,Wool Socks,5,57.37,0,286.85,Online,Ivan Petrov
```

## Conventions And Caveats

- The CSV is the read-only source of truth. Aggregations (totals, averages,
  category shares) are recomputed at runtime by `dashboard.py` from this file.
- `revenue` is taken from the CSV directly. The dashboard never recomputes it
  from `units_sold × unit_price × (1 - discount_pct/100)`; that calculation is
  out of scope and `AGENTS.md` explicitly forbids overwriting `revenue`.
- `discount_pct` is a percent, not a fraction. A value of `20` means a 20%
  discount.
- "Revenue" in the dashboard always means the sum of the `revenue` column for
  the current quarter selection. Claims like "lost revenue" or "what revenue
  could have been without discounts" are not supported by this dataset and
  must not be invented (see `AGENTS.md` → "Never").
