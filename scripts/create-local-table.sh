#!/bin/bash

# Create DynamoDB table for local development
TABLE_NAME="AnalysisResultsTable"
echo "Creating $TABLE_NAME table in local DynamoDB..."

aws dynamodb create-table \
    --table-name $TABLE_NAME \
    --attribute-definitions AttributeName=url,AttributeType=S \
    --key-schema AttributeName=url,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url http://localhost:8000

echo "Table creation initiated. Checking table status..."

# Wait for table to be active
aws dynamodb wait table-exists \
    --table-name $TABLE_NAME \
    --endpoint-url http://localhost:8000

echo "✅ Table '$TABLE_NAME' created successfully!"

# Verify table creation
echo "Table description:"
aws dynamodb describe-table \
    --table-name $TABLE_NAME \
    --endpoint-url http://localhost:8000 \
    --query 'Table.{TableName:TableName,Status:TableStatus,KeySchema:KeySchema}'