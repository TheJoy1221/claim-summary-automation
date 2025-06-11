# Claim Summary Automation

A real-world automation tool that extracts key information from insurance claim data, parses structured HTML, and summarizes unstructured notes using GPT. Outputs a clean, standardized format for rapid decision-making and downstream automation.

---

🚀 Features
	- Parses structured and unstructured data from Excel and HTML
	- Uses OpenAI GPT API to summarize lengthy case notes
	- Extracts fields like Claimant Name, Date of Injury, Diagnosis, Treatment, and Doctor Visits
	-  Outputs to a standardized Excel sheet for downstream processing
	- Clean fallback logic in place if summarization fails
	- Designed to reduce manual work and improve processing speed for case coordinators

🚀 Tech Stack
	•	Python 3.x
	•	pandas, openpyxl
	•	bs4 (BeautifulSoup) for HTML parsing
	•	openai for GPT integration
	•	datetime, os, re

🧰 How It Works
	1.	📥 Load input data from Excel workbook (with multiple sheets)
	2.	🧾 Parse structured fields (e.g., Claimant Info, Loss Details)
	3.	🧹 Extract raw HTML notes and clean them with BeautifulSoup
	4.	🧠 Use GPT API to summarize note content (configurable per sheet)
	5.	📤 Write results into a clean, readable Excel sheet

## 📁 Example Output

| Claimant        | Date of Injury | Summary of Notes                           |
|-----------------|----------------|--------------------------------------------|
| John Doe        | 2024-06-18     | Patient received PT twice a week. No pain. |
| Amanda Sterling | 2024-07-22     | MRI completed. Pending surgical referral.  |

> *(Sample data only; no real PHI or confidential records are used.)*

🔒 Security

This public version contains no PHI. All identifiers, data, and outputs have been anonymized or removed.

⚙️ Setup

pip install pandas openpyxl beautifulsoup4 openai

Make sure your OpenAI key is stored as an environment variable:

export OPENAI_API_KEY='your-key-here'

📄 Assumptions
	•	📂 The Excel file currently includes three sheets, each with specific formatting:
	•	Sheet 1: Claimant Information
	•	Sheet 2: HTML Notes
	•	Sheet 3: Additional Data
	•	🧾 Column headers must remain consistent for successful parsing
	•	🧠 GPT usage assumes reasonable API limits and cost-awareness
	•	🔁 Current logic is based on known sheet structure and order

🔧 TODO (Roadmap)
	•	🔍 Add dynamic sheet recognition and flexible column mapping
	•	🛠 Build CLI tool to process multiple files in batch
	•	🤖 Integrate form submission via RPA (Selenium or AutoGUI)
	•	🧠 Extend GPT prompt tuning for better summarization of medical terms
	•	🖥 Add GUI or Streamlit interface for non-technical users

💬 Questions?
	•	💌 Want to collaborate or provide feedback? Open an issue or reach out!
	•	🤝 Contributions are welcome as this project continues to evolve.
