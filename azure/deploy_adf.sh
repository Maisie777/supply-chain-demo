#!/bin/bash

# Variables
RESOURCE_GROUP="your-resource-group"
FACTORY_NAME="your-datafactory-name"
PIPELINE_NAME="RunDatabricksETL"

# Deploy pipeline using exported ARM template
az deployment group create \
  --name ADFDeployment \
  --resource-group $RESOURCE_GROUP \
  --template-file azure/adf_pipeline.json \
  --parameters factoryName=$FACTORY_NAME

echo "✅ Azure Data Factory pipeline deployed!"