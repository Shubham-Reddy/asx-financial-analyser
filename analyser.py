import os
import json
from groq import Groq
import streamlit as st

def get_client():
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment or Streamlit secrets")
    return Groq(api_key=api_key)

def analyse_report(text):
    client = get_client()
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": """You are a senior financial analyst specialising in ASX listed companies.
                Analyse this annual report and return ONLY a valid JSON object with no extra text, no markdown, no backticks.
                Use exactly these keys:
                {
                    "company_name": "full company name",
                    "asx_code": "3 letter ASX code if found",
                    "financial_year": "e.g. FY2024",
                    "executive_summary": "two paragraph summary of overall performance",
                    "sentiment": "positive or neutral or negative",
                    "revenue": "exact revenue figure with currency e.g. USD 55.7 billion",
                    "profit": "exact net profit figure with currency",
                    "revenue_growth": "percentage change in revenue e.g. +5.2% or -3.1%",
                    "profit_growth": "percentage change in profit",
                    "ebitda": "EBITDA figure if mentioned",
                    "dividend": "dividend per share if mentioned",
                    "employees": "number of employees if mentioned",
                    "risks": ["risk 1", "risk 2", "risk 3", "risk 4", "risk 5"],
                    "opportunities": ["opportunity 1", "opportunity 2", "opportunity 3"],
                    "key_highlights": ["highlight 1", "highlight 2", "highlight 3"],
                    "outlook": "one paragraph on future outlook"
                }
                Return only the JSON object. Nothing else."""
            },
            {
                "role": "user",
                "content": f"Analyse this ASX annual report:\n\n{text[:6000]}"
            }
        ]
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    return json.loads(raw)
