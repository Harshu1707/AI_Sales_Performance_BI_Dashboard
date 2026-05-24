-- Global Sales Performance & Business Insights Dashboard
-- Assumed table: superstore_orders
-- Assumed grain: one row per order line item

-- 1. Top 5 best-selling products by revenue and quantity
SELECT
    product_name,
    SUM(sales) AS total_sales,
    SUM(quantity) AS total_quantity,
    SUM(profit) AS total_profit
FROM superstore_orders
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 5;

-- 2. Monthly revenue analysis
SELECT
    DATE_TRUNC('month', order_date) AS sales_month,
    SUM(sales) AS monthly_sales,
    SUM(profit) AS monthly_profit,
    COUNT(DISTINCT order_id) AS total_orders
FROM superstore_orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY sales_month;

-- 3. Region-wise profit analysis
SELECT
    region,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    CASE WHEN SUM(sales) = 0 THEN 0 ELSE SUM(profit) / SUM(sales) * 100 END AS profit_margin_pct,
    COUNT(DISTINCT order_id) AS total_orders
FROM superstore_orders
GROUP BY region
ORDER BY total_profit DESC;

-- 4. Highest profit categories
SELECT
    category,
    sub_category,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    CASE WHEN SUM(sales) = 0 THEN 0 ELSE SUM(profit) / SUM(sales) * 100 END AS profit_margin_pct
FROM superstore_orders
GROUP BY category, sub_category
ORDER BY total_profit DESC;

-- 5. Customer lifetime value
SELECT
    customer_id,
    customer_name,
    segment,
    SUM(sales) AS lifetime_sales,
    SUM(profit) AS lifetime_profit,
    COUNT(DISTINCT order_id) AS order_count,
    CASE WHEN COUNT(DISTINCT order_id) = 0 THEN 0 ELSE SUM(sales) / COUNT(DISTINCT order_id) END AS average_order_value
FROM superstore_orders
GROUP BY customer_id, customer_name, segment
ORDER BY lifetime_sales DESC;

-- 6. Most discounted products
SELECT
    product_name,
    category,
    sub_category,
    AVG(discount) AS average_discount,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    COUNT(*) AS line_count
FROM superstore_orders
GROUP BY product_name, category, sub_category
HAVING AVG(discount) > 0
ORDER BY average_discount DESC, total_profit ASC
LIMIT 20;

-- 7. Sales growth trends
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) AS sales_month,
        SUM(sales) AS monthly_sales
    FROM superstore_orders
    GROUP BY DATE_TRUNC('month', order_date)
),
growth AS (
    SELECT
        sales_month,
        monthly_sales,
        LAG(monthly_sales) OVER (ORDER BY sales_month) AS previous_month_sales
    FROM monthly_sales
)
SELECT
    sales_month,
    monthly_sales,
    previous_month_sales,
    CASE
        WHEN previous_month_sales IS NULL OR previous_month_sales = 0 THEN NULL
        ELSE (monthly_sales - previous_month_sales) / previous_month_sales * 100
    END AS sales_growth_pct
FROM growth
ORDER BY sales_month;

-- 8. Loss-making products
SELECT
    product_name,
    category,
    sub_category,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    AVG(discount) AS average_discount,
    SUM(quantity) AS total_quantity
FROM superstore_orders
GROUP BY product_name, category, sub_category
HAVING SUM(profit) < 0
ORDER BY total_profit ASC;

-- 9. Discount impact on profitability
SELECT
    CASE
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount <= 0.10 THEN '0-10%'
        WHEN discount <= 0.20 THEN '10-20%'
        WHEN discount <= 0.30 THEN '20-30%'
        ELSE '30%+'
    END AS discount_band,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    CASE WHEN SUM(sales) = 0 THEN 0 ELSE SUM(profit) / SUM(sales) * 100 END AS profit_margin_pct,
    COUNT(DISTINCT order_id) AS total_orders
FROM superstore_orders
GROUP BY
    CASE
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount <= 0.10 THEN '0-10%'
        WHEN discount <= 0.20 THEN '10-20%'
        WHEN discount <= 0.30 THEN '20-30%'
        ELSE '30%+'
    END
ORDER BY profit_margin_pct DESC;

