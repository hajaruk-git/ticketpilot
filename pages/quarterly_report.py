import streamlit as st
import pandas as pd
from datetime import datetime
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Quarterly Analysis", page_icon="📊")
st.title("📊 Quarterly Analysis of IT Tickets")

QUARTERS = {
    "Q1 2025": ("2025-01-01", "2025-03-31"),
    "Q2 2025": ("2025-04-01", "2025-06-30"),
}

quarter = st.selectbox("Choose a quarter", list(QUARTERS.keys()))

if st.button("Analyze tickets"):
    start_str, end_str = QUARTERS[quarter]
    start_date = datetime.strptime(start_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_str, "%Y-%m-%d")

    try:
        df = pd.read_csv("tickets.csv")
        df["CreatedAt"] = pd.to_datetime(df["CreatedAt"], format="mixed", errors="coerce")
        mask = (df["CreatedAt"] >= start_date) & (df["CreatedAt"] <= end_date) & (df["Category"] == "IT")
        filtered_df = df[mask]
        messages = filtered_df["Message"].dropna().tolist()

        if not messages:
            st.warning("No IT tickets found for the selected period.")
        else:
            formatted_messages = "\n- " + "\n- ".join(messages)
            prompt = f"""
You are an IT support assistant. You are given a series of IT tickets submitted between {start_date.date()} and {end_date.date()}.

Here are the messages:
{formatted_messages}

Analyze these tickets and:
1. Identify the 3 to 5 most recurring issues.
2. Group them by theme (VPN, passwords, network, etc.)
3. Estimate their approximate frequency (percentage or count).
4. Write a clear, structured report in markdown format, intended for a non-technical IT manager.
"""

            with st.spinner("GPT is analyzing the tickets..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=800
                )

            report = response["choices"][0]["message"]["content"]

            st.subheader("📝 Analysis Report")
            st.markdown(report)

            st.download_button("📥 Download the report (.md)", report, file_name=f"IT_report_{quarter}.md")

    except Exception as e:
        st.error(f"Error during analysis: {e}")
