# Business Insights Report

## Executive Summary

The Global Sales Performance dashboard helps retail leadership monitor sales, profit, customer behavior, product performance, discount effectiveness, and regional growth. The analysis is designed to reveal where the business is growing, where profit is leaking, and which actions can improve margin and revenue.

## Core Insights To Finalize After Data Load

Use the generated EDA files in `data/processed/` to replace bracketed values with actual numbers.

## Revenue And Profit

- Total sales reached `[Total Sales]` with total profit of `[Total Profit]`.
- Overall profit margin was `[Profit Margin %]`.
- Average order value was `[Average Order Value]`, indicating the typical revenue generated per order.

Recommendation:

- Track sales and profit together. High-revenue areas with weak margins should be reviewed for discounting, shipping cost, and product mix issues.

## Regional Performance

- Best-performing region by sales: `[Region]`.
- Best-performing region by profit: `[Region]`.
- Lowest-performing state by profit: `[State]`.

Recommendation:

- Replicate high-margin regional strategies in underperforming states.
- Review low-profit states for discount-heavy orders, expensive shipping, or unprofitable product categories.

## Product And Category Trends

- Most profitable category: `[Category]`.
- Highest revenue sub-category: `[Sub-Category]`.
- Largest loss-making product: `[Product Name]`.

Recommendation:

- Promote profitable categories and reduce dependency on low-margin or loss-making products.
- Reprice or discontinue consistently unprofitable products unless they support strategic customer acquisition.

## Customer Behavior

- Highest-value customer segment: `[Segment]`.
- Top customer by lifetime value: `[Customer Name]`.
- Repeat purchase behavior should be monitored using order count and average order value.

Recommendation:

- Build segment-specific campaigns.
- Offer loyalty incentives to high-value customers while avoiding margin-eroding blanket discounts.

## Discount Impact

- Orders with higher discount bands should be compared against margin performance.
- If the `30%+` discount band shows negative margin, discount governance is needed.

Recommendation:

- Set approval rules for discounts above key thresholds.
- Use product-level margin targets before applying promotional discounts.

## Seasonal Sales Patterns

- Review `monthly_sales_trends.csv` to identify peak and low-demand months.
- Use the 3-month forecast output to prepare inventory, staffing, and campaign plans.

Recommendation:

- Increase stock and campaign spend before recurring peak months.
- Use low-demand months for targeted retention and clearance campaigns.

## Strategic Recommendations

- Prioritize profit margin, not only sales volume.
- Reduce excessive discounting on products with repeated losses.
- Invest in high-performing categories and customer segments.
- Build regional action plans for states with negative profit.
- Monitor forecast variance monthly to improve planning accuracy.

