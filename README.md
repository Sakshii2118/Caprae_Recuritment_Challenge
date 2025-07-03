# Caprae LeadGen Scraping Tool

**Tool Name:** `caprae_leadgen_scraping`  
**Author:** Sakshi Gupta  
**Track:** Quality-First — Caprae Capital Lead Generation Challenge

---

## 🧠 Project Overview

This project focuses on enhancing Caprae's lead generation workflow by improving the **data validation, enrichment, and scoring** process.

Rather than scraping more data, the tool ensures that existing lead data is:
- Cleaned
- Verified
- Scored based on quality
- Prioritized for sales outreach

The app is fully built with **Python and Streamlit**, making it fast, browser-based, and easy to use — no coding required.

---

## 🚀 Features

- ✅ **Email Validation**  
  Uses regex to verify if email formats are valid  
- ✅ **Free Email Filtering**  
  Flags leads using generic domains like `gmail.com`, `yahoo.com`, etc.
- ✅ **Deduplication Options**  
  User can choose how to remove duplicates (by Company, Email, Phone, etc.)
- ✅ **Lead Scoring**  
  Based on email validity, domain type, revenue, employee count, and completeness
- ✅ **Lead Prioritization**  
  Classifies each lead into High (🟢), Medium (🟡), or Low (🔴) priority
- ✅ **LinkedIn Enrichment**  
  For missing LinkedIn data, the tool generates a Google search URL to find the company profile
- ✅ **Interactive UI**  
  Filter by priority and view cleaned leads in a sortable, scrollable table
- ✅ **Export Cleaned Leads**  
  Download the fully cleaned and scored dataset in one click

---

## 🧪 Scoring Model Logic

The tool applies a **heuristic rule-based model**:

- +2: Valid business email (not free)
- +2: Revenue ≥ 5000 Cr
- +2: Employees > 10,000
- −1: Missing phone number
- −1: Missing website

➡️ Leads are then classified as:
-  High Priority (score > 6)
-  Medium Priority (score 3–6)
-  Low Priority (score < 3)

---

## 💻 How to Set Up and Run

### 1. Clone the repository
```bash
git clone https://github.com/Sakshii2118/Caprae_Recuritment_Challenge.git
cd caprae-leadgen-scraping
```
### 2. (Optional) Create a virtual environment
```bash
conda create -n caprae-env python=3.10 -y
conda activate caprae-env
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the Streamlit app
```bash
streamlit run caprae_capital_app.py
```
Then go to `http://localhost:8501` in your browser.

---
## 📂 File Structure

```
caprae-leadgen-scraping/
├── caprae_capital_app.py           # Main Streamlit application
├── scrap_leads.csv                 # Sample raw data input
├── caprae_demo_notebook.ipynb      # (Optional) Jupyter Notebook walkthrough
├── caprae_leadgen_scraping_report.pdf  # 1-page strategy report
├── README.md
├── requirements.txt

```

---
## 🎥 Walkthrough Demo

The accompanying 2-minute video demonstrates:

- Uploading a CSV of raw leads  
- Applying deduplication settings  
- Viewing lead scoring results  
- Filtering by High/Medium/Low priority  
- Downloading the cleaned dataset  

---

## 💼 Business Value

This tool aligns directly with Caprae's sales strategy by ensuring that lead data is:

- Accurate  
- Actionable  
- Prioritized for outreach  

Instead of high-volume scraping, it emphasizes **lead quality, completeness, and strategic filtering** — improving conversion rates and saving time for your sales team.

---

## 🙋‍♀️ Submitted By

**Sakshi Gupta**

