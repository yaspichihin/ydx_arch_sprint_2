#!/bin/bash
curl -X POST http://127.0.0.1:8082/api/events/movie \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "movie_id": 1,
  "title": "Inception",
  "action": "viewed",
  "user_id": 1,
  "rating": 8.5,
  "genres": ["Action", "Sci-Fi"],
  "description": "A mind-bending sci-fi thriller."
}
EOF