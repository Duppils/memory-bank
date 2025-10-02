echo "Starting system initialization..."

echo "Waiting for core services to become available..."

/usr/local/bin/wait-for-it.sh ollama:11434 -t 30 --strict -- echo "Ollama is ready."

/usr/local/bin/wait-for-it.sh qdrant:6333 -t 30 --strict -- echo "Qdrant is ready."

/usr/local/bin/wait-for-it.sh n8n:5678 -t 30 --strict -- echo "n8n is ready."

echo "All services are up. Proceeding with configuration."

echo "Configuring Ollama..."
python3 /app/scripts/setup_ollama.py

echo "Configuring Qdrant..."
python3 /app/scripts/setup_qdrant.py

docker exec n8n \
  n8n import:workflow \
  --input=/home/node/.n8n/config/memory_ingest_workflow.json

echo "Initialization complete!"