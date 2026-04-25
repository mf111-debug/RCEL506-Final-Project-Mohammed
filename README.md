# Saudi Arabia Defense Localization Analysis (2010–2030)
## Assessing Progress Toward 50% Defense Localization by 2030

**Course:** RCEL 506 — Applied Statistics and Data Science for Engineering Leaders  
**Institution:** Rice University  
**Author:** Mohammed Farran  
**Date:** April 2026

---

## Business Problem

Saudi Arabia's Vision 2030 targets 50% defense sector localization by 2030, up from 4% in 2018. This project builds a data-driven forecasting model to assess the trend in Saudi Arabia's arms import dependency as a proxy indicator of localization progress from 2010 to 2024.

---

## Solution

A time series forecasting pipeline that tracks Saudi Arabia's monthly arms import dependency ratio — defined as Chapter 93 arms imports divided by total military expenditure — using publicly available international trade and defense spending data.

Three models were built and compared:

| Model | R² | RMSE | Role |
|---|---|---|---|
| Rolling Mean | -0.11 | 1.19% | Naive Baseline |
| Linear Regression | **0.47** | **0.82%** | **Best Model** |
| Prophet | -1.15 | 1.65% | Time Series Forecast |

Linear Regression outperformed all models on the test period (2023–2024). Prophet was used for long-term trend forecasting to 2030.

---

## Key Finding

Saudi Arabia's arms import dependency peaked at **10.85%** in May 2015 during the Yemen conflict and declined to **2.29%** by December 2024 — a **77.4% reduction**. The forecast projects this ratio remaining stable and low through 2030. This trend is directionally consistent with GAMI's official localization data showing progress from 4% (2018) to 24.89% (2024). Whether the 50% target will be reached cannot be confirmed from public trade data alone.

---

## Repository Contents

| File | Description |
|---|---|
| `GitHub_Final_Project.ipynb` | Complete analysis notebook (14 cells) |
| `RCEL506_Final_Presentation_v2.pptx` | Final presentation slides |
| `TradeData_2010.csv` ... `TradeData_2024.csv` | UN Comtrade monthly arms imports to Saudi Arabia |
| `sipri_milex_raw.xlsx` | SIPRI military expenditure database |

---

## How to Run

1. Open `GitHub_Final_Project.ipynb` in Google Colab
2. Upload all CSV and Excel files from this repository
3. Run all cells in order from Cell 1 to Cell 14

Install required library before running:
!pip install prophet

---

## Data Sources

| Source | Variable | Frequency | Period |
|---|---|---|---|
| UN Comtrade (mirror data) | Arms imports to Saudi Arabia (HS Chapter 93, USD) | Monthly | 2010–2024 |
| SIPRI Military Expenditure Database | Saudi military spending (constant 2024 USD millions) | Annual ÷ 12 | 2010–2024 |

**Note on mirror data:** Saudi Arabia does not self-report arms imports to UN Comtrade. This project uses exports reported by all trading partners to Saudi Arabia as a proxy — a standard methodology in defense trade research.

---

## Methodology

**Target Variable:**
Import Dependency % = (Arms Imports USD / Military Expenditure USD) × 100

**Features used in Linear Regression:**
- Year, Month
- Lag_1 — last month's value
- Lag_3 — value 3 months ago
- Lag_12 — same month last year
- Rolling_3 — 3-month moving average
- Rolling_12 — 12-month moving average

**Train/Test Split:** Time-based split to prevent data leakage
- Train: January 2011 – December 2022 (144 months)
- Test: January 2023 – December 2024 (24 months)

---

## Limitations

- HS Chapter 93 covers arms and ammunition only — excludes aircraft, ships, and vehicles
- Military expenditure includes personnel and operations costs, not procurement only
- Results represent directional trends, not absolute localization percentages
- Direct localization data is not publicly available — import dependency is used as a proxy

---

## Author

**Mohammed Farran**  
Rice University — RCEL 506  
April 2026
