import tiktoken


enc = tiktoken.get_encoding("o200k_base")
max_tokens = 4096


def request_validation(data):
    context = ""
    query = ""
    try:
        for item in data['messages']:
            if item['role'] == 'system':
                if context == "":
                    context += item['content']
                else:
                    context += "\n" + item['content']
            elif item['role'] == 'user':
                if query == "":
                    query += item['content']
                else:
                    query += "\n" + item['content']
            elif item['role'] not in ['system', 'user']:
                raise ValueError(f"Invalid role: {item['role']}")
    except KeyError as e:
        raise ValueError(f"KeyError: {e}")
    total_tokens = len(enc.encode(query + context))
    if total_tokens > max_tokens:
        raise ValueError(
            f"Total tokens: {total_tokens} exceeds max tokens: {max_tokens}")
    return query, context


if __name__ == "__main__":
    data = {
        "messages": [
            {
                "role": "system",
                "content": "The author grew up in a large town."
            },
            {
                "role": "user",
                "content": "The author went to college in the city."
            }
        ]
    }
    print(request_validation(data))
    try:
        max_tokens = 10
        print(request_validation(data))
    except ValueError as e:
        print(e)
        max_tokens = 4096
    data = {
        "messages": [
            {
                "role": "system",
                "content": "The author grew up in a large town."
            },
            {
                "role": "user",
                "content": "The author went to college in the city."
            },
            {
                "role": "system",
                "content": "The author went to college in the city."
            }
        ]
    }
    print(request_validation(data))
    data = {
        "messages": [
            {
                "role": "system",
                "content": "The author grew up in a large town."
            },
            {
                "role": "user",
                "content": "The author went to college in the city."
            },
            {
                "role": "system",
                "content": "The author went to college in the city."
            },
            {
                "role": "user",
                "content": "The author went to college in the city."
            }
        ]
    }
    print(request_validation(data))
    data = {
        "messages": [
            {
                "role": "system",
                "content": "The author grew up in a large town."
            },
            {
                "role": "user",
                "content": "The author went to college in the city."
            },
            {
                "role": "system",
                "content": "The author went to college in the city."
            },
            {
                "role": "user",
                "content": "The author went to college in the city."
            },
            {
                "role": "system",
                "content": "The author went to college in the city."
            }
        ]
    }
    print(request_validation(data))