"""Generate EDA summary tables for cleaned Superstore data."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def currency(value: float) -> float:
    return round(float(value), 2)


def run_eda(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    summary = pd.DataFrame(
        [
            {"metric": "total_sales", "value": currency(df["sales"].sum())},
            {"metric": "total_profit", "value": currency(df["profit"].sum())},
            {"metric": "profit_margin_pct", "value": currency(df["profit"].sum() / df["sales"].sum() * 100 if df["sales"].sum() else 0)},
            {"metric": "total_orders", "value": int(df["order_id"].nunique())},
            {"metric": "average_order_value", "value": currency(df["sales"].sum() / df["order_id"].nunique() if df["order_id"].nunique() else 0)},
            {"metric": "customer_count", "value": int(df["customer_id"].nunique())},
            {"metric": "total_quantity_sold", "value": int(df["quantity"].sum())},
        ]
    )
    summary.to_csv(output_dir / "kpi_summary.csv", index=False)

    monthly = (
        df.groupby("order_year_month", dropna=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
        .reset_index()
    )
    monthly["sales_growth_pct"] = monthly["sales"].pct_change().replace([np.inf, -np.inf], np.nan) * 100
    monthly.to_csv(output_dir / "monthly_sales_trends.csv", index=False)

    region = (
        df.groupby("region", dropna=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
        .assign(profit_margin_pct=lambda x: np.where(x["sales"] != 0, x["profit"] / x["sales"] * 100, 0))
        .sort_values("sales", ascending=False)
        .reset_index()
    )
    region.to_csv(output_dir / "region_performance.csv", index=False)

    state_profit = (
        df.groupby(["country", "state"], dropna=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"))
        .sort_values("profit")
        .reset_index()
    )
    state_profit.to_csv(output_dir / "state_profit.csv", index=False)

    category = (
        df.groupby(["category", "sub_category"], dropna=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"), quantity=("quantity", "sum"))
        .sort_values("sales", ascending=False)
        .reset_index()
    )
    category.to_csv(output_dir / "category_revenue.csv", index=False)

    product = (
        df.groupby("product_name", dropna=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"), quantity=("quantity", "sum"), orders=("order_id", "nunique"))
        .sort_values("sales", ascending=False)
        .reset_index()
    )
    product.head(10).to_csv(output_dir / "top_10_products.csv", index=False)
    product[product["profit"] < 0].sort_values("profit").head(25).to_csv(output_dir / "loss_making_products.csv", index=False)

    customer = (
        df.groupby(["customer_id", "customer_name", "segment"], dropna=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
        .assign(avg_order_value=lambda x: np.where(x["orders"] != 0, x["sales"] / x["orders"], 0))
        .sort_values("sales", ascending=False)
        .reset_index()
    )
    customer.to_csv(output_dir / "customer_lifetime_value.csv", index=False)

    discount = (
        df.groupby("discount_band", dropna=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"), avg_discount=("discount", "mean"), orders=("order_id", "nunique"))
        .assign(profit_margin_pct=lambda x: np.where(x["sales"] != 0, x["profit"] / x["sales"] * 100, 0))
        .reset_index()
    )
    discount.to_csv(output_dir / "discount_profitability.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate EDA outputs for Superstore data.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV file.")
    parser.add_argument("--output-dir", required=True, help="Directory for EDA CSV outputs.")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    run_eda(df, Path(args.output_dir))
    print(f"EDA outputs written to {args.output_dir}")


if __name__ == "__main__":
    main()

