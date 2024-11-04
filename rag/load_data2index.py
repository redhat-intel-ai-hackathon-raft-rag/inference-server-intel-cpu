from rag.vector_store import VectorStore
from rag.data_loader import \
    load_sqldatabase_webpage_document, \
    load_sqldatabase_webpage_raft, \
    load_sqldatabase_book_document, \
    load_sqldatabase_book_raft


def load_data2index():
    vector_store = VectorStore(collection_name="webpage_document")
    temp_nodes = []
    for node in load_sqldatabase_webpage_document():
        temp_nodes.append(node)
        if len(temp_nodes) % 10000 == 0:
            vector_store.add_nodes(temp_nodes)
            temp_nodes = []
    vector_store.add_nodes(temp_nodes)
    vector_store = VectorStore(collection_name="webpage_raft")
    temp_nodes = []
    for node in load_sqldatabase_webpage_raft():
        temp_nodes.append(node)
        if len(temp_nodes) % 10000 == 0:
            vector_store.add_nodes(temp_nodes)
            temp_nodes = []
    vector_store.add_nodes(temp_nodes)
    vector_store = VectorStore(collection_name="book_document")
    temp_nodes = []
    for node in load_sqldatabase_book_document():
        temp_nodes.append(node)
        if len(temp_nodes) % 10000 == 0:
            vector_store.add_nodes(temp_nodes)
            temp_nodes = []
    vector_store.add_nodes(temp_nodes)
    vector_store = VectorStore(collection_name="book_raft")
    temp_nodes = []
    for node in load_sqldatabase_book_raft():
        temp_nodes.append(node)
        if len(temp_nodes) % 10000 == 0:
            vector_store.add_nodes(temp_nodes)
            temp_nodes = []
    vector_store.add_nodes(temp_nodes)


if __name__ == "__main__":
    load_data2index()
    vector_store = VectorStore(collection_name="webpage_document")
    nodes = vector_store.retrieve("What is the role of polyamines in cell growth and proliferation?")
    print(nodes[0])
    vector_store = VectorStore(collection_name="webpage_raft")
    nodes = vector_store.retrieve("What is the role of polyamines in cell growth and proliferation?")
    print(nodes[0])
    vector_store = VectorStore(collection_name="book_document")
    nodes = vector_store.retrieve("What is the role of polyamines in cell growth and proliferation?")
    print(nodes[0])
    vector_store = VectorStore(collection_name="book_raft")
    nodes = vector_store.retrieve("What is the role of polyamines in cell growth and proliferation?")
    print(nodes[0])
    # print(response_synthesize("What is the role of polyamines in cell growth and proliferation, \
    #     and how does it differ from their role in ion channel regulation?", nodes))
    # nodes = vector_store.retrieve("What is the role of polyamines in cell growth and proliferation?")
    # print(nodes[0])
    # print(response_synthesize("What is the role of polyamines in cell growth and proliferation?", nodes))