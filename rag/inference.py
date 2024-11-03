from typing import List
import uuid
from llama_index.core.settings import Settings
from llama_index.core.schema import NodeWithScore, TextNode
from llama_index.core.postprocessor import BaseNodePostprocessor
from embedding import embedding
from llm_models import llm
from rag.graph_store import GraphStore
from rag.response_synthesizer import response_synthesize
from rag.vector_store import VectorStore
# from llm_config import SUPPORTED_LLM_MODELS
from dotenv import load_dotenv

load_dotenv()


class Inference:
    def __init__(self,
                 vector_stores: List[VectorStore],
                 graph_stores: List[GraphStore] = [],
                 node_processors: List[BaseNodePostprocessor] = []):
        Settings.embed_model = embedding
        Settings.llm = llm
        self.vector_stores = [
            vector_store for vector_store in vector_stores
            if vector_store.index is not None
        ]
        self.graph_stores = [
            graph_store for graph_store in graph_stores
            if graph_store.index is not None
        ]
        self.node_processors = node_processors
        # llm_model_configuration = \
        #   SUPPORTED_LLM_MODELS['English']['qwen2.5-1.5b-instruct']
        # llm.max_new_tokens = 2048
        # stop_tokens = llm_model_configuration.get("stop_tokens")
        # if stop_tokens is not None:
        #     llm._stopping_criteria = StoppingCriteriaList(stop_tokens)

    def get_response(self, query, context, top_k=3):
        nodes = []
        nodes.append(self.get_node_from_context(context))
        for vector_store in self.vector_stores:
            nodes.extend(vector_store.retrieve(query, top_k))
        for vector_store in self.vector_stores:
            nodes.extend(vector_store.retrieve(context, top_k))
        for graph_store in self.graph_stores:
            nodes.extend(graph_store.retrieve(query, top_k))
        for graph_store in self.graph_stores:
            nodes.extend(graph_store.retrieve(context, top_k))
        for processor in self.node_processors:
            nodes = processor.postprocess_nodes(nodes)
        return response_synthesize(query, nodes)

    def get_node_from_context(self, context):
        text_Node = TextNode(
            id_=str(uuid.uuid4()),
            text=context
        )
        return NodeWithScore(
            node=text_Node,
            score=0.8
        )


if __name__ == "__main__":
    from rag.data_loader import \
        load_sqldatabase_webpage_document, \
        load_sqldatabase_webpage_raft, \
        load_sqldatabase_book_document, \
        load_sqldatabase_book_raft
    vector_store = VectorStore()
    graph_store = GraphStore()
    inference = Inference(vector_store=VectorStore(), graph_store=GraphStore())
    temp_nodes = []
    for node in load_sqldatabase_webpage_document():
        temp_nodes.append(node)
        if len(temp_nodes) % 100 == 0:
            vector_store.add_nodes(temp_nodes)
            temp_nodes = []
            break
    vector_store.add_nodes(temp_nodes)
    temp_nodes = []
    for node in load_sqldatabase_webpage_raft():
        temp_nodes.append(node)
        if len(temp_nodes) % 100 == 0:
            vector_store.add_nodes(temp_nodes)
            temp_nodes = []
            break
    vector_store.add_nodes(temp_nodes)
    temp_nodes = []
    for node in load_sqldatabase_book_document():
        temp_nodes.append(node)
        if len(temp_nodes) % 100 == 0:
            vector_store.add_nodes(temp_nodes)
            temp_nodes = []
            break
    vector_store.add_nodes(temp_nodes)
    temp_nodes = []
    for node in load_sqldatabase_book_raft():
        temp_nodes.append(node)
        if len(temp_nodes) % 100 == 0:
            vector_store.add_nodes(temp_nodes)
            temp_nodes = []
            break
    vector_store.add_nodes(temp_nodes)
    nodes = vector_store.retrieve("\
        What is the role of polyamines in cell growth and proliferation, \
        and how does it differ from their role in ion channel regulation?"
    )
    print(nodes[0])
    print(response_synthesize("What is the role of polyamines in cell growth and proliferation, \
        and how does it differ from their role in ion channel regulation?", nodes))
    nodes = vector_store.retrieve("What is the role of polyamines in cell growth and proliferation?")
    print(nodes[0])
    print(response_synthesize("What is the role of polyamines in cell growth and proliferation?", nodes))