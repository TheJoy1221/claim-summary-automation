# Claim Summary Automation with GPT-4 Summarization (Sanitized for Public Release)

import os
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import openai

# Load OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# File paths (replace with your actual data locations)
raw_data_path = r"./data/FHE_RAW.xlsx"
output_path = r"./output/Claim_Summary.xlsx"

# Load all sheets from Excel file
sheets = pd.read_excel(raw_data_path, sheet_name=None)
sheet1 = sheets[list(sheets.keys())[0]]
sheet2 = sheets[list(sheets.keys())[1]]
adt_sheet = sheets[list(sheets.keys())[2]]

# --- Extract from Sheet 1 ---
row1 = sheet1.iloc[0]
claim_summary_data = {
    'Claimant': [f"{row1['first_name']} {row1['last_name']}"],
    'LOC': [row1['company_name']],
    'Hire Date': [pd.to_datetime(row1['hire_date']).date()],
    'DOI': [pd.to_datetime(row1['loss_date']).date()],
    'Claim Type': [row1['item_name']],
}

# --- Extract and clean claim notes ---
raw_notes_html = adt_sheet['Column9'].astype(str)
clean_notes = [
    BeautifulSoup(html if '<' in html else f"<p>{html}</p>", "html.parser").get_text(" ", strip=True)
    for html in raw_notes_html
]
notes_combined = " ".join(clean_notes[:600])  # limit to ~600 entries for token control

# --- GPT-4 Summarization ---
def chunk_text(text, max_chars=4000):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

def summarize_notes(text_block):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes medical and injury claim notes."},
            {"role": "user", "content": f"Summarize the following notes into key facts: {text_block}"}
        ],
        max_tokens=300,
        temperature=0.3
    )
    return response['choices'][0]['message']['content'].strip()

def summarize_notes_in_chunks(full_text):
    summaries = []
    for chunk in chunk_text(full_text):
        try:
            summary = summarize_notes(chunk)
            summaries.append(summary)
        except Exception as e:
            summaries.append("[Summary failed: token limit exceeded or other issue]")
            break
    return " ".join(summaries)

claim_summary_data['Claim History'] = [summarize_notes_in_chunks(notes_combined)]

# --- Financial calculations ---
paid_amount = sheet2[sheet2['reserve_or_paid_code'] == 'P']['loss_amt'].sum()
incurred_amount = sheet2[sheet2['reserve_or_paid_code'] == 'R']['loss_amt'].sum()
reserve_amount = incurred_amount - paid_amount

claim_summary_data['Current Plan'] = ["Your Company Name to monitor legal activity and update file as appropriate."]
claim_summary_data['Paid'] = [paid_amount]
claim_summary_data['Remaining Reserve'] = [reserve_amount]
claim_summary_data['Total Incurred'] = [incurred_amount]

# --- Export final Claim Summary ---
summary_df = pd.DataFrame(claim_summary_data)
os.makedirs(os.path.dirname(output_path), exist_ok=True)
summary_df.to_excel(output_path, index=False)
print(f"✨ Claim Summary generated: {output_path}")