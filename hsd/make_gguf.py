import os
from gguf import GGUFWriter

print("Converting your merged weights to GGUF format...")
# This automatically handles generating a direct GGUF mapping for Ollama
os.system("python -m gguf.convert_hf_to_gguf ./merged_fine_tuned_model --outfile ./model/final_fine_tuned.gguf")
print("Conversion process finished!")