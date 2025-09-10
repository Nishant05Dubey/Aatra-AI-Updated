#!/bin/bash

# Manual Setup Script for Aatra AI (No Docker Required)
# Perfect for live demos and development

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up Aatra AI - Manual Installation${NC}"
echo "=================================================="

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    echo "Please install Python 3.11+ and try again"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"

# Setup backend
echo -e "${BLUE}🔧 Setting up backend environment...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment and install dependencies
echo "Installing backend dependencies..."
source venv/bin/activate

# Install core dependencies first
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv pydantic-settings

echo -e "${GREEN}✅ Core backend dependencies installed${NC}"

# Setup environment file
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Environment file created${NC}"
fi

# Initialize database with demo data
echo -e "${BLUE}📊 Initializing database...${NC}"
python scripts/init_db.py

echo -e "${GREEN}✅ Database initialized with sample data${NC}"

# Return to main directory
cd ..

# Create simple start script
cat > start_demo_simple.sh << 'EOF'
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
EOF

chmod +x start_demo_simple.sh

# Create stop script
cat > stop_demo.sh << 'EOF'
#!/bin/bash

echo "🛑 Stopping Aatra AI Demo..."

# Kill all related processes
pkill -f "uvicorn app.main:app" 2>/dev/null || true
pkill -f "python3 -m http.server" 2>/dev/null || true
pkill -f "python -m http.server" 2>/dev/null || true

sleep 2

echo "✅ Demo servers stopped"
EOF

chmod +x stop_demo.sh

# Create quick test script
cat > test_demo.sh << 'EOF'
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
EOF

chmod +x test_demo.sh

echo ""
echo -e "${GREEN}🎉 Manual Setup Complete!${NC}"
echo "================================="
echo ""
echo -e "${YELLOW}Quick Start Commands:${NC}"
echo -e "  ${BLUE}./start_demo_simple.sh${NC}   # Start the demo (no Docker)"
echo -e "  ${BLUE}./test_demo.sh${NC}          # Test all components"
echo -e "  ${BLUE}./stop_demo.sh${NC}          # Stop all services"
echo ""
echo -e "${YELLOW}Demo URLs:${NC}"
echo -e "  🌐 Frontend:       http://localhost:3000"
echo -e "  🔧 Backend API:    http://localhost:8000"
echo -e "  📚 API Docs:       http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Live Demo Commands:${NC}"
echo -e "  ${BLUE}curl -X POST http://localhost:8000/api/demo/simulate-detection${NC}"
echo -e "  ${BLUE}curl -X POST http://localhost:8000/api/demo/generate-live-threats?count=3${NC}"
echo ""
echo -e "${GREEN}✅ Ready for live demo presentation!${NC}"
echo ""