#!/bin/bash
curl -X POST http://cinemaabyss.example.com/api/events/payment \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "payment_id": 1,
  "user_id": 1,
  "amount": 9.99,
  "status": "completed",
  "timestamp": "2023-01-15T14:30:00Z",
  "method_type": "credit_card"
}
EOF