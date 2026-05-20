![Python](https://img.shields.io/badge/Python-Data_Engineering-blue)
![PySpark](https://img.shields.io/badge/PySpark-Big_Data-orange)
![Azure](https://img.shields.io/badge/Azure-Cloud-blue)
![Databricks](https://img.shields.io/badge/Databricks-ETL-red)
![PowerBI](https://img.shields.io/badge/PowerBI-Analytics-yellow)
![DeltaLake](https://img.shields.io/badge/Delta_Lake-Lakehouse-green)

# Azure Data Platform Project

## Overview
This project demonstrates an end-to-end Azure-style cloud data engineering pipeline using PySpark, Delta Lake, Azure architecture principles, and Power BI-ready data modelling.

The project showcases production-style data engineering concepts including:
- ETL/ELT pipeline development
- Data cleansing & transformation
- Schema validation
- Delta Lake processed layer
- Analytics-ready reporting architecture
- Cloud engineering repository structure

## Project Status
✅ Active Portfolio Project  
✅ Production-style Architecture  
✅ PySpark ETL Pipeline  
✅ Power BI Reporting Layer  

---

## Architecture

![Architecture Diagram](docs/Architecture.png)

### Architecture Flow

```text
CSV Sales Data
      ↓
ADLS Gen2
      ↓
Azure Databricks (PySpark ETL/ELT)
      ↓
Delta Lake Processed Layer
      ↓
Power BI Analytics Dashboard
```

---

## Tech Stack

- Azure Databricks
- PySpark
- Delta Lake
- Azure Data Factory
- ADLS Gen2
- Power BI
- Python
- SQL Server
- GitHub Actions
- Docker

---

## Key Features

- Batch data ingestion from CSV
- Schema inference
- Data cleansing and deduplication
- Data type casting
- Data quality validation
- Delta Lake processed layer
- Analytics-ready reporting model
- Production-style repository structure

---

## Business Use Case

This pipeline processes sales transaction data and prepares it for business analytics and reporting.

The processed dataset supports:
- Revenue analysis by region
- Product category insights
- Payment method analysis
- Daily sales trends
- Customer purchasing behaviour

---

## Repository Structure

```text
azure-data-platform/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── pipelines/
│   └── etl_pipeline.py
│
├── src/
│   ├── ingestion/
│   ├── transformation/
│   └── loading/
│
├── tests/
│
├── docs/
│   ├── Architecture.png
│   └── powerbi-dashboard.png
│
├── powerbi/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Pipeline Logic

The PySpark ETL pipeline performs:

1. Extract raw sales data from CSV
2. Infer schema automatically
3. Remove duplicate records
4. Parse and standardise dates
5. Cast numeric fields
6. Validate required columns
7. Remove invalid records
8. Add pipeline load timestamp
9. Write processed data into Delta Lake format

---

## Power BI Dashboard

![Power BI Dashboard](powerbi/powerbi-dashboard.png)

Dashboard includes:
- Total Revenue KPI
- Total Orders KPI
- Customer Metrics
- Revenue by Region
- Product Category Analysis
- Daily Sales Trends
- Payment Method Insights

---

## Engineering Concepts Demonstrated

- ETL/ELT pipeline design
- Lakehouse architecture
- Data quality validation
- Cloud analytics engineering
- PySpark transformations
- Delta Lake storage
- Analytics reporting integration
- Production-style project structuring

---

## Future Enhancements

- Add Azure Data Factory orchestration
- Implement incremental loading
- Add unit testing with PyTest
- Deploy using Azure DevOps CI/CD
- Add streaming ingestion pipeline
- Add monitoring & alerting
- Integrate Terraform IaC

---

## Author

Korneli Pingula  
Senior Data Engineer | Azure • AWS • Databricks • PySpark • SQL • Power BI

LinkedIn:
linkedin.com/in/pingulakornelius

GitHub:
github.com/Kornelius99
