# Smart Patient Readmission Risk Analytics

A Databricks-based data engineering and analytics project that analyzes hospital patient admissions and identifies patterns associated with 30-day patient readmission risk.

## Project Overview

This project implements a Medallion Architecture using Bronze, Silver, and Gold layers in Databricks. Patient, admission, and diagnosis data is processed through ingestion, cleaning, enrichment, feature engineering, and aggregation stages to produce business-ready analytics.

The final solution provides a Databricks Executive Overview dashboard containing healthcare KPIs, readmission trends, risk distribution, demographic analysis, and high-risk patient profiles.

## Architecture

![Smart Patient Readmission Risk Pipeline](architecture/smart_patient_readmission_architecture.png)

### Data Flow

```text
Patient Data + Admission Data + Diagnosis Data
                    |
                    v
             Data Ingestion
                    |
                    v
              Bronze Layer
                    |
                    v
       Cleaning / Validation / Enrichment
                    |
                    v
               Silver Layer
                    |
                    v
       Feature Engineering + Risk Scoring
                    |
                    v
                Gold Layer
                    |
                    v
          Databricks Dashboard
```

## Medallion Architecture

### Bronze Layer

Initial patient and admission data is ingested into Databricks.

Example datasets:
- `bronze_patients`
- `bronze_admissions`
- `bronze_diagnosis`

### Silver Layer

The Silver layer cleans and enriches the source data and combines patient, admission, and diagnosis information.

Important attributes include:
- Patient information
- Age and age group
- Gender
- Diagnosis
- Department
- Length of stay
- Previous admissions
- Readmission information
- Risk-related features

### Gold Layer

The Gold layer contains business-ready analytical datasets used by the dashboard.

Key outputs include:
- Readmission rate by diagnosis
- Department performance
- Readmission rate by age group
- Patient risk profiles
- Monthly readmission trends

## Dashboard

The Executive Overview dashboard contains:

- **Total Patients:** 199
- **Total Admissions:** 692
- **Total Readmissions:** 153
- **Overall Readmission Rate:** 22.11%
- **Average Length of Stay:** 5.78 days
- Readmission Rate by Department
- Readmission Rate by Diagnosis
- Monthly Readmission Rate Trend
- Patient Risk Distribution
- Readmission Rate by Age Group
- High-Risk Patient Profiles

![Executive Dashboard](dashboard/executive_overview.png)

## Key Insights

Based on the project datasets:

- Respiratory cases have a readmission rate of approximately **28.70%**.
- Cardiovascular cases have a readmission rate of approximately **28.32%**.
- ICU has the highest department-level readmission rate shown in the dashboard at approximately **31.87%**.
- Elderly patients have the highest age-group readmission rate at approximately **30.13%**.
- The highest observed monthly readmission rate is **30.88% in May 2026**.
- Patient risk distribution contains **93 High-risk**, **78 Medium-risk**, and **28 Low-risk** patients.

## Risk Distribution

| Risk Category | Patient Count |
|---|---:|
| High | 93 |
| Medium | 78 |
| Low | 28 |

## Technology Stack

- Databricks
- Apache Spark / PySpark
- Python
- SQL
- Delta Tables
- Databricks SQL Dashboards
- Git & GitHub

## Repository Structure

```text
Smart-Patient-Readmission-Risk-Analytics/
│
├── notebooks/
│   ├── generate_data.py
│   ├── silver_transform.py
│   └── gold_aggregations.py
│
├── dashboard/
│   └── Smart Patient Readmission Risk Analytics 2026-08-10 18_06
│
├── architecture/
│   └── smart_patient_readmission_architecture.png
│
├── screenshots/
│   ├── admission spark frame
│   ├── age group risk
│   ├── gold layer validation
│   └── silver layer verification
│
├── docs/
│   └── Smart_Patient_Readmission_Risk_Analytics_Report.docx
│
├── README.md
└── .gitignore
```

## Data Pipeline

### 1. Data Generation and Ingestion
Patient and admission datasets are created as Spark DataFrames and loaded into the Bronze layer.

### 2. Silver Transformation
The Silver transformation cleans, joins, and enriches the source datasets to create an analytical patient-admission dataset.

### 3. Feature Engineering
Important features include age, age group, comorbidities, length of stay, previous admissions, diagnosis, and discharge information.

### 4. Risk Analysis
Patient and group-level readmission metrics are calculated to identify populations with higher readmission risk.

### 5. Gold Aggregations
Business-ready datasets are generated for diagnosis analysis, department performance, age-group risk, and patient risk profiles.

### 6. Dashboard
Gold datasets are visualized through Databricks dashboard widgets for business-oriented analysis.

## Validation

The pipeline includes validation steps for the different layers.

Example Gold-layer validation results:

```text
Readmission by Diagnosis rows: 9
Department Performance rows: 7
Age Group Risk rows: 5
Patient Risk Profiles rows: 199
```

## Project Objective

The objective is to demonstrate how healthcare admission data can be processed through a modern data pipeline and transformed into actionable readmission-risk analytics using Databricks and Apache Spark.

The project demonstrates:
- Data ingestion
- Data transformation
- Medallion architecture
- Feature engineering
- Risk analysis
- Data validation
- Business intelligence
- Dashboard-based analytics

## Future Enhancements

- Add machine-learning-based readmission prediction.
- Implement automated pipeline scheduling.
- Add incremental data ingestion.
- Add data-quality monitoring and alerts.
- Add interactive dashboard filters.
- Add automated notifications for high-risk patients.

## Author

**Anushka Patil**

B.E. Computer Engineering

---

> This project is intended for educational and portfolio purposes. The healthcare data is used for analytics demonstration and should not be treated as real clinical decision-making data.
