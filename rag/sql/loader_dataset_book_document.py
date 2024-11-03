import os
import json
import uuid
from datetime import datetime
from typing import Any, Dict, Generator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from rag.sql.schema import Book, BookDocument, BookRaft
from rag.sql.engine import engine


Session = sessionmaker(bind=engine)
session = Session()

jsonl_file = 'dataset/dataset_book.jsonl'


def current_timestamp():
    return datetime.now().timestamp()


def load_dataset_book(path: str) -> Generator[Dict[str, Any], None, None]:
    with open(path, 'r') as f:
        for line in f:
            yield json.loads(line)


def persist_batch(batch_books_documents, batch_books_rafts):
    try:
        session.add_all(batch_books_documents)
        session.flush()
        session.add_all(batch_books_rafts)
        session.commit()
    except IntegrityError:
        session.rollback()
        print("Failed to insert books")
        json_books_documents = [
            {
                'id': book_doc.id,
                'text': book_doc.text,
                'book_id': book_doc.book_id,
                'created_at': book_doc.created_at
            }
            for book_doc in batch_books_documents]
        os.makedirs("dataset/insertion_failed/dataset_book/books_documents", exist_ok=True)
        with open(f"dataset/insertion_failed/dataset_book/books_documents/{current_timestamp()}.json", 'w') as f:
            json.dump(json_books_documents, f)
        json_books_rafts = [
            {
                'id': raft.id,
                'input': raft.input,
                'output': raft.output,
                'book_document_id': raft.book_document_id,
                'created_at': raft.created_at
            }
            for raft in batch_books_rafts]
        os.makedirs("dataset/insertion_failed/dataset_book/books_documents", exist_ok=True)
        with open(f"dataset/insertion_failed/dataset_book/books_rafts/{current_timestamp()}.json", 'w') as f:
            json.dump(json_books_rafts, f)
    finally:
        session.commit()


def insert_dataset_book_document(path: str) -> Generator[Dict[str, Any], None, None]:
    Session = sessionmaker(bind=engine)
    session = Session()
    book_dataset_loader = load_dataset_book(path)
    batch_size = 100
    batch_books_documents = []
    batch_books_rafts = []
    for item in book_dataset_loader:
        if item.get('title_and_authors') is None \
                or item.get('title_and_authors').get('title') is None \
                or item.get('raft') is None:
            continue
        try:
            title = item.get("title_and_authors").get("title")
            book = session.query(Book).filter(Book.id == title).first()
            if item.get("raft") is None:
                continue
            docs_texts = [doc for doc in set([doc.get("oracle_context") for doc in item.get("raft", [])])]
            for doc_text in docs_texts:
                if len(doc_text) < 100:
                    continue
                if doc_text is None or doc_text == "":
                    continue
                book_doc = BookDocument(
                    id=uuid.uuid4(),
                    text=doc_text.replace("\x00", ""),
                    book_id=book.id,
                    created_at=current_timestamp()
                )
                batch_books_documents.append(book_doc)
                for raft in item.get("raft"):
                    if raft.get("oracle_context") == doc_text:
                        if len(raft.get("input")) < 10 or len(raft.get("output")) < 10:
                            continue
                        raft = BookRaft(
                            id=uuid.uuid4(),
                            input=raft.get("input").replace("\x00", ""),
                            output=raft.get("output").replace("\x00", ""),
                            book_document_id=book_doc.id,
                            created_at=current_timestamp()
                        )
                        batch_books_rafts.append(raft)
            if len(batch_books_documents) % batch_size == 0:
                batch_books_documents = list(set(batch_books_documents))
                batch_books_rafts = list(set(batch_books_rafts))
                persist_batch(batch_books_documents, batch_books_rafts)
                batch_books_documents = []
                batch_books_rafts = []
        except Exception as e:
            # print line number
            print(e.__traceback__.tb_lineno)
            print(e)
    persist_batch(batch_books_documents, batch_books_rafts)
    print("Finished inserting books")


if __name__ == '__main__':
    insert_dataset_book_document(jsonl_file)
