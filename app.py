from flask import Flask, request, jsonify
from validator import \
    request_validation, invalid_request
from rag.graph_store import GraphStore
from rag.vector_store import VectorStore
from rag.node_processor import node_processors
from rag.inference import Inference

vector_store = VectorStore()
graph_store = GraphStore()
node_processors = [
    node_processors.get("community_processor"),
    node_processors.get("influence_processor"),
    node_processors.get("community_score_processor"),
    node_processors.get("influence_score_processor"),
    node_processors.get("llama_processor"),
]
inference = Inference(vector_store, graph_store, node_processors)


app = Flask(__name__)


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    question, context = request_validation(data)
    invalid_request(data)
    answer = inference.get_response(question)
    data["messages"].append({
        "role": "system",
        "content": answer
    })
    return jsonify(data["messages"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
