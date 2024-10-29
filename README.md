python -m venv .venv &&
source .venv/bin/activate &&
pip install -r requirement.txt &&
./scripts/download_model.sh &&
python app.py

```
curl -X POST http://localhost:5000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
  "messages": [
    {
      "role": "system",
      "content": "The meaning of life is to be happy."
    },
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
}'
```
