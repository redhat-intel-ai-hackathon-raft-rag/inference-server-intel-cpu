from llm_models import tokenizer

def vectorize_input(input_text):
    input_ids = tokenizer(input_text, max_length=768, truncation=True, padding='max_length', return_tensors='np')
    return input_ids["input_ids"]


if __name__ == "__main__":
    input_text = " #Question: What is the meaning of life?"
    instruction = """#Instruction:
         - Please provide a short answer.
         - Answer should be one sentence.
         """
    instruction = instruction.replace("  ", "").replace("  ", "").replace("\n", "")
    context = " #Context: The meaning of life is to be happy."
    print(vectorize_input(input_text + instruction + context))