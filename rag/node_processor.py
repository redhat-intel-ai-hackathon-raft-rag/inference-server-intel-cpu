from llama_index.core.postprocessor import \
    SimilarityPostprocessor, KeywordNodePostprocessor
from llama_index.postprocessor.openvino_rerank import OpenVINORerank
from dev import device


sim_processor = SimilarityPostprocessor(similarity_cutoff=0.75)

keyword_postprocessor = KeywordNodePostprocessor(
    required_keywords=["word1", "word2"], exclude_keywords=["word3", "word4"]
)

reranker = OpenVINORerank(
    model_id_or_path="BAAI/bge-reranker-base", device=device)


if __name__ == "__main__":
    from llama_index.core.schema import TextNode
    nodes = [
        TextNode(
            id_="919ea626-2850-4bd9-824f-26689a0d164a",
            text="The author grew up in a large town."
        ),
        TextNode(
            id_="15d6ed4e-bc13-44eb-a1d3-d32baf56d70b",
            text="The author went to college in the city."
        )
    ]
    filtered_nodes = sim_processor.postprocess_nodes(nodes)
    print(filtered_nodes)
