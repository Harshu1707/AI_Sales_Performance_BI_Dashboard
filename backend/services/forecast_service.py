from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LinearRegression


def build_forecast(df: pd.DataFrame) -> dict:

    # Convert to datetime
    df["order_date"] = pd.to_datetime(df["order_date"])

    # Monthly sales aggregation
    monthly = (
        df.set_index("order_date")
        .resample("ME")["sales"]
        .sum()
        .reset_index()
        .rename(columns={"order_date": "date", "sales": "sales"})
    )

    # Create period index
    monthly["period"] = range(len(monthly))

    # Train model
    model = LinearRegression()
    model.fit(monthly[["period"]], monthly["sales"])

    # Predict next 3 months
    future_periods = pd.DataFrame({
        "period": range(len(monthly), len(monthly) + 3)
    })

    last_date = monthly["date"].max()

    future_dates = pd.date_range(
        last_date + pd.offsets.MonthEnd(1),
        periods=3,
        freq="ME"
    )

    predictions = model.predict(future_periods)

    # Forecast output
    forecast = [
        {
            "month": date.strftime("%b %Y"),
            "predictedSales": round(float(max(value, 0)), 2)
        }
        for date, value in zip(future_dates, predictions)
    ]

    # Historical data
    history = [
        {
            "month": row.date.strftime("%b %Y"),
            "sales": round(float(row.sales), 2)
        }
        for row in monthly.tail(18).itertuples(index=False)
    ]

    # Growth calculation
    growth = 0

    if len(history) and history[-1]["sales"]:
        growth = (
            (
                forecast[-1]["predictedSales"]
                - history[-1]["sales"]
            )
            / history[-1]["sales"]
        ) * 100

    return {
        "history": history,
        "forecast": forecast,
        "predictedGrowth": round(float(growth), 2)
    }