#!/bin/bash

# === CONFIGURE THESE VARIABLES ===
RESOURCE_GROUP="your-resource-group"
FACTORY_NAME="your-datafactory-name"
PIPELINE_NAME="RunDatabricksETL"
TEMPLATE_FILE="azure/adf_pipeline.json"

# === DO NOT EDIT BELOW UNLESS NEEDED ===
echo "Deploying pipeline: $PIPELINE_NAME to Data Factory: $FACTORY_NAME"

az datafactory pipeline create \
  --resource-group $RESOURCE_GROUP \
  --factory-name $FACTORY_NAME \
  --name $PIPELINE_NAME \
  --pipeline "$(cat $TEMPLATE_FILE)"

echo "✅ Deployment completed."
