from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core import get_response_synthesizer
from llm_models import llm

response_synthesizer = get_response_synthesizer(
    response_mode=ResponseMode.COMPACT,
    llm=llm
)

stream_response_synthesizer = get_response_synthesizer(
    response_mode=ResponseMode.COMPACT,
    llm=llm,
    streaming=True
)


def response_synthesize(text, nodes, streaming=False):
    """
    given a text and retrieved nodes, synthesize a response with LLM
    text: user query
    nodes: retrieved nodes from component of retriever
    llm: global setting with llmma index Setting module
    """
    if streaming:
        return stream_response_synthesizer.synthesize(text, nodes)
    return response_synthesizer.synthesize(text, nodes)


if __name__ == '__main__':
    from rag.vector_store import VectorStore
    from llama_index.core.schema import TextNode
    vector_store = VectorStore([
        TextNode(
            id_="919ea626-2850-4bd9-824f-26689a0d164a",
            text="The author grew up in a large town."
        ),
        TextNode(
            id_="15d6ed4e-bc13-44eb-a1d3-d32baf56d70b",
            text="The author went to college in the city."
        ),
    ])
    nodes = vector_store.retrieve("Where did the author grow up?")
    print(response_synthesize("Where did the author grow up?", nodes))
