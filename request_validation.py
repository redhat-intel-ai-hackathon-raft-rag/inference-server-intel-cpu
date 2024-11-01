import tiktoken


cutoff_rate = 0.1
enc = tiktoken.encoding_for_model("Qwen/Qwen2.5-1.5B-Instruct")
max_tokens = 4096  # Set a suitable max token limit


def request_validation(data):
    context = "",
    question = ""
    try:
        for item in data['messages']:
            if item['role'] == 'system':
                context += item['content']
            elif item['role'] == 'user':
                question = item['content']
            elif item['role'] not in ['system', 'user']:
                raise ValueError(f"Invalid role: {item['role']}")
    except KeyError as e:
        raise ValueError(f"KeyError: {e}")
    total_tokens = len(enc.encode(question + context))
    if total_tokens > max_tokens:
        raise ValueError(
            f"Total tokens: {total_tokens} exceeds max tokens: {max_tokens}")
    return question, context
