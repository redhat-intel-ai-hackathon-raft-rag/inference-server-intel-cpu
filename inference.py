import time
import torch
from llm_models import generate_answer

instruction = "#Instruction: - Please provide a short answer. - Answer should be one sentence. "

def inference(question, context):
    start_time = time.time()
    if context != "":
        context = "#Context:" + context
    answer = generate_answer(question, instruction + context)
    end_time = time.time()
    print(f"Inference time: {end_time - start_time}")
    return answer

if __name__ == '__main__':
    input_text = "#Question: What is the meaning of life?"
    context = " #Context: The meaning of life is to be happy."
    print(inference(input_text, instruction + context))
