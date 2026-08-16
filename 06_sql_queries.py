import pandas as pd
import sqlite3

conn = sqlite3.connect("telco_churn.db")

# Query 1: Overall churn rate
q1 = """
SELECT
    Churn,
    COUNT(*) as customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2) as percentage
FROM customers
GROUP BY Churn
"""
print("=== Query 1: Overall Churn Rate ===")
print(pd.read_sql(q1, conn))

# Query 2: Churn rate by contract type
q2 = """
SELECT
    Contract,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC
"""
print("\n=== Query 2: Churn Rate by Contract ===")
print(pd.read_sql(q2, conn))

# Query 3: High-risk segment - month-to-month + electronic check + fiber optic
q3 = """
SELECT
    COUNT(*) as high_risk_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct
FROM customers
WHERE Contract = 'Month-to-month'
    AND PaymentMethod = 'Electronic check'
    AND InternetService = 'Fiber optic'
"""
print("\n=== Query 3: High-Risk Segment (Month-to-month + E-check + Fiber) ===")
print(pd.read_sql(q3, conn))

# Query 4: Rank contract types by revenue at risk (churned customers' total charges)
q4 = """
SELECT
    Contract,
    COUNT(*) as churned_customers,
    ROUND(SUM(MonthlyCharges), 2) as monthly_revenue_at_risk,
    ROUND(SUM(TotalCharges), 2) as total_revenue_lost
FROM customers
WHERE Churn = 'Yes'
GROUP BY Contract
ORDER BY monthly_revenue_at_risk DESC
"""
print("\n=== Query 4: Revenue Impact by Contract Type (Churned Only) ===")
print(pd.read_sql(q4, conn))

q5 = """
SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12mo'
        WHEN tenure <= 24 THEN '13-24mo'
        WHEN tenure <= 48 THEN '25-48mo'
        ELSE '49-72mo'
    END as tenure_group,
    COUNT(*) as total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate_pct
FROM customers
WHERE tenure > 0
GROUP BY tenure_group
ORDER BY churn_rate_pct DESC
"""
print("\n=== Query 5: Churn Rate by Tenure Group ===")
print(pd.read_sql(q5, conn))

# Debug: check these edge-case rows
debug = """
SELECT tenure, TotalCharges, Churn, COUNT(*) as count
FROM customers
WHERE tenure = 0
GROUP BY tenure, TotalCharges, Churn
"""
print("\n=== Debug: tenure = 0 rows ===")
print(pd.read_sql(debug, conn))

conn.close()