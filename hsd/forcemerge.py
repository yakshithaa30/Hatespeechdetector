import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

base_model_name = "Qwen/Qwen2.5-1.5B-Instruct"
adapter_dir = "./model"  # The folder containing your adapter_config.json
output_dir = "./merged_fine_tuned_model"

print("Step 1: Loading clean base model...")
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.float32,
    device_map="cpu"
)
tokenizer = AutoTokenizer.from_pretrained(base_model_name)

print("Step 2: Explicitly binding your fine-tuned weights...")
# This forces the script to wrap the base weights with your trained parameters
model = PeftModel.from_pretrained(base_model, adapter_dir)

print("Step 3: Merging weights permanently...")
model = model.merge_and_unload()

print("Step 4: Overwriting the folder with the authentic model...")
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print("\nSUCCESS: Your authentic fine-tuned model is fully created!")