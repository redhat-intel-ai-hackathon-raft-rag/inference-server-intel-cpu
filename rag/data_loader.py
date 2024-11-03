import json
import os
from typing import Generator, List
import uuid
from llama_index.core.schema import TextNode
from llama_index.core import SimpleDirectoryReader, Document
from rag.sql.schema import WebpageDocument, WebpageRaft, BookDocument, BookRaft
from sqlalchemy.orm import sessionmaker
from rag.sql.engine import engine

Session = sessionmaker(bind=engine)
session = Session()

def load_raw_documents(input_dir: str) -> List[Document]:
    reader = SimpleDirectoryReader(input_dir=input_dir)
    documents = reader.load_data()
    return documents


def load_json_nodes(
        input_dir: str,
        text_field: str) -> Generator[TextNode, None, None]:
    for file in os.listdir(input_dir):
        with open(os.path.join(input_dir, file), 'r') as f:
            data = json.load(f)
            id_ = uuid.uuid4()
            node = TextNode(
                id_=str(id_),
                text=data[text_field],
            )
            yield node


def load_sqldatabase_webpage_document() -> Generator[WebpageDocument, None, None]:
    webpage_documents = session.query(WebpageDocument).yield_per(100)
    for webpage_document in webpage_documents:
        node = TextNode(
            id_=str(webpage_document.id),
            text=webpage_document.text,
        )
        yield node


def load_sqldatabase_webpage_raft() -> Generator[WebpageRaft, None, None]:
    webpage_rafts = session.query(WebpageRaft).yield_per(100)
    for webpage_raft in webpage_rafts:
        node = TextNode(
            id_=str(webpage_raft.id),
            text=webpage_raft.input,
        )
        yield node


def load_sqldatabase_book_document() -> Generator[BookDocument, None, None]:
    book_documents = session.query(BookDocument).yield_per(100)
    for book_document in book_documents:
        node = TextNode(
            id_=str(book_document.id),
            text=book_document.text,
        )
        yield node


def load_sqldatabase_book_raft() -> Generator[BookRaft, None, None]:
    book_rafts = session.query(BookRaft).yield_per(100)
    for book_raft in book_rafts:
        node = TextNode(
            id_=str(book_raft.id),
            text=book_raft.input,
        )
        yield node


if __name__ == "__main__":
    for webpage_document in load_sqldatabase_webpage_document():
        print(webpage_document.text)
        break
    for webpage_raft in load_sqldatabase_webpage_raft():
        print(webpage_raft.text)
        break
    for book_document in load_sqldatabase_book_document():
        print(book_document.text)
        break
    for book_raft in load_sqldatabase_book_raft():
        print(book_raft.text)
        break
    print("Finished loading nodes")