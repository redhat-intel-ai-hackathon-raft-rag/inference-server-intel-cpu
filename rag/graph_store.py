from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.indices.property_graph import PropertyGraphIndex
from llama_index.core import StorageContext
from rag.response_synthesizer import response_synthesize
from llama_index.core.schema import TextNode
from llm_models import llm
from embedding import embedding


class GraphStore:
    graph_store = Neo4jPropertyGraphStore(
        username="neo4j",
        password="neo4jneo4j",
        url="bolt://localhost:7687",
    )
    index = PropertyGraphIndex.from_existing(
        graph_store,
        llm=llm,
        embed_model=embedding,
    )

    def add_nodes(self, nodes):
        if self.index is None:
            self.index = PropertyGraphIndex(
                nodes=nodes,
                storage_context=StorageContext.from_defaults(
                    graph_store=self.graph_store,
                ),
                llm=llm,
                embed_model=embedding
            )
        else:
            self.index.insert_nodes(nodes)

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

    def _delete_nodes_by_ids(self, node_ids):
        return self.graph_store.delete(node_ids)

    def _delete_nodes_by_properties(self, properties):
        return self.graph_store.delete(properties=properties)

    def _cipher_query(self, cipher_query):
        return self.graph_store.structured_query(cipher_query)


if __name__ == '__main__':
    from llama_index.core.settings import Settings
    from llama_index.core.schema import TextNode
    from llm_models import llm
    from embedding import embedding
    Settings.embed_model = embedding
    Settings.llm = llm
    graph_store = GraphStore()
    text_nodes = TextNode(
        id_="919ea626-2850-4bd9-824f-26689a0d164a",
        text="The author grew up in a large town.",
    )
    graph_store.add_nodes([text_nodes])
    text_nodes = TextNode(
        id_="15d6ed4e-bc13-44eb-a1d3-d32baf56d70b",
        text="The author went to college in the city.",
    )
    graph_store.add_nodes([text_nodes])
    nodes = graph_store.retrieve("Where did the author grow up?")
    print(nodes)
    print(response_synthesize("Where did the author grow up?", nodes))
