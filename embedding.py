from llama_index.embeddings.huggingface_openvino import OpenVINOEmbedding
from dev import device

embedding = OpenVINOEmbedding(
    model_id_or_path="BAAI/bge-small-en-v1.5",
    embed_batch_size=4,
    device=device,
    model_kwargs={"compile": False}
)
embedding._model.compile()
