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

echo "-----------------------------------------------------------------------------------------------------------------"

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

echo "-----------------------------------------------------------------------------------------------------------------"

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
      "content": "What makes RedHat and Microsoft as Tier 1 enterprise solution vendors"
    }
  ]
}'

echo "-----------------------------------------------------------------------------------------------------------------"

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
      "content": "Did Robert Noyce create the culture of Silicon valley?"
    }
  ]
}'
