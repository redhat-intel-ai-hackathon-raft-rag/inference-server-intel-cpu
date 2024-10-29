from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from optimum.intel import OVModelForCausalLM, OVWeightQuantizationConfig
import nltk
nltk.download('punkt')  # Download the punkt tokenizer
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize


# model_id = "./qwen_lora"
model_id = "./models/qwen2.5-1.5B_lora_sft"
quantization_config = OVWeightQuantizationConfig(bits=4, sym=False, ratio=0.8, quant_method="awq", scale_estimation=True, dataset="wikitext2")
model = OVModelForCausalLM.from_pretrained(model_id, quantization_config=quantization_config)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")

ov_pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

def generate_answer(question, context):
    results = ov_pipe(
        f"{context} {question}",
        cache_implementation="offloaded_static",
        num_return_sequences=10,
        min_new_tokens=5,
        max_new_tokens=40,
        top_p=0.90, 
        top_k=30,
        do_sample=True,
        num_beams=10,
        renormalize_logits=True,
        early_stopping=True,
        eta_cutoff=2e-3,
        epsilon_cutoff=9e-4,
        repetition_penalty=100.0,
        encoder_repetition_penalty=100.0,
        no_repeat_ngram_size=3,
        exponential_decay_length_penalty=(len(f"{question}{context}") + 10, -20.0) 
        )
    best_answer = ""
    better_answer = ""
    for result in results:
        answer = result["generated_text"]
        # remove {context}{question} from the answer
        answer = answer.replace(f"{context}{question}", "")
        answer = sent_tokenize(answer)
        if not answer[-1].endswith(".") and not answer[-1].endswith('."') and not answer[-1].endswith("?") and not answer[-1].endswith("!"):
            answer = answer[0:-1]
        answer = " ".join(answer)
        if answer != "":
            if "Answer " or "answer" or "Solution " or "solution" or "Response " or "response" in answer:
                if best_answer == "":
                    best_answer = answer
                elif len(answer) < len(best_answer):
                    best_answer = answer
            if better_answer == "":
                better_answer = answer
            elif len(answer) > len(better_answer):
                better_answer = answer
    if best_answer == "" and better_answer == "":
        return generate_answer(question, context)
    if len(best_answer) == 0:
        return better_answer
    return best_answer