import pandas as pd

df = pd.read_csv("telco_churn_clean.csv")

# 1. Overall churn rate
print("=== Overall Churn Rate ===")
print(df['Churn'].value_counts(normalize=True) * 100)

# 2. Churn by Contract type
print("\n=== Churn Rate by Contract Type ===")
print(df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).round(2))

# 3. Churn by Payment Method
print("\n=== Churn Rate by Payment Method ===")
print(df.groupby('PaymentMethod')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).round(2))

# 4. Churn by Internet Service
print("\n=== Churn Rate by Internet Service ===")
print(df.groupby('InternetService')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).round(2))

# 5. Churn by tenure groups
df['tenure_group'] = pd.cut(df['tenure'], bins=[0, 12, 24, 48, 72],
                              labels=['0-12mo', '13-24mo', '25-48mo', '49-72mo'])
print("\n=== Churn Rate by Tenure Group ===")
print(df.groupby('tenure_group', observed=True)['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).round(2))

# 6. Average tenure/charges for churned vs retained
print("\n=== Avg Tenure & Charges: Churned vs Retained ===")
print(df.groupby('Churn')[['tenure', 'MonthlyCharges', 'TotalCharges']].mean().round(2))

# Save tenure_group column for later use
df.to_csv("telco_churn_clean.csv", index=False)