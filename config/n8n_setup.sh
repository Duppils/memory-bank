CREDENTIALS_FILE="/setup/credentials.json"
WORKFLOW_INGEST_FILE="/setup/memory_ingest_workflow.json"
WORKFLOW_RETRIEVAL_FILE="/setup/memory_retrieval_workflow.json"

echo "Starting n8n setup and configuration..."

echo "Attempting to import credentials..."
n8n import:credentials --input ${CREDENTIALS_FILE} --import-with-new-id

echo "Importing and activating ingest workflow..."
n8n import:workflow --input ${WORKFLOW_INGEST_FILE} --activate

echo "Importing and activating retrieval workflow..."
n8n import:workflow --input ${WORKFLOW_RETRIEVAL_FILE} --activate

echo "Setup complete!"