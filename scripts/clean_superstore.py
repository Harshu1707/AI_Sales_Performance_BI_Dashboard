"""Clean and prepare Kaggle Superstore data for BI analysis."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "ship_date",
    "customer_id",
    "customer_name",
    "segment",
    "region",
    "country",
    "state",
    "city",
    "category",
    "sub_category",
    "product_name",
    "sales",
    "quantity",
    "discount",
    "profit",
    "shipping_cost",
]


COLUMN_ALIASES = {
    "sub-category": "sub_category",
    "subcategory": "sub_category",
    "shipping cost": "shipping_cost",
    "ship cost": "shipping_cost",
    "order id": "order_id",
    "order date": "order_date",
    "ship date": "ship_date",
    "customer id": "customer_id",
    "customer name": "customer_name",
    "product name": "product_name",
}


def snake_case(value: str) -> str:
    value = value.strip().lower()
    value = COLUMN_ALIASES.get(value, value)
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return re.sub(r"_+", "_", value).strip("_")


def read_dataset(input_path: Path) -> pd.DataFrame:
    suffix = input_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(input_path, encoding="utf-8-sig")
    if suffix in {".xls", ".xlsx"}:
        return pd.read_excel(input_path)
    raise ValueError(f"Unsupported file type: {suffix}")


def clean_superstore(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [snake_case(str(col)) for col in df.columns]

    if "shipping_cost" not in df.columns:
        df["shipping_cost"] = 0.0

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            df[column] = np.nan

    df = df.drop_duplicates()

    text_columns = [
        "order_id",
        "customer_id",
        "customer_name",
        "segment",
        "region",
        "country",
        "state",
        "city",
        "category",
        "sub_category",
        "product_name",
    ]
    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()
        df[column] = df[column].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

    for column in ["order_date", "ship_date"]:
        df[column] = pd.to_datetime(df[column], errors="coerce", dayfirst=False)

    numeric_columns = ["sales", "quantity", "discount", "profit", "shipping_cost"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["sales"] = df["sales"].fillna(0).clip(lower=0)
    df["quantity"] = df["quantity"].fillna(0).clip(lower=0).round().astype(int)
    df["discount"] = df["discount"].fillna(0).clip(lower=0)
    df["profit"] = df["profit"].fillna(0)
    df["shipping_cost"] = df["shipping_cost"].fillna(0).clip(lower=0)

    for column in text_columns:
        df[column] = df[column].fillna("Unknown")

    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.month
    df["order_month_name"] = df["order_date"].dt.strftime("%b")
    df["order_year_month"] = df["order_date"].dt.to_period("M").astype("string")
    df["ship_days"] = (df["ship_date"] - df["order_date"]).dt.days
    df["profit_margin"] = np.where(df["sales"] != 0, df["profit"] / df["sales"], 0)
    df["discount_band"] = pd.cut(
        df["discount"],
        bins=[-0.01, 0, 0.1, 0.2, 0.3, 1],
        labels=["No Discount", "0-10%", "10-20%", "20-30%", "30%+"],
    ).astype("string")
    df["is_profitable"] = df["profit"] > 0

    df = df.sort_values(["order_date", "order_id", "product_name"]).reset_index(drop=True)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean Kaggle Superstore data.")
    parser.add_argument("--input", required=True, help="Path to raw CSV/XLS/XLSX file.")
    parser.add_argument("--output", required=True, help="Path for cleaned CSV output.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cleaned = clean_superstore(read_dataset(input_path))
    cleaned.to_csv(output_path, index=False)

    print(f"Rows: {len(cleaned):,}")
    print(f"Columns: {len(cleaned.columns):,}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()

