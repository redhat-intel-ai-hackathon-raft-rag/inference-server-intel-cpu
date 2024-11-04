# fast output when user query similar to the RAFT training data
curl -N -X POST http://flask-app-route-eichi-uehara-2-dev.apps.cluster.intel.sandbox1234.opentlc.com/v1/chat/completions \
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

echo " "
echo "----------------------------------------------------------------------------------------------"

# showcase the ability of the LLM to generate answers finetuned with medical data and provided medical documents for RAG inference
curl -N -X POST http://flask-app-route-eichi-uehara-2-dev.apps.cluster.intel.sandbox1234.opentlc.com/v1/chat/completions \
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

echo " "
echo "----------------------------------------------------------------------------------------------"

# showcase the finetuned LLM's ability to answer questions that are not in the training data nor the dataset for RAG inference 1
# note: LLM is fine-tuned to answer with chain of thoughts
curl -N -X POST http://flask-app-route-eichi-uehara-2-dev.apps.cluster.intel.sandbox1234.opentlc.com/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
  "messages": [
    {
      "role": "system",
      "content": "Provide answer with references if available."
    },
    {
      "role": "user",
      "content": "What makes RedHat as Tier 1 enterprise solution vendors"
    }
  ]
}'

echo " "
echo "----------------------------------------------------------------------------------------------"

# showcase the ability to answer questions that are not in the training data nor the dataset for RAG inference 2
# note: LLM is fine-tuned to answer with chain of thoughts
curl -N -X POST http://flask-app-route-eichi-uehara-2-dev.apps.cluster.intel.sandbox1234.opentlc.com/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
  "messages": [
    {
      "role": "system",
      "content": "Provide answer with references if available."
    },
    {
      "role": "user",
      "content": "How did Robert Noyce affect the culture of Silicon valley?"
    }
  ]
}'
