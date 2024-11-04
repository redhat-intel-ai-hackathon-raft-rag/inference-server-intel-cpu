from qdrant_client import QdrantClient, models
from rag.response_synthesizer import response_synthesize
from rag.vector_store import VectorStore
from rag.data_loader import load_sqldatabase_book_raft


client = QdrantClient(url="http://localhost:6333")
collection_name = "book_raft"


def load_data2index():
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=384,
            distance=models.Distance.COSINE,
            on_disk=True),
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                always_ram=True,
            )
        ),
        optimizers_config=models.OptimizersConfigDiff(
            indexing_threshold=0,
        ),
    )
    vector_store = VectorStore(collection_name=collection_name)
    temp_nodes = []
    for node in load_sqldatabase_book_raft():
        temp_nodes.append(node)
        if len(temp_nodes) % 10000 == 0:
            vector_store.add_nodes(temp_nodes)
            temp_nodes = []
    vector_store.add_nodes(temp_nodes)
    client.update_collection(
        collection_name=collection_name,
        optimizer_config=models.OptimizersConfigDiff(indexing_threshold=20000),
    )


if __name__ == "__main__":
    load_data2index()
    vector_store = VectorStore(collection_name=collection_name)
    nodes = vector_store.retrieve("What is the role of polyamines in cell growth and proliferation?")
    print(nodes[0])
    print(response_synthesize("What is the role of polyamines in cell growth and proliferation, \
        and how does it differ from their role in ion channel regulation?", nodes))
    nodes = vector_store.retrieve("What is the role of polyamines in cell growth and proliferation?")
    print(nodes[0])
    print(response_synthesize("What is the role of polyamines in cell growth and proliferation?", nodes))