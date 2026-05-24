from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_DATASET = ROOT / "data" / "raw" / "superstore.csv"

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "data"

ACTIVE_UPLOAD = UPLOAD_DIR / "uploaded_superstore.csv"


def load_superstore(path: str | Path | None = None) -> pd.DataFrame:

    dataset_path = (
        Path(path)
        if path
        else (ACTIVE_UPLOAD if ACTIVE_UPLOAD.exists() else DEFAULT_DATASET)
    )

    df = pd.read_csv(dataset_path)

    # Clean columns
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    print("Loaded Columns:", df.columns.tolist())

    # Convert date column
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    # Numeric columns
    numeric_cols = [
        "sales",
        "profit",
        "discount",
        "quantity"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)
        else:
            df[col] = 0

    return df.dropna(subset=["order_date"])


def save_uploaded_dataset(file: FileStorage) -> str:

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    filename = secure_filename(
        file.filename or "uploaded_superstore.csv"
    )

    if not filename.lower().endswith(".csv"):
        raise ValueError("Only CSV files are supported.")

    file.save(ACTIVE_UPLOAD)

    return str(ACTIVE_UPLOAD)


def money(value: float) -> float:
    return round(float(value), 2)


def records(frame: pd.DataFrame, *cols: str) -> list[dict[str, Any]]:

    return (
        frame.loc[:, cols]
        .replace({np.nan: None})
        .to_dict(orient="records")
    )


def build_kpi_payload(df: pd.DataFrame) -> dict[str, Any]:

    total_sales = df["sales"].sum()

    total_profit = df["profit"].sum()

    orders = (
        df["order_id"].nunique()
        if "order_id" in df.columns
        else len(df)
    )

    customers = (
        df["customer_id"].nunique()
        if "customer_id" in df.columns
        else 0
    )

    monthly = (
        df.set_index("order_date")
        .resample("ME")["sales"]
        .sum()
    )

    growth = 0

    if len(monthly) >= 2 and monthly.iloc[-2] != 0:
        growth = (
            (monthly.iloc[-1] - monthly.iloc[-2])
            / monthly.iloc[-2]
        ) * 100

    return {
        "totalSales": money(total_sales),
        "totalProfit": money(total_profit),
        "profitMargin": round(
            (total_profit / total_sales) * 100,
            2
        ) if total_sales else 0,
        "averageOrderValue": money(
            total_sales / orders
        ) if orders else 0,
        "customerCount": int(customers),
        "totalOrders": int(orders),
        "salesGrowth": round(float(growth), 2),
    }


def build_chart_payload(df: pd.DataFrame) -> dict[str, Any]:

    monthly = (
        df.set_index("order_date")
        .resample("ME")
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum")
        )
        .reset_index()
    )

    monthly["month"] = monthly["order_date"].dt.strftime(
        "%b %Y"
    )

    region = (
        df.groupby("region", as_index=False)
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum")
        )
    )

    category = (
        df.groupby("category", as_index=False)
        .agg(
            profit=("profit", "sum"),
            sales=("sales", "sum")
        )
    )

    products = (
        df.groupby("product_name", as_index=False)
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum")
        )
        .sort_values("sales", ascending=False)
        .head(10)
        .rename(columns={"product_name": "product"})
    )

    segment = (
        df.groupby("segment", as_index=False)
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum")
        )
    )

    state = (
        df.groupby("state", as_index=False)
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum")
        )
        .sort_values("sales", ascending=False)
        .head(18)
    )

    scatter = df.sample(
        min(500, len(df)),
        random_state=7
    )[
        ["discount", "profit", "sales", "category"]
    ]

    losses = (
        df.groupby("product_name", as_index=False)
        .agg(
            profit=("profit", "sum"),
            sales=("sales", "sum")
        )
        .sort_values("profit")
        .head(8)
        .rename(columns={"product_name": "product"})
    )

    return {
        "monthlyTrend": records(
            monthly,
            "month",
            "sales",
            "profit"
        ),
        "regionSales": records(
            region,
            "region",
            "sales",
            "profit"
        ),
        "categoryProfit": records(
            category,
            "category",
            "profit",
            "sales"
        ),
        "topProducts": records(
            products,
            "product",
            "sales",
            "profit"
        ),
        "discountScatter": records(
            scatter,
            "discount",
            "profit",
            "sales",
            "category"
        ),
        "segmentAnalysis": records(
            segment,
            "segment",
            "sales",
            "profit"
        ),
        "stateHeatmap": records(
            state,
            "state",
            "sales",
            "profit"
        ),
        "lossProducts": records(
            losses,
            "product",
            "profit",
            "sales"
        ),
    }

def executive_summary(df: pd.DataFrame) -> dict[str, Any]:

    kpis = build_kpi_payload(df)

    best_region = (
        df.groupby("region")["profit"]
        .sum()
        .sort_values(ascending=False)
    )

    best_category = (
        df.groupby("category")["profit"]
        .sum()
        .sort_values(ascending=False)
    )

    discount_corr = (
        df[["discount", "profit"]]
        .corr(numeric_only=True)
        .iloc[0, 1]
    )

    return {
        "kpis": kpis,

        "bestRegion": (
            best_region.index[0]
            if len(best_region)
            else "N/A"
        ),

        "bestRegionProfit": (
            money(best_region.iloc[0])
            if len(best_region)
            else 0
        ),

        "bestCategory": (
            best_category.index[0]
            if len(best_category)
            else "N/A"
        ),

        "bestCategoryProfit": (
            money(best_category.iloc[0])
            if len(best_category)
            else 0
        ),

        "discountProfitCorrelation": (
            round(float(discount_corr), 3)
            if not np.isnan(discount_corr)
            else 0
        ),

        "lossMakingProducts": build_chart_payload(df)[
            "lossProducts"
        ][:5],
    }