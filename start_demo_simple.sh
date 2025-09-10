#!/bin/bash

echo "🚀 Starting Aatra AI Demo (Manual Setup)..."
echo "============================================="

# Kill any existing processes
pkill -f "uvicorn app.main:app" 2>/dev/null || true
pkill -f "python -m http.server" 2>/dev/null || true

# Wait for processes to stop
sleep 2

# Start backend
echo "🔧 Starting backend server..."
cd backend
source venv/bin/activate

# Start backend in background
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Backend starting with PID: $BACKEND_PID"

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 8

# Check if backend is running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend server started successfully"
else
    echo "❌ Backend server failed to start"
    echo "Checking what went wrong..."
    
    # Try to start in foreground to see errors
    echo "🔍 Starting backend in foreground for debugging..."
    kill $BACKEND_PID 2>/dev/null || true
    sleep 2
    
    echo "🔧 Attempting to start backend with debug info..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    sleep 5
    
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend started successfully on retry"
    else
        echo "❌ Backend still not responding. Please check logs above."
        echo "💡 Try running manually: cd backend && source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000"
        exit 1
    fi
fi

cd ..

# Start frontend
echo "🌐 Starting frontend server..."
python3 -m http.server 3000 &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 3

echo ""
echo "🎉 Demo is ready!"
echo "=================="
echo ""
echo "🌐 Frontend Demo:     http://localhost:3000"
echo "🔧 Backend API:       http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🏥 Health Check:      http://localhost:8000/health"
echo ""
echo "🎬 Demo Tips:"
echo "- Press Ctrl+C to stop the demo"
echo "- Use 'curl -X POST http://localhost:8000/api/demo/simulate-detection' for live threats"
echo "- Open browser dev tools and use quickDemo('critical') for instant testing"
echo ""
echo "Press Ctrl+C to stop the demo"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping demo servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    pkill -f "uvicorn app.main:app" 2>/dev/null || true
    pkill -f "python3 -m http.server" 2>/dev/null || true
    echo "👋 Demo stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Keep script running
wait
