#!/usr/bin/env python3
from huggingface_hub import snapshot_download
import mlx.core as mx
import mlx_lm
import mlx_lm.models
from mlx_lm import load, generate

# Step 1: Download the model
model_name = "mlx-community/DeepSeek-R1-Distill-Llama-8B-8bit"
model_path = snapshot_download(repo_id=model_name)

# Step 2: Load the model
model, tokenizer = mlx_lm.utils.load(model_path)

# Path where the model was downloaded
#model_path = "/Users/mike/.cache/huggingface/hub/models--mlx-community--DeepSeek-R1-Distill-Llama-70B-8bit/snapshots/e2d7c57b02d34dbc4962ab7df154afdea0f6a44c"
# model, tokenizer = mlx_lm.utils.load(model_path)
def chat_with_model(prompt):
#    response = generate(model, tokenizer, prompt=prompt, verbose=True)
#    output = model.generate(prompt, max_tokens=200)

    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template is not None:
        messages = [{"role": "user", "content": prompt}]
        prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

    response = generate(model, tokenizer, prompt=prompt, max_tokens=2048, verbose=True) 

    return response

def main():
    while True:
        user_input = input("Enter your message (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        response = chat_with_model(user_input)
        print("\nAssistant:", response)

if __name__ == "__main__":
    main()