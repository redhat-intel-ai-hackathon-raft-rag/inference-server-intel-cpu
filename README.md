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

setup kubernetes cluster by referencing, then port-forward to local

https://github.com/redhat-intel-ai-hackathon-raft-rag/infra

both approach takes with 10 minutes

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
python -m rag.load_data2index
```

## Run application

```bash
python -m app
```

```bash
curl -X POST http://localhost:5000/v1/chat/completions \
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
