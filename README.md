# Retail Sales EDA Project

This project explores a simulated retail company's 7,084 raw transactions from India (2023-2024), documents data cleaning, and analyzes the resulting 7,000-row dataset. It includes a Streamlit dashboard, an EDA notebook, a static HTML dashboard, a written report, and automated data checks.

## Project files

- `app.py` - interactive Streamlit dashboard.
- `Retail_EDA_Project.ipynb` - data-quality audit, cleaning, analysis, and saved cleaned-data export.
- `Retail_EDA_Insights_Report.pdf` - three-page, management-facing findings report for submission.
- `EDA_Insights_Report.docx` - editable Word version of the insights report.
- `Retail_Sales_Dashboard.html` - standalone dashboard; its findings summarize the full dataset, while its filters update KPIs and charts.
- `retail_customer_sales_dataset.csv` - raw input data.
- `cleaned_retail_customer_sales_dataset.csv` - cleaned data used by the dashboard and tests.
- `tests/test_cleaned_data.py` - validation checks for the cleaned data.

## Setup on Windows PowerShell

Run these commands from the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell prevents environment activation, use the virtual-environment interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the Streamlit dashboard

From the project folder, with `.venv` active:

```powershell
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Run the notebook

Open `Retail_EDA_Project.ipynb` in VS Code with the Jupyter extension, select the project's `.venv` Python interpreter as the notebook kernel, and run all cells from top to bottom. Run it from the project folder because the notebook reads the raw CSV and writes `cleaned_retail_customer_sales_dataset.csv` using relative paths.

The packages needed by both the app and notebook are listed in `requirements.txt`, including `ipykernel`, `matplotlib`, `seaborn`, and `missingno`.

## Run the data checks

From the project folder, with `.venv` active:

```powershell
python -m pytest tests -v
```

## Interpretation note

Discount and delivery comparisons in this project are descriptive analyses of the available records. Correlations and group averages do not establish cause and effect. In particular, delivery-date quality and the recorded cost model limit conclusions about delivery speed and discount profitability.
