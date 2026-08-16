import pandas as pd

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

# 1. Fix TotalCharges: blank -> 0, then convert to numeric
df['TotalCharges'] = df['TotalCharges'].replace(' ', '0')
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])

# 2. Convert SeniorCitizen from 0/1 to Yes/No for consistency
df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})

# 3. Drop customerID - no analytical value
df = df.drop(columns=['customerID'])

print("Cleaned shape:", df.shape)
print(df.dtypes)
print("\nSample:")
print(df.head())

df.to_csv("telco_churn_clean.csv", index=False)
print("\nSaved to telco_churn_clean.csv")