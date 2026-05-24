# Tableau Dashboard Build Guide

## Data Import

1. Open Tableau Desktop or Tableau Public.
2. Connect to `data/processed/superstore_clean.csv`.
3. Connect to `data/processed/sales_forecast_3_months.csv` if using generated forecast output.
4. Validate data types for dates, dimensions, and measures.

## Worksheets

Create worksheets for:

- KPI summary
- Monthly sales trend
- Regional sales
- Category revenue share
- State/region map
- Top 10 products
- Loss-making products
- Profit vs discount
- Customer segment sales and profit
- 3-month forecast

## Dashboard Actions

- Add filters for order date, region, segment, category, and sub-category.
- Enable worksheet actions for product and region drill-down.
- Use highlight actions for customer segment and discount analysis.

## Publishing

Export screenshots to `dashboard/screenshots/` and include them in the README.

