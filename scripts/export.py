from optimum.intel import OVModelForCausalLM
from transformers import AutoTokenizer


model_id = "./models/qwen2.5-1.5B_lora_sft"
model = OVModelForCausalLM.from_pretrained(model_id, export=True)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")

save_directory = "qwen_lora"
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)
