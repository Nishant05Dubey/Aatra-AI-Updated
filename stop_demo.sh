#!/bin/bash

echo "🛑 Stopping Aatra AI Demo..."

# Kill all related processes
pkill -f "uvicorn app.main:app" 2>/dev/null || true
pkill -f "python3 -m http.server" 2>/dev/null || true
pkill -f "python -m http.server" 2>/dev/null || true

sleep 2

echo "✅ Demo servers stopped"
