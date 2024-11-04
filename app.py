from flask import Flask, request, jsonify, Response
from request_validation import request_validation
# from rag.graph_store import GraphStore
from rag.vector_store import VectorStore
from rag.node_processor import sim_processor, reranker
from rag.inference import Inference
from dotenv import load_dotenv

load_dotenv()
vector_stores = [
    VectorStore(collection_name="webpage_document"),
    VectorStore(collection_name="webpage_raft"),
    VectorStore(collection_name="book_document"),
    VectorStore(collection_name="book_raft")
]
# graph_store = GraphStore()
node_processors = [
    sim_processor,
    # reranker
]
inference = Inference(
    vector_stores=vector_stores,
    node_processors=node_processors
)
app = Flask(__name__)


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    query, context = request_validation(data)
    answer = inference.get_response(query, context)
    response = answer["response"]
    if answer["streaming"]:
        return Response(response.response_gen, content_type='text/event-stream')
    else:
        data["messages"].append({
            "role": "system",
            "content": response,
        })
        return jsonify(data["messages"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
