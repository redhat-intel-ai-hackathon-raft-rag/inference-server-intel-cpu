import json
import os
from typing import Generator, List
import uuid
from llama_cloud import TextNode
from llama_index.core import SimpleDirectoryReader, Document


def load_raw_documents(input_dir: str) -> List[Document]:
    reader = SimpleDirectoryReader(input_dir=input_dir)
    documents = reader.load_data()
    return documents


def load_json_nodes(
        input_dir: str,
        text_field: str) -> Generator[TextNode]:
    for file in os.listdir(input_dir):
        with open(os.path.join(input_dir, file), 'r') as f:
            data = json.load(f)
            id_ = uuid.uuid4()
            node = TextNode(
                id_=str(id_),
                text=data[text_field],
            )
            yield node
