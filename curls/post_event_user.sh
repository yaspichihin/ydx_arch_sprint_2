#!/bin/bash
curl -X POST http://127.0.0.1:8082/api/events/user \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "user_id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "action": "registered",
  "timestamp": "2023-01-15T14:30:00Z"
}
EOF