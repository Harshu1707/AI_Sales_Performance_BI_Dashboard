# Power BI Dashboard Build Guide

## Data Import

1. Open Power BI Desktop.
2. Import `data/processed/superstore_clean.csv`.
3. Import `data/processed/sales_forecast_3_months.csv`.
4. Confirm date fields and numeric types.
5. Add DAX measures from `dax/powerbi_measures.dax`.

## Recommended Model

- Main fact table: `superstore_clean`.
- Optional forecast table: `sales_forecast_3_months`.
- Create a date table if you want production-grade time intelligence.

## Visual Layout

Use four pages:

- Executive Overview
- Regional Performance
- Product Analysis
- Customer & Discount Insights

## Required Visuals

- KPI cards
- Monthly sales trend line chart
- Regional sales bar chart
- Category-wise pie or donut chart
- Map visualization by state/region
- Top 10 products chart
- Profit vs discount scatter plot
- Sales forecasting chart
- Customer segment analysis
- Interactive slicers and filters

## Advanced Features

- Drill-down hierarchy: Region > State > City.
- Drill-down hierarchy: Category > Sub-Category > Product Name.
- Dynamic page navigation buttons.
- Tooltip pages for product and customer details.
- Responsive canvas layout using consistent spacing and grouped slicers.

