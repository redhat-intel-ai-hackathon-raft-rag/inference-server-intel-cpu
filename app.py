import faiss
import numpy as np
from transformers import pipeline
from flask import Flask, request, jsonify
from inference import inference
from vector_store import PreviousOutputVectorStore
from vector_store import RaftStore
from embedding import vectorize_input

app = Flask(__name__)
previous_output_vector_store = PreviousOutputVectorStore()
cutoff_rate = 0.1

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    question = ""
    context = ""
    answer = ""
    try:
        for item in data['messages']:
            if item['role'] == 'system':
                context += item['content']
            elif item['role'] == 'user':
                question = item['content']
            elif item['role'] not in ['system', 'user']:
                raise ValueError(f"Invalid role: {item['role']}")
    except KeyError as e:
        return jsonify({'error': f"KeyError: {str(e)}"})
    # Vectorize the input
    vector = vectorize_input(question + context)
    # Check if there are significantly similar inputs in vector store
    distances, index = previous_output_vector_store.search_vector(vector)
    if distances[0][0] < cutoff_rate:
        data["messages"].append({
            'role': 'system',
            'content': previous_output_vector_store.get_output_text(
               previous_output_vector_store.get_input_text(index[0][0])
               )
            })
        return jsonify(data)
    # Perform inference
    answer = inference(question, context)
    # Store in vector store
    previous_output_vector_store.add_vector(vector, question + context, answer)
    data["messages"].append({'role': 'system', 'content': answer})
    return jsonify(data["messages"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
