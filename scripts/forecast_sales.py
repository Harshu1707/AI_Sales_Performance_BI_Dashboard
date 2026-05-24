"""Forecast next 3 months of Superstore sales."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
except ImportError:  # pragma: no cover - depends on local environment
    ExponentialSmoothing = None


def forecast_sales(df: pd.DataFrame, periods: int = 3) -> pd.DataFrame:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    monthly = (
        df.dropna(subset=["order_date"])
        .set_index("order_date")
        .resample("MS")["sales"]
        .sum()
        .asfreq("MS")
        .fillna(0)
    )

    if len(monthly) < 6:
        raise ValueError("At least 6 months of sales history is recommended for forecasting.")

    if ExponentialSmoothing is None:
        recent = monthly.tail(6)
        trend = recent.diff().dropna().mean() if len(recent) > 1 else 0
        last_value = recent.iloc[-1]
        index = pd.date_range(monthly.index.max() + pd.offsets.MonthBegin(1), periods=periods, freq="MS")
        values = [max(last_value + trend * step, 0) for step in range(1, periods + 1)]
        return pd.DataFrame(
            {
                "forecast_month": index.strftime("%Y-%m"),
                "forecast_sales": pd.Series(values).round(2).values,
                "model": "Rolling 6-Month Trend Fallback",
            }
        )

    if len(monthly) >= 24:
        model = ExponentialSmoothing(monthly, trend="add", seasonal="add", seasonal_periods=12)
    else:
        model = ExponentialSmoothing(monthly, trend="add", seasonal=None)

    fitted = model.fit(optimized=True)
    forecast = fitted.forecast(periods)

    return pd.DataFrame(
        {
            "forecast_month": forecast.index.strftime("%Y-%m"),
            "forecast_sales": forecast.round(2).values,
            "model": "Holt-Winters Exponential Smoothing",
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a 3-month Superstore sales forecast.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV file.")
    parser.add_argument("--output", required=True, help="Path for forecast CSV output.")
    parser.add_argument("--periods", type=int, default=3, help="Number of months to forecast.")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    forecast_sales(df, args.periods).to_csv(output_path, index=False)
    print(f"Forecast written to {output_path}")


if __name__ == "__main__":
    main()
