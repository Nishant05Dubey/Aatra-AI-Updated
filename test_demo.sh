#!/bin/bash

echo "🧪 Testing Aatra AI Demo..."

echo "1. Testing backend health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
    curl http://localhost:8000/health | python3 -m json.tool
else
    echo "❌ Backend is not responding"
    exit 1
fi

echo ""
echo "2. Testing dashboard stats..."
if curl -f http://localhost:8000/api/dashboard/stats > /dev/null 2>&1; then
    echo "✅ Dashboard API working"
    curl http://localhost:8000/api/dashboard/stats | python3 -m json.tool
else
    echo "❌ Dashboard API not working"
fi

echo ""
echo "3. Testing content analysis..."
curl -X POST http://localhost:8000/api/analysis/content \
  -H "Content-Type: application/json" \
  -d '{"content": "I hate India and want to destroy it", "platform": "test"}' \
  | python3 -m json.tool

echo ""
echo "4. Testing frontend..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend is not accessible"
fi

echo ""
echo "🎉 Demo test complete!"
