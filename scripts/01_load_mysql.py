import sqlite3
import pandas as pd

print("1. Booting up local database engine...")
# This automatically creates a local database file without needing a server or password
conn = sqlite3.connect('olist_ecommerce_automated.db')

files = [
    'olist_orders_dataset.csv',
    'olist_customers_dataset.csv',
    'olist_order_items_dataset.csv',
    'olist_order_payments_dataset.csv',
    'olist_order_reviews_dataset.csv'
]

print("2. Ingesting raw Kaggle CSVs...")
for file in files:
    table_name = file.replace('.csv', '')
    print(f"   -> Loading {table_name}...")
    # Read the CSV and push it directly into the database engine
    df = pd.read_csv(file)
    df.to_sql(table_name, conn, if_exists='replace', index=False)

print("3. Executing SQL Transformation Engine...")
# Clear out any old runs
conn.execute("DROP TABLE IF EXISTS olist_financial_analytics_export;")

# The exact same robust SQL logic we built earlier
transform_query = """
CREATE TABLE olist_financial_analytics_export AS
WITH PaymentSummary AS (
    SELECT 
        order_id,
        SUM(payment_value) AS total_payment_value,
        MAX(payment_type) AS primary_payment_type,
        MAX(payment_installments) AS max_installments,
        COUNT(payment_sequential) AS number_of_payment_methods
    FROM olist_order_payments_dataset
    GROUP BY order_id
),
BasketSummary AS (
    SELECT 
        order_id,
        COUNT(product_id) AS total_items_in_basket,
        SUM(price) AS total_products_revenue,
        SUM(freight_value) AS total_freight_revenue
    FROM olist_order_items_dataset
    GROUP BY order_id
)
SELECT 
    o.order_id,
    o.order_purchase_timestamp,
    strftime('%Y-%m', o.order_purchase_timestamp) AS order_month,
    c.customer_unique_id,
    c.customer_state,
    c.customer_city,
    b.total_items_in_basket,
    b.total_products_revenue,
    b.total_freight_revenue,
    p.total_payment_value,
    p.primary_payment_type,
    p.max_installments,
    CASE 
        WHEN p.max_installments <= 1 THEN 'Paid in Full'
        WHEN p.max_installments BETWEEN 2 AND 5 THEN 'Short-Term Financing (2-5x)'
        WHEN p.max_installments > 5 THEN 'Long-Term Financing (6x+)'
        ELSE 'Unknown'
    END AS installment_behavior_tier,
    CASE 
        WHEN p.total_payment_value > 250 THEN 'High Value (> $250)'
        WHEN p.total_payment_value BETWEEN 75 AND 250 THEN 'Mid Value ($75 - $250)'
        WHEN p.total_payment_value > 0 THEN 'Low Value (< $75)'
        ELSE 'Unknown'
    END AS revenue_tier,
    CASE
        WHEN p.number_of_payment_methods > 1 THEN 'Split Payment'
        ELSE 'Single Payment'
    END AS payment_complexity,
    r.review_score
FROM olist_orders_dataset o
LEFT JOIN olist_customers_dataset c ON TRIM(o.customer_id) = TRIM(c.customer_id)
LEFT JOIN BasketSummary b ON TRIM(o.order_id) = TRIM(b.order_id)
LEFT JOIN PaymentSummary p ON TRIM(o.order_id) = TRIM(p.order_id)
LEFT JOIN olist_order_reviews_dataset r ON TRIM(o.order_id) = TRIM(r.order_id)
WHERE o.order_status LIKE '%delivered%';
"""
# Run the massive query
conn.execute(transform_query)

print("4. Extracting final Master Dataset...")
# Pull the newly created table out of the database and save it as a CSV
final_df = pd.read_sql("SELECT * FROM olist_financial_analytics_export", conn)
final_df.to_csv('olist_powerbi_master.csv', index=False)

print("\n✅ PIPELINE COMPLETE! File 'olist_powerbi_master.csv' is ready for Power BI.")
