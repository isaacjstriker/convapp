# Convapp

Convapp is a small Python web application that converts spreadsheet data from Google Sheets exports (`.xlsx`) into CSV files compatible with a proprietary line-of-business system.

It was originally built for a local non-profit that needed to migrate **~25,000 rows** of territory mapping data. A manual approach would have taken months. Convapp automates the entire process, validating and reshaping the data so it can be imported reliably in just a couple of days.

---

## Why I built this

A local non-profit was moving to new software for managing territory data. All of their data lived in Google Sheets, scattered across multiple tabs and columns with inconsistent formatting.

Manually copying this into the new system would have been:

- Error‑prone
- Extremely time‑consuming
- Hard to keep in sync as the data changed

I built Convapp to:

- Take their **Google Sheets `.xlsx` exports**,
- Normalize and validate the data,
- Output **CSV files** that matched the **exact schema** required by their proprietary software.

This turned a months‑long manual process into a **two‑day automated migration**.

---

## Features

- **XLSX → CSV conversion** customized for the target system’s schema
- **Data cleaning & transformation** using `pandas`
- **Schema mapping**:
  - Maps human‑friendly column names to system fields
  - Handles type conversions and normalization
- **Validation & logging**:
  - Flags and logs problematic rows before export
  - Helps catch issues early instead of during import
- Simple **web interface** (via Flask) for running conversions

---

## Tech Stack

- **Backend:** Python, Flask
- **Data Processing:** `pandas`
- **Frontend:** HTML, CSS
- **Other:** CSV, XLSX

---

## How it works (high level)

1. **Upload XLSX**  
   User uploads a Google Sheets export (or the script reads from a known location).

2. **Parse & validate**  
   `pandas` reads the workbook into DataFrames, performs type checks, and validates required fields.

3. **Transform**  
   Data is:
   - Normalized (e.g., trimming whitespace, standardizing codes)
   - Mapped to the target CSV schema
   - Filtered for invalid or incomplete rows

4. **Export CSV**  
   A clean CSV is generated that can be imported directly into the proprietary system.

5. **Logs & reports**  
   Any issues (missing fields, invalid codes) are logged for review.

---

## Running locally

> Note: This project was built for a specific client and schema, so it’s more of a **reference implementation** than a generic tool. The steps below illustrate the setup.

### Prerequisites

- Python 3.10+ (or similar)
- `pip` or `pipenv`/`poetry`

### Setup

```bash
git clone https://github.com/isaacjstriker/convapp.git
cd convapp

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open `http://localhost:5000` (or whatever port is configured) in your browser.

---

## Key learning points

Convapp gave me practical experience with:

- Designing a **data pipeline** around messy real-world spreadsheets
- Using **pandas** for robust transformation and validation
- Thinking in terms of **schemas**, not just files
- Building a small but useful **Flask** app to expose that logic to non-technical users
- Communicating with stakeholders to understand their target system and edge cases

---

## Potential Future improvements (ideas)

- Make the mapping configuration **data‑driven** (e.g., YAML/JSON instead of hard‑coded)
- Add a simple **UI for mapping columns** between source and target
- Support **multiple export formats** and schemas
- Add more robust **test coverage** for unusual edge cases
