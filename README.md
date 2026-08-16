# Telco Customer Churn Analysis

End-to-end churn analysis using the IBM Telco Customer Churn dataset, covering data cleaning, SQL segmentation analysis, an AI agent for natural-language querying, and an interactive Power BI dashboard.

## Business Question
Which customers are most likely to churn, and what specific combination of factors puts them at highest risk?

## Key Findings
- **Overall churn rate: 26.54%** (1,869 of 7,043 customers)
- **Contract type is the single biggest churn driver**: Month-to-month customers churn at 42.71% — over 15x higher than two-year contract customers (2.83%)
- **Compound high-risk segment identified**: customers with Month-to-month contract + Electronic check payment + Fiber optic internet churn at **60.37%** — more than double the company average
- **Electronic check payment method** shows a striking 45.29% churn rate vs. 15-19% for all other payment methods
- **Tenure strongly predicts loyalty**: new customers (0-12 months) churn at 47.68%, vs. just 9.51% for long-tenured customers (49-72 months)
- Churned customers pay **more per month on average** ($74.44 vs $61.27) but leave with far lower lifetime value

## Tech Stack
- **Python:** pandas, matplotlib, seaborn
- **SQL:** SQLite (CTEs, CASE WHEN, aggregation)
- **AI:** Google Gemini API (gemini-3.6-flash) — custom agent that writes and executes its own pandas code to answer natural-language churn questions
- **Dashboard:** Power BI (DAX measures, calculated columns)

## Project Structure
01_load_data.py - Loads and inspects the raw dataset
02_clean_data.py - Fixes TotalCharges data type, handles blanks, drops customerID
03_eda.py - Churn rate breakdown by contract, payment, tenure, internet service
04_ai_agent.py - AI agent: answers natural-language churn questions
05_load_to_sqlite.py - Loads cleaned data into a local SQLite database
06_sql_queries.py - 5 SQL queries including the compound high-risk segment analysis
07_visualizations.py - Generates all 4 charts
telco_churn_clean.csv - Cleaned dataset
Telco_Churn_Dashboard.pbix - Interactive Power BI dashboard

## Churn by Segment

| Segment | Churn Rate |
|---|---|
| Month-to-month contract | 42.71% |
| One year contract | 11.27% |
| Two year contract | 2.83% |
| Fiber optic internet | 41.89% |
| DSL internet | 18.96% |
| Electronic check payment | 45.29% |
| **High-risk compound segment** | **60.37%** |

## Revenue Impact
Month-to-month churned customers alone account for **$120,847 in monthly recurring revenue at risk** and **$1.93M in lost total customer value** — far exceeding one-year ($674,991) and two-year ($260,753) contract losses combined.

## AI Agent Example
Q: Which contract type has the highest churn rate?
[Generated code]: result = (df['Churn'] == 'Yes').groupby(df['Contract']).mean().idxmax()
[Raw result]: Month-to-month
[Answer]: Customers on month-to-month contracts have the highest churn rate because they lack a long-term commitment...

Safety measures: keyword blocklist, restricted execution environment, automatic rate-limit retry handling — same architecture as my GA4 funnel analysis AI agent.

## Data Quality Notes
- 11 customers had blank `TotalCharges` values (brand-new signups with 0 tenure, not yet billed) — converted to 0 and excluded from tenure-based churn rate calculations, since they haven't had a chance to churn yet

## Setup
1. Download dataset: [IBM Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
2. `pip install pandas matplotlib seaborn google-genai python-dotenv`
3. Add your Gemini API key to a `.env` file: `GEMINI_API_KEY=your_key`
4. Run scripts in order: `01_load_data.py` → `02_clean_data.py` → `03_eda.py` → `05_load_to_sqlite.py` → `06_sql_queries.py` → `07_visualizations.py`
