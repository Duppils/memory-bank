import requests
import os
import sys
import json

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://ollama:11434")
MODELS = ["nomic-embed-text", "llama3.2:3b"]

def pull_model_and_wait(model_name):
    print(f"Checking/Pulling model: {model_name}...")
    
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/pull", 
            json={"name": model_name, "stream": True}, 
            stream=True, 
            timeout=3600
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error initiating pull for {model_name}: {e}")
        return False
    
    last_status = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                
                if 'error' in data:
                    print(f"Ollama Error: {data['error']}", file=sys.stderr)
                    return False

                status = data.get('status', 'Processing...')
                if status != last_status:
                    print(f"[{model_name}] Status: {status}")
                    last_status = status
                    
                if status.startswith("success") or status.startswith("The model is already available"):
                    print(f"Model {model_name} successfully downloaded/available.")
                    return True
            except json.JSONDecodeError:
                print(f"Received non-JSON line: {line.decode('utf-8')}")
    
    print(f"Error: Model {model_name} pull failed or did not finish.")
    return False


def main():
    print(f"Ollama URL: {OLLAMA_URL}")

    for model in MODELS:
        pull_model_and_wait(model)
    
    print("Ollama setup script finished.")

if __name__ == "__main__":
    main()