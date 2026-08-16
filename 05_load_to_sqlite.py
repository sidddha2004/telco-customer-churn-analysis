import pandas as pd
import sqlite3

df = pd.read_csv("telco_churn_clean.csv")

# Create a SQLite database file and load the dataframe into it as a table
conn = sqlite3.connect("telco_churn.db")
df.to_sql("customers", conn, if_exists="replace", index=False)

# Quick test query to confirm it worked
test = pd.read_sql("SELECT COUNT(*) as total_rows FROM customers", conn)
print(test)

conn.close()
print("Data loaded into telco_churn.db successfully")