import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Paths based on your folder structure
base_model_path = "Qwen/Qwen2.5-1.5B-Instruct"  # Download the base weights from HF automatically
adapter_path = "./model"                       # Your folder containing adapter_config.json and adapter_model.safetensors
output_path = "./merged_fine_tuned_model"      # Where to save the final true model

print("Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(base_model_path, torch_dtype="auto", device_map="cpu")
tokenizer = AutoTokenizer.from_pretrained(base_model_path)

print("Loading your fine-tuned adapters...")
model = PeftModel.from_pretrained(base_model, adapter_path)

print("Merging weights permanently...")
merged_model = model.merge_and_unload()

print("Saving final model files...")
merged_model.save_pretrained(output_path)
tokenizer.save_pretrained(output_path)
print(f"Successfully merged! Saved to {output_path}")