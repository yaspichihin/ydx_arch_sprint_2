for ((i=0; i<=1000; i++)); do
  curl http://localhost:8000/api/movies | jq .
done