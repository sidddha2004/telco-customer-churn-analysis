import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 120

df = pd.read_csv("telco_churn_clean.csv")

# ===== CHART 1: Churn Rate by Contract Type =====
contract_churn = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(contract_churn.index, contract_churn.values, color=['#d62728', '#ff7f0e', '#2ca02c'])
for bar, val in zip(bars, contract_churn.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f"{val:.1f}%", ha='center', fontweight='bold')
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Contract Type", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig("chart1_churn_by_contract.png")
plt.show()
print("Saved chart1_churn_by_contract.png")

# ===== CHART 2: Tenure Distribution - Churned vs Retained =====
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x='tenure', hue='Churn', bins=30, kde=True, palette={'Yes': '#d62728', 'No': '#2ca02c'}, ax=ax)
ax.set_xlabel("Tenure (months)")
ax.set_title("Customer Tenure Distribution: Churned vs Retained", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig("chart2_tenure_distribution.png")
plt.show()
print("Saved chart2_tenure_distribution.png")

# ===== CHART 3: Churn Rate by Internet Service =====
internet_churn = df.groupby('InternetService')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(internet_churn.index, internet_churn.values, color=['#d62728', '#ff7f0e', '#2ca02c'])
for bar, val in zip(bars, internet_churn.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f"{val:.1f}%", ha='center', fontweight='bold')
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Internet Service Type", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig("chart3_churn_by_internet.png")
plt.show()
print("Saved chart3_churn_by_internet.png")

# ===== CHART 4: High-Risk Segment Breakdown =====
df['high_risk'] = (
    (df['Contract'] == 'Month-to-month') &
    (df['PaymentMethod'] == 'Electronic check') &
    (df['InternetService'] == 'Fiber optic')
)

risk_churn = df.groupby('high_risk')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
labels = ['Other Customers', 'High-Risk Segment\n(Month-to-month + E-check + Fiber)']
values = [risk_churn[False], risk_churn[True]]

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(labels, values, color=['#2ca02c', '#d62728'])
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f"{val:.1f}%", ha='center', fontweight='bold', fontsize=12)
ax.set_ylabel("Churn Rate (%)")
ax.set_title("High-Risk Segment vs Other Customers", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig("chart4_high_risk_segment.png")
plt.show()
print("Saved chart4_high_risk_segment.png")