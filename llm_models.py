import os
from transformers import AutoTokenizer
from optimum.intel import OVModelForCausalLM, OVWeightQuantizationConfig
from llama_index.llms.openvino import OpenVINOLLM
from prompt_template import completion_to_prompt, messages_to_prompt
from device import device

if os.path.exists("./qwen_lora_openvino"):
    model_id = "./qwen_lora_openvino"
else:
    model_id = "./models/qwen2.5-1.5B_lora_sft"
    quantization_config = OVWeightQuantizationConfig(
        bits=4, sym=False,
        ratio=0.8, quant_method="awq",
        scale_estimation=True, dataset="wikitext2"
    )
    model = OVModelForCausalLM.from_pretrained(
        model_id, quantization_config=quantization_config
    )
    model.save_pretrained("./qwen_lora_openvino")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
    tokenizer.save_pretrained("./qwen_lora_openvino")
llm = OpenVINOLLM(
    model_id_or_path="qwen_lora_openvino",
    context_window=3900,
    max_new_tokens=256,
    model_kwargs={"ov_config": {
        "KV_CACHE_PRECISION": "u8",
        "DYNAMIC_QUANTIZATION_GROUP_SIZE": "32",
        "PERFORMANCE_HINT": "LATENCY",
        "NUM_STREAMS": "1",
        "CACHE_DIR": "",
    }},
    generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    device_map=device
)
