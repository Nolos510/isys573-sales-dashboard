"""
Tests for ISYS 573 Sales Dashboard
===================================
Run: pytest tests/ -v
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from dashboard import load_data, build_region_bar, build_monthly_line, \
                      build_category_pie, build_top_products, \
                      build_discount_impact, build_discount_kpis, build_html

DATA_PATH = Path(__file__).parent.parent / "data" / "sales.csv"


@pytest.fixture
def df() -> pd.DataFrame:
    return load_data(DATA_PATH)


class TestLoadData:
    def test_loads_without_error(self, df):
        assert len(df) == 500

    def test_required_columns_present(self, df):
        required = {"date", "region", "category", "product",
                    "units_sold", "unit_price", "revenue", "channel",
                    "discount_pct"}
        assert required.issubset(set(df.columns))

    def test_date_parsed_as_datetime(self, df):
        assert pd.api.types.is_datetime64_any_dtype(df["date"])

    def test_quarter_column_added(self, df):
        assert "quarter" in df.columns
        assert set(df["quarter"].unique()).issubset({"Q1", "Q2", "Q3", "Q4"})

    def test_month_column_added(self, df):
        assert "month" in df.columns

    def test_revenue_is_positive(self, df):
        assert (df["revenue"] > 0).all()

    def test_four_regions(self, df):
        assert df["region"].nunique() == 4

    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_data(Path("/nonexistent/path.csv"))

    def test_raises_when_discount_pct_missing(self, tmp_path):
        source = pd.read_csv(DATA_PATH).drop(columns=["discount_pct"])
        csv_path = tmp_path / "missing_discount.csv"
        source.to_csv(csv_path, index=False)

        with pytest.raises(ValueError, match="discount_pct"):
            load_data(csv_path)


class TestRegionChart:
    def test_returns_figure(self, df):
        fig = build_region_bar(df)
        assert fig is not None

    def test_has_four_bars(self, df):
        fig = build_region_bar(df)
        assert len(fig.data) == 1
        assert len(fig.data[0].y) == 4

    def test_filtered_by_quarter(self, df):
        q1 = df[df["quarter"] == "Q1"]
        fig = build_region_bar(q1)
        # Should only show regions present in Q1
        assert len(fig.data[0].x) <= 4


class TestMonthlyChart:
    def test_returns_figure(self, df):
        fig = build_monthly_line(df)
        assert fig is not None

    def test_has_twelve_months_or_fewer(self, df):
        fig = build_monthly_line(df)
        assert len(fig.data[0].x) <= 12

    def test_revenue_values_are_positive(self, df):
        fig = build_monthly_line(df)
        assert all(v > 0 for v in fig.data[0].y)


class TestCategoryChart:
    def test_returns_figure(self, df):
        fig = build_category_pie(df)
        assert fig is not None

    def test_six_categories(self, df):
        fig = build_category_pie(df)
        assert len(fig.data[0].labels) == 6


class TestTopProducts:
    def test_returns_figure(self, df):
        fig = build_top_products(df)
        assert fig is not None

    def test_default_top_10(self, df):
        fig = build_top_products(df)
        assert len(fig.data[0].y) == 10

    def test_custom_n(self, df):
        fig = build_top_products(df, n=5)
        assert len(fig.data[0].y) == 5

    def test_sorted_ascending_for_horizontal_bar(self, df):
        fig = build_top_products(df)
        revenues = list(fig.data[0].x)
        assert revenues == sorted(revenues)


class TestDiscountImpact:
    def test_returns_figure(self, df):
        fig = build_discount_impact(df)
        assert fig is not None

    def test_uses_expected_discount_bands(self):
        sample = pd.DataFrame({
            "discount_pct": [0, 3, 7, 12, 20],
            "revenue": [100, 200, 300, 400, 500],
        })
        fig = build_discount_impact(sample)

        assert list(fig.data[0].x) == ["0%", "0-5%", "5-10%", "10-15%", "15%+"]
        assert list(fig.data[0].y) == [100, 200, 300, 400, 500]

    def test_hover_data_includes_transaction_volume(self, df):
        fig = build_discount_impact(df)

        assert sum(fig.data[0].customdata) == len(df)
        assert "Transactions" in fig.data[0].hovertemplate

    def test_discount_kpis_are_percentages(self, df):
        avg_discount, discounted_transactions = build_discount_kpis(df)

        assert avg_discount.endswith("%")
        assert discounted_transactions.endswith("%")
        assert 0 <= float(avg_discount.rstrip("%")) <= 100
        assert 0 <= float(discounted_transactions.rstrip("%")) <= 100

    def test_discount_chart_and_kpis_respect_quarter_filter(self, df):
        q1 = df[df["quarter"] == "Q1"]
        fig = build_discount_impact(q1)
        avg_discount, discounted_transactions = build_discount_kpis(q1)

        assert sum(fig.data[0].customdata) == len(q1)
        assert avg_discount == f"{q1['discount_pct'].mean():.1f}%"
        assert discounted_transactions == f"{(q1['discount_pct'] > 0).mean() * 100:.1f}%"

    def test_dashboard_html_includes_discount_section(self, df):
        html = build_html(df)

        assert "Discount Impact Analysis" in html
        assert "chartDiscount" in html
        assert "avg_discount" in html
        assert "discounted_transactions" in html
