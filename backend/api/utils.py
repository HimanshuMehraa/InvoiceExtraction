import openai
from django.conf import settings
import fitz  # PyMuPDF
import os
import datetime
import json

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

client = openai.OpenAI()

def extract_invoice_data(text):
    prompt = f"""
Extract the following fields from this invoice text:

- Invoice Date
- Invoice Number
- Amount
- Due Date

Respond in JSON format with keys: invoice_date, invoice_number, amount, due_date.

Omit $ sign from the amount . Just a value 
Invoice Text:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        result = response.choices[0].message.content
        data = json.loads(result)
        return data

    except Exception as e:
        print("Error:", e)
        return {}
