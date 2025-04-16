# Azure Data Factory Pipeline

## Purpose
This pipeline orchestrates the ETL process by triggering a Databricks notebook to read raw CSVs from Azure Blob, transform them with PySpark, and write cleaned results back to Blob.

## Components
- Trigger: Manual (can be scheduled later)
- Activities:
    - Run Databricks notebook
- Linked Services:
    - Azure Blob Storage
    - Azure Databricks

## Deployment
Use `deploy_adf.sh` to deploy the pipeline from `adf_pipeline.json`.
