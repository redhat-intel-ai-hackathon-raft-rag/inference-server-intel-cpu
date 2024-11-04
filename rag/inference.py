from typing import List
import uuid
from llama_index.core.settings import Settings
from llama_index.core.schema import NodeWithScore, TextNode
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from embedding import embedding
from llm_models import llm
from rag.graph_store import GraphStore
from rag.response_synthesizer import response_synthesize
from rag.vector_store import VectorStore
# from llm_config import SUPPORTED_LLM_MODELS
from sqlalchemy.orm import sessionmaker
from rag.sql.engine import engine
from rag.sql.schema import WebpageRaft, BookRaft, WebpageDocument, BookDocument
from dotenv import load_dotenv

load_dotenv()
Session = sessionmaker(bind=engine)
session = Session()

COLLECTION_SCHEMA_MAP = {
    "webpage_raft": WebpageRaft,
    "book_raft": BookRaft,
    "webpage_document": WebpageDocument,
    "book_document": BookDocument
}


class Inference:
    def __init__(self,
                 vector_stores: List[VectorStore],
                 graph_stores: List[GraphStore] = [],
                 node_processors: List[BaseNodePostprocessor] = []):
        Settings.embed_model = embedding
        Settings.llm = llm
        self.raft_vector_stores = [
            vector_store for vector_store in vector_stores
            if "raft" in vector_store.vector_store.collection_name.lower()
        ]
        self.vector_stores = [
            vector_store for vector_store in vector_stores
            if vector_store.index is not None and
            vector_store not in self.raft_vector_stores
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
        for raft_vector_store in self.raft_vector_stores:
            nodes.extend(
                self.handle_raft_query(
                    raft_vector_store.retrieve(query, top_k),
                    raft_vector_store.vector_store.collection_name
                )
            )
        if self.has_significant_similar_query(nodes):
            return self.generate_response_with_raft(nodes)
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
        return {
            "response": response_synthesize(query, nodes, streaming=True),
            "streaming": True
        }

    def get_node_from_context(self, context):
        text_Node = TextNode(
            id_=str(uuid.uuid4()),
            text=context
        )
        return NodeWithScore(
            node=text_Node,
            score=0.8
        )

    def handle_raft_query(self, nodes: List[NodeWithScore], collection_name):
        items = session.query(
            COLLECTION_SCHEMA_MAP[collection_name].id,
            COLLECTION_SCHEMA_MAP[collection_name].output
        ).filter(
            COLLECTION_SCHEMA_MAP[collection_name].id.in_(
                [node.node.id_ for node in nodes]
            )
        ).all()
        # print(nodes)
        # updated_nodes = []
        for node in nodes:
            for item in items:
                if str(item.id) == str(node.node.id_):
                    # updated_nodes.append(
                    #     NodeWithScore(
                    #         node=TextNode(id_=node.node.id_, text=item.output),
                    #         score=node.score
                    #     )
                    # )
                    node.node.text = item.output
        print(nodes)
        # print(updated_nodes)
        return nodes

    def has_significant_similar_query(self, nodes: List[NodeWithScore]):
        return any(
            node.score > 0.90
            for node in nodes
        )

    def generate_response_with_raft(self, nodes: List[NodeWithScore]):
        # pick the node with the highest score
        nodes.sort(key=lambda x: x.score, reverse=True)
        return {
            "response": nodes[0].node.text,
            "streaming": False
        }
        # return nodes[0].node.text


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