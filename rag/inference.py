import uuid
from llama_index.core.settings import Settings
from llama_index.core.schema import NodeWithScore, TextNode
# from llm_config import SUPPORTED_LLM_MODELS
from embedding import embedding
from llm_models import llm
from rag.response_synthesizer import response_synthesize


class Inference:
    def __init__(self, vector_store, graph_store, node_processors=None):
        Settings.embed_model = embedding
        Settings.llm = llm
        self.node_processors = node_processors
        self.vector_store = vector_store
        self.graph_store = graph_store
        # llm_model_configuration = \
        #   SUPPORTED_LLM_MODELS['English']['qwen2.5-1.5b-instruct']
        # llm.max_new_tokens = 2048
        # stop_tokens = llm_model_configuration.get("stop_tokens")
        # if stop_tokens is not None:
        #     llm._stopping_criteria = StoppingCriteriaList(stop_tokens)

    def get_response(self, query, context, top_k=3):
        nodes = []
        nodes.append(self.get_node_from_context(context))
        # retrieve nodes
        nodes.extend(self.vector_store.retrieve(context))
        nodes.extend(self.graph_store.retrieve(context))
        nodes.extend(self.vector_store.retrieve(query))
        nodes.extend(self.graph_store.retrieve(query))
        # node post processing
        for processor in self.node_processors:
            nodes = processor.postprocess_nodes(nodes)
        # response synthesis
        return response_synthesize(query, nodes)

    def get_node_from_context(self, context):
        text_Node = TextNode(
            id_=str(uuid.uuid4()),
            text=context
        )
        return NodeWithScore(
            node=text_Node,
            score=1.0
        )


if __name__ == "__main__":
    nodewithscore = NodeWithScore(
        node=TextNode(
            id_=str(uuid.uuid4()),
            text="The author worked at a local restaurant."
        ),
        score=1.0
    )
    print(nodewithscore)
