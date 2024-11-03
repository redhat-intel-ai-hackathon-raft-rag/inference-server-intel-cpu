import os
import json
import uuid
from datetime import datetime
from typing import Any, Dict, Generator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from rag.sql.schema import Book, BookCite
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


def persist_batch(batch_books, batch_books_cites):
    try:
        session.add_all(batch_books)
        session.flush()
        session.add_all(batch_books_cites)
    except Exception:
        session.rollback()
        print("Failed to insert books")
        json_books = [
            {
                'id': book.id,
                'authors': book.authors,
                'created_at': book.created_at
            }
            for book in batch_books]
        json_books_cites = [
            {
                'id': book_cite.id,
                'cited_book_title': book_cite.cited_book_title,
                'cited_book_authors': book_cite.cited_book_authors,
                'book_id': book_cite.book_id,
            }
            for book_cite in batch_books_cites]
        os.makedirs("dataset/insertion_failed/dataset_book/books", exist_ok=True)
        with open(f"dataset/insertion_failed/dataset_book/books/{current_timestamp()}.json", 'w') as f:
            json.dump(json_books, f)
        os.makedirs("dataset/insertion_failed/dataset_book/books_cites", exist_ok=True)
        with open(f"dataset/insertion_failed/dataset_book/books_cites/{current_timestamp()}.json", 'w') as f:
            json.dump(json_books_cites, f)
    finally:
        session.commit()


def insert_dataset_book(path: str) -> Generator[Dict[str, Any], None, None]:
    book_dataset_loader = load_dataset_book(path)
    batch_size = 1
    batch_books = []
    batch_books_cites = []
    # batch_books_documents = []
    for item in book_dataset_loader:
        if item.get('title_and_authors') is None \
                or item.get('title_and_authors').get('title') is None \
                or item.get('raft') is None:
            continue
        try:
            title = item.get("title_and_authors").get("title")
            cites = item.get("references", [])
            authors = item.get("title_and_authors").get("author_names", None)
            if isinstance(authors, str) is True:
                authors = [authors]
            if authors is not None and len(authors) > 0:
                authors = [author for author in authors if isinstance(author, str) is True and len(author) > 2]
                # authors += "|".join(authors)
            book = Book(
                id=title,
                authors=authors,
                created_at=current_timestamp()
            )
            batch_books.append(book)
            for cite in cites:
                if isinstance(cite, dict) is False \
                   or cite.get("title") is None or cite.get("title") == "":
                    continue
                cite_authors = cite.get("authors", None)
                if isinstance(cite_authors, str) is True:
                    cite_authors = [cite_authors]
                if cite_authors is not None and len(cite_authors) > 0:
                    cite_authors = [author for author in cite_authors if isinstance(author, str) is True and len(author) > 2]
                    # cite_authors += "|".join(cite_authors)
                book_cite = BookCite(
                    id=uuid.uuid4().hex,
                    cited_book_title=cite.get("title"),
                    cited_book_authors=cite_authors,
                    created_at=current_timestamp(),
                    book_id=title
                )
                batch_books_cites.append(book_cite)
        except Exception as e:
            print(e.__traceback__.tb_lineno)
            print(e)
        if len(batch_books) % batch_size == 0:
            batch_books = list(set(batch_books))
            batch_books_cites = list(set(batch_books_cites))
            persist_batch(batch_books, batch_books_cites)
            batch_books = []
            batch_books_cites = []
    persist_batch(batch_books, batch_books_cites)


if __name__ == '__main__':
    insert_dataset_book(jsonl_file)
