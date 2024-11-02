from datetime import datetime
import json
from typing import Any, Dict, Generator
from urllib.parse import urlparse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from rag.sql.schema import Webpage, WebpageLink
from rag.sql.engine import engine

# delete all rows

jsonl_file = 'dataset/dataset_web.jsonl'


def current_timestamp():
    return datetime.now().timestamp()


def load_dataset_web(path: str) -> Generator[Dict[str, Any], None, None]:
    with open(path, 'r') as f:
        for line in f:
            yield json.loads(line)


def insert_dataset_web(path: str) -> Generator[Dict[str, Any], None, None]:
    Session = sessionmaker(bind=engine)
    session = Session()
    web_dataset_loader = load_dataset_web(path)
    batch_size = 1000
    batch_webpages = []
    batch_webpage_links = []
    ids = []
    for item in web_dataset_loader:
        if item.get('url') in ids:
            continue
        ids.append(item.get('url'))
        url = item.get('url')
        text = item.get('text')
        links = item.get('links', [])
        parsed_url = urlparse(url)
        domain_parts = parsed_url.netloc.split('.')
        if len(domain_parts) >= 2:
            domain = '.'.join(domain_parts[-2:])
        else:
            domain = parsed_url.netloc
        try:
            title = item.get('title')
        except Exception:
            title = None
        webpage = Webpage(
            id=url,
            text=text,
            domain=domain,
            title=title,
            created_at=current_timestamp()
        )
        batch_webpages.append(webpage)
        if links is not None and len(links) > 0:
            for link in links:
                webpage_link = WebpageLink(
                    link=link,
                    webpage_id=webpage.id,
                    created_at=current_timestamp()
                )
                batch_webpage_links.append(webpage_link)

        def persist_batch(batch_webpages, batch_webpage_links):
            try:
                session.add_all(batch_webpages)
                session.flush()
                session.add_all(batch_webpage_links)
                session.commit()
                batch_webpages = []
                batch_webpage_links = []
            except IntegrityError:
                session.rollback()
                print("Failed to insert webpages")
                json_webpages = [
                    {
                        'id': webpage.id,
                        'text': webpage.text,
                        'domain': webpage.domain,
                        'title': webpage.title,
                        'created_at': webpage.created_at
                    }
                    for webpage in batch_webpages]
                json_webpage_links = [
                    {
                        'id': webpage_link.id,
                        'link': webpage_link.link,
                        'webpage_id': webpage_link.webpage_id,
                        'created_at': webpage_link.created_at
                    }
                    for webpage_link in batch_webpage_links]
                with open(f"dataset/insertion_failed/dataset_web/webpages/{current_timestamp()}.json", 'w') as f:
                    json.dump(json_webpages, f)
                with open(f"dataset/insertion_failed/dataset_web/webpage_links/{current_timestamp()}.json", 'w') as f:
                    json.dump(json_webpage_links, f)
        if len(batch_webpages) % batch_size == 0:
            persist_batch(batch_webpages, batch_webpage_links)
    persist_batch(batch_webpages, batch_webpage_links)


if __name__ == '__main__':
    insert_dataset_web(jsonl_file)
