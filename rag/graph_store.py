from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.indices.property_graph import PropertyGraphIndex
from llama_index.core import StorageContext

from rag.data_loader import load_json_nodes, load_raw_documents
from rag.response_synthesizer import response_synthesize


class GraphStore:
    graph_store = Neo4jPropertyGraphStore(
        username="neo4j",
        password="neo4jneo4j",
        url="bolt://localhost:7687",
    )
    index = PropertyGraphIndex.from_existing(
        graph_store,
    )

    def insert(self, document):
        self.index.insert(document)

    def load_raw_documents(self, input_dir: str):
        documents = load_raw_documents(input_dir)
        self.index = PropertyGraphIndex.from_documents(
            documents=documents,
            storage_context=StorageContext.from_defaults(
                graph_store=self.graph_store,
            )
        )

    def load_json_nodes(self, input_dir: str, text_field: str):
        nodes = load_json_nodes(input_dir, text_field)
        self.index = PropertyGraphIndex(
                nodes=nodes,
                storage_context=StorageContext.from_defaults(
                    vector_store=self.vector_store,
                )
            )

    def get_retriever(self, top_k=3):
        return self.index.as_retriever(
            similarity_top_k=top_k,
        )

    def retrieve(self, text: str, top_k=3):
        """
        retrieving nodes from vector store
        """
        retriver = self.get_retriever(top_k)
        return retriver.retrieve(text)

    def upsert_nodes(self, entities):
        """
        examples:
        entities = [
            EntityNode(
                name="llama", label="ANIMAL", properties={"key": "val"}),
            EntityNode(
                name="index", label="THING", properties={"key": "val"}),
        ]
        """
        self.graph_store.upsert_nodes(entities)

    def upsert_relations(self, relations):
        """
        examples:
        relations = [
            Relation(
                label="HAS",
                source_id=entities[0].id,
                target_id=entities[1].id,
                properties={},
            )
        ]
        """

        self.graph_store.upsert_relations(relations)

    def upsert_llama_nodes(self, source_chunks):
        """
        examples:
        source_chunk = TextNode(id_="source", text="My llama has an index.")
        """
        self.graph_store.upsert_llama_nodes(source_chunks)

    def get_node_by_ids(self, node_ids):
        return self.graph_store.get(ids=node_ids)

    def get_node_by_properties(self, properties: dict):
        """
        examples:
        properties = {"key": "value"}
        """
        return self.graph_store.get(properties=properties)

    def get_rel_map(self, entity_nodes: list):
        return self.graph_store.get_rel_map(entity_nodes)

    def get_llama_nodes(self, ids):
        return self.graph_store.get_llama_nodes(ids)

    def _delete_nodes_by_ids(self, node_ids):
        return self.graph_store.delete(node_ids)

    def _delete_nodes_by_properties(self, properties):
        return self.graph_store.delete(properties=properties)

    def _cipher_query(self, cipher_query):
        return self.graph_store.structured_query(cipher_query)


if __name__ == '__main__':
    from llama_index.core import Document
    graph_store = GraphStore()
    document = Document(
        text="The author grew up in a small town.",
    )
    graph_store.insert(document)
    document = Document(
        text="The author went to college in the city.",
    )
    graph_store.insert(document)
    nodes = graph_store.retrieve("Where did the author grow up?")
    print(nodes)
    print(response_synthesize("Where did the author grow up?", nodes))
