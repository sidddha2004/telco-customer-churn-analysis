import pandas as pd

# Load the raw dataset
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("Shape:", df.shape)
print("\nColumn names and types:")
print(df.info())
print("\nFirst 5 rows:")
print(df.head())
print("\nChurn value counts:")
print(df['Churn'].value_counts())
print("\nMissing values per column:")
print(df.isnull().sum())

# Check for hidden blanks in TotalCharges
print("\nRows where TotalCharges is blank/space:")
print(df[df['TotalCharges'].str.strip() == ''])