import os
from datetime import datetime
import json
from typing import Any, Dict, Generator
import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from rag.sql.schema import Webpage, WebpageDocument, WebpageRaft
from rag.sql.engine import engine


Session = sessionmaker(bind=engine)
session = Session()

jsonl_file = 'dataset/dataset_web.jsonl'


def current_timestamp():
    return datetime.now().timestamp()


def load_dataset_webpage(path: str) -> Generator[Dict[str, Any], None, None]:
    with open(path, 'r') as f:
        for line in f:
            yield json.loads(line)


def persist_batch(batch_webpages_documents, batch_webpages_rafts):
    try:
        session.add_all(batch_webpages_documents)
        session.flush()
        session.add_all(batch_webpages_rafts)
        session.commit()
        batch_webpages_documents = []
        batch_webpages_rafts = []
    except IntegrityError:
        session.rollback()
        session.commit()
        print("Failed to insert webpages")
        json_webpages_documents = [
            {
                'id': webpage_doc.id,
                'text': webpage_doc.text,
                'webpage_id': webpage_doc.webpage_id,
                'created_at': webpage_doc.created_at
            }
            for webpage_doc in batch_webpages_documents]
        with open(f"dataset/insertion_failed/dataset_webpage/webpages_documents/{current_timestamp()}.json", 'w') as f:
            json.dump(json_webpages_documents, f)
        json_webpages_rafts = [
            {
                'id': raft.id,
                'input': raft.input,
                'output': raft.output,
                'webpage_document_id': raft.webpage_document_id,
                'created_at': raft.created_at
            }
            for raft in batch_webpages_rafts]
        with open(f"dataset/insertion_failed/dataset_webpage/webpages_rafts/{current_timestamp()}.json", 'w') as f:
            json.dump(json_webpages_rafts, f)


def insert_dataset_webpage_document(path: str) -> Generator[Dict[str, Any], None, None]:
    Session = sessionmaker(bind=engine)
    session = Session()
    webpage_dataset_loader = load_dataset_webpage(path)
    batch_size = 100
    batch_webpages_documents = []
    batch_webpages_rafts = []
    for item in webpage_dataset_loader:
        if item.get('url') is None \
                or item.get('raft') is None:
            continue
        try:
            url = item.get('url')
            webpage = session.query(Webpage).filter(Webpage.id == url).first()
            if webpage is None:
                print(f"webpage with url {url} not found")
                continue
            if item.get("raft") is None:
                continue
            docs_texts = [doc for doc in set([doc.get("oracle_context") for doc in item.get("raft", [])])]
            for doc_text in docs_texts:
                if doc_text is None or doc_text == "":
                    continue
                webpage_doc = WebpageDocument(
                    id=uuid.uuid4().hex,
                    text=doc_text.replace("\x00", ""),
                    webpage_id=webpage.id,
                    created_at=current_timestamp()
                )
                batch_webpages_documents.append(webpage_doc)
                for raft in item.get("raft"):
                    if raft.get("oracle_context") == doc_text:
                        raft = WebpageRaft(
                            id=uuid.uuid4().hex,
                            input=raft.get("input").replace("\x00", ""),
                            output=raft.get("output").replace("\x00", ""),
                            webpage_document_id=webpage_doc.id,
                            created_at=current_timestamp()
                        )
                        batch_webpages_rafts.append(raft)
            if len(batch_webpages_documents) % batch_size == 0:
                persist_batch(batch_webpages_documents, batch_webpages_rafts)
                batch_webpages_documents = []
                batch_webpages_rafts = []
        except Exception as e:
            print(e.__traceback__.tb_lineno)
            print(e)
    persist_batch(batch_webpages_documents, batch_webpages_rafts)
    print("Finished inserting webpages")


if __name__ == '__main__':
    insert_dataset_webpage_document(jsonl_file)
