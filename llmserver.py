from flask import Flask, request, jsonify
from flask_cors import CORS
import mlx_lm
import mlx.core as mx
import mlx_lm.models
from huggingface_hub import snapshot_download
from mlx_lm import load, generate
import signal
import sys
import atexit

app = Flask(__name__)
CORS(app)

# Step 1: Download the model
model_name = "mlx-community/DeepSeek-R1-Distill-Llama-8B-8bit"
model_path = snapshot_download(repo_id=model_name)
model, tokenizer = mlx_lm.utils.load(model_path)

def cleanup():
    print("Cleaning up resources...")
    # Add any cleanup code here if needed
    sys.stdout.flush()

def signal_handler(sig, frame):
    print('Received shutdown signal')
    cleanup()
    sys.exit(0)

# Register the cleanup function to run at exit
atexit.register(cleanup)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)  # Handles Ctrl+C
signal.signal(signal.SIGTERM, signal_handler) # Handles termination request

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json.get("prompt")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    # Generate a response from the model
    response = generate(model, tokenizer, prompt=prompt, max_tokens=4096, verbose=True)
    return jsonify({"response": response})

if __name__ == "__main__":
    try:
        # Enable debug mode and allow all incoming connections
        app.run(host="0.0.0.0", port=5001, debug=False)  # Set debug=False for cleaner shutdown
    except Exception as e:
        print(f"Error starting server: {e}")
        cleanup()
        sys.exit(1)