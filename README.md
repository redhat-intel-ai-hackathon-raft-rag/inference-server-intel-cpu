```bash
python -m venv .venv &&
source .venv/bin/activate &&
pip install -r requirement.txt
```

## setup quantized OpenVEVO format model

./scripts/download_model.sh &&

## setup infra

setup local postgres, qdrant, neo4j(optional)

or

setup kubernetes cluster then port-forward to local by referencing below

https://github.com/redhat-intel-ai-hackathon-raft-rag/infra

both approaches take within 10 minutes

## setup .env

enter the variables according to the infra

## setup SQL database

```bash
python -m rag.sql.loader_dataset_web
python -m rag.sql.loader_dataset_web_document
python -m rag.sql.loader_dataset_book
python -m rag.sql.loader_dataset_book_document
```

## setup Vector database

```bash
python -m rag.sql.load_data2index_book_document
python -m rag.sql.load_data2index_book_raft
python -m rag.sql.load_data2index_webpage_document
python -m rag.sql.load_data2index_webpage_raft
```

## Run application

```bash
python -m app
```

```bash
curl -N -X POST http://localhost:5000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
  "messages": [
    {
      "role": "system",
      "content": "Provide answer with references if available."
    },
    {
      "role": "user",
      "content": "What is the role of polyamines in cell growth and proliferation?"
    }
  ]
}'
```

```bash
curl -N -X POST http://localhost:5000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
  "messages": [
    {
      "role": "system",
      "content": "Provide answer with references if available."
    },
    {
      "role": "user",
      "content": "How to understand the role of the polyamines"
    }
  ]
}'
```
