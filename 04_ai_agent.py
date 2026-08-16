import os
import time
import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

df = pd.read_csv("telco_churn_clean.csv")

FORBIDDEN_KEYWORDS = ['import', 'open(', 'exec(', 'eval(', 'os.', 'sys.',
                       '__', 'subprocess', 'delete', 'remove', 'write']

def is_code_safe(code):
    code_lower = code.lower()
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in code_lower:
            return False
    return True

def _ask_agent_internal(question):
    schema_info = f"""
You have access to a pandas DataFrame called df — Telco customer churn data.
Columns: {list(df.columns)}
Sample row: {df.iloc[0].to_dict()}

The user will ask a question about customer churn.
Write ONLY a single line of executable pandas code that answers the question,
assigning the result to a variable called `result`. No explanations, no markdown,
just the raw code line. Use df.
"""

    code_response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=schema_info + f"\n\nQuestion: {question}\n\nCode:"
    )
    code = code_response.text.strip().strip("`").replace("python\n", "")
    print(f"\n[Generated code]: {code}")

    local_vars = {"df": df, "pd": pd}

    if not is_code_safe(code):
        result = "Blocked: generated code contained a potentially unsafe operation."
    else:
        try:
            exec(code, {"__builtins__": {}}, local_vars)
            result = local_vars.get("result", "No result variable found")
        except Exception as e:
            result = f"Error running code: {e}"

    print(f"[Raw result]: {result}")

    explain_response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Question: {question}\nResult: {result}\n\nExplain this result in one or two plain-English sentences, as if reporting to a business stakeholder."
    )

    print(f"\n[Answer]: {explain_response.text}")

def ask_agent(question, retries=3):
    for attempt in range(retries):
        try:
            return _ask_agent_internal(question)
        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e) and attempt < retries - 1:
                print(f"Rate limited, waiting 60s before retry...")
                time.sleep(60)
            else:
                raise

# Test it
ask_agent("Which contract type has the highest churn rate?")
ask_agent("What is the average tenure of customers who churned versus those who stayed?")
ask_agent("Which payment method has the highest churn rate?")
ask_agent("Are senior citizens more likely to churn than non-senior citizens?")