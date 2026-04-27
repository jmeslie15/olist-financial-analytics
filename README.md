# Brazilian E-Commerce Financial Analytics Pipeline

## 📌 Executive Summary
This project analyzes 100,000+ anonymized transactions from Olist, a Brazilian e-commerce marketplace. The goal was to uncover consumer credit behavior, highlighting the correlation between extended installment financing and high-value cart conversions. 

### 📥 Project Files
* **[📄 View the Dashboard Report (PDF)](./Olist_Financial_Dashboard.pdf)** - A static, high-resolution export of the multi-page dashboard.
* **[📊 Download the Power BI File (.pbix)](./Olist_Financial_Dashboard.pbix)** - The raw Power BI file (requires Power BI Desktop to open).

## 🏗️ Architecture & Technologies Used
* **Data Engineering:** Python (`pandas`, `sqlalchemy`, `pymysql`) 
* **Database:** MySQL
* **Data Visualization:** Power BI
* **Techniques:** Programmatic Data Ingestion, Multi-level SQL CTEs, Dimensional Modeling, AI-driven Decomposition Trees.

## ⚙️ The ETL Pipeline
Engineered a programmatic Python ingestion script (`scripts/01_load_mysql.py`) and a robust SQL pipeline to transform the raw data:
1. **Ingestion:** Bypassed GUI limitations by using `pandas` and `sqlalchemy` to bulk-load 5 disparate raw CSV files directly into a local MySQL database.
2. **Transformation:** Executed multi-level SQL Common Table Expressions (CTEs) to aggregate item-level transactions into basket-level financial metrics without data fan-out.
3. **Export:** Exported a flattened, enriched `olist_powerbi_master.csv` specifically optimized for Power BI reporting.

## 📊 Key Business Insights
* **Credit Reliance:** Analyzed over 99k orders, proving that baskets exceeding $250 are heavily dependent on long-term (6x+) financing options.
* **Geographic Purchasing Power:** Identified key states driving Gross Merchandise Value (GMV) utilizing Power BI's AI Decomposition Tree for root-cause analysis.
* **Payment Complexity:** Segmented single vs. split-payment behaviors to identify friction points in high-value checkout flows.

## 📸 Dashboard Gallery

<img width="1299" height="735" alt="dashboard_page_3" src="https://github.com/user-attachments/assets/61795dd6-283c-4aad-a423-014a263a3b63" />
<img width="1304" height="732" alt="dashboard_page_2" src="https://github.com/user-attachments/assets/3c5b3689-816f-4271-9ff6-89cc55c015a0" />
<img width="1296" height="734" alt="dashboard_page_1" src="https://github.com/user-attachments/assets/831c1fca-afb4-401d-a7b9-bf14d2d25a51" />

