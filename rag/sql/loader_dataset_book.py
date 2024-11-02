from datetime import datetime
import json
from typing import Any, Dict, Generator
import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from rag.sql.schema import Book, BookCite, BookDocument
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


def insert_dataset_book(path: str) -> Generator[Dict[str, Any], None, None]:
    Session = sessionmaker(bind=engine)
    session = Session()
    book_dataset_loader = load_dataset_book(path)
    batch_size = 100
    batch_books = []
    batch_books_cites = []
    batch_books_documents = []
    for item in book_dataset_loader:
        if item.get('title_and_authors') is None \
                or item.get('title_and_authors').get('title') is None \
                or item.get('raft') is None:
            continue
        try:
            title = item.get("title_and_authors").get("title")
            cites = item.get("references", [])
            book = Book(
                id=uuid.uuid4(),
                title=title,
                created_at=current_timestamp()
            )
            batch_books.append(book)
            for cite in cites:
                if isinstance(cite, dict) is False \
                   or cite.get("title") is None or cite.get("title") == "":
                    continue
                # remove NUL (0x00) characters
                book_cited = Book(
                    id=uuid.uuid4(),
                    title=cite.get("title").replace("\x00", ""),
                    created_at=current_timestamp()
                )
                book_cite = BookCite(
                    book_id=book.id,
                    cited_book_id=book_cited.id,
                    created_at=current_timestamp()
                )
                batch_books.append(book_cited)
                batch_books_cites.append(book_cite)
            if item.get("raft") is None:
                continue
            docs_texts = [doc for doc in set([doc.get("oracle_input") for doc in item.get("raft", [])])]
            for doc_text in docs_texts:
                if doc_text is None or doc_text == "":
                    continue
                book_doc = BookDocument(
                    id=uuid.uuid4(),
                    text=doc_text.replace("\x00", ""),
                    book_id=book.id,
                    created_at=current_timestamp()
                )
                batch_books_documents.append(book_doc)
        except Exception as e:
            # print line number
            print(e.__traceback__.tb_lineno)
            print(e)

        def persist_batch(batch_books, batch_books_cites, batch_books_documents):
            try:
                session.add_all(batch_books)
                session.flush()
                session.add_all(batch_books_cites)
                session.add_all(batch_books_documents)
                session.commit()
                batch_books = []
                batch_books_cites = []
                batch_books_documents = []
            except IntegrityError:
                session.rollback()
                print("Failed to insert books")
                json_books = [
                    {
                        'id': book.id,
                        'title': book.title,
                        'created_at': book.created_at
                    }
                    for book in batch_books]
                json_books_cites = [
                    {
                        'book_id': book_cite.book_id,
                        'cited_book_id': book_cite.cited_book_id,
                        'created_at': book_cite.created_at
                    }
                    for book_cite in batch_books_cites]
                json_books_documents = [
                    {
                        'id': book_doc.id,
                        'text': book_doc.text,
                        'book_id': book_doc.book_id,
                        'created_at': book_doc.created_at
                    }
                    for book_doc in batch_books_documents]
                with open(f"dataset/insertion_failed/dataset_book/books/{current_timestamp()}.json", 'w') as f:
                    json.dump(json_books, f)
                with open(f"dataset/insertion_failed/dataset_book/books_cites/{current_timestamp()}.json", 'w') as f:
                    json.dump(json_books_cites, f)
                with open(f"dataset/insertion_failed/dataset_book/books_documents/{current_timestamp()}.json", 'w') as f:
                    json.dump(json_books_documents, f)
        if len(batch_books) % batch_size == 0:
            persist_batch(batch_books, batch_books_cites, batch_books_documents)
    persist_batch(batch_books, batch_books_cites, batch_books_documents)

if __name__ == '__main__':
    insert_dataset_book(jsonl_file)