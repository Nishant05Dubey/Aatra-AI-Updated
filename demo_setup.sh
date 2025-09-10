#!/bin/bash

# Aatra AI Live Demo Setup Script
# This script prepares a complete live demonstration environment

set -e

echo "🎬 Setting up Aatra AI Live Demo Environment"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

if ! command -v curl &> /dev/null; then
    echo -e "${RED}❌ curl is required but not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Setup backend environment
echo -e "${BLUE}🔧 Setting up backend environment...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -q fastapi uvicorn sqlalchemy pydantic python-dotenv pydantic-settings

echo -e "${GREEN}✅ Backend dependencies installed${NC}"

# Setup environment file
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Environment file created${NC}"
fi

# Initialize database with demo data
echo -e "${BLUE}📊 Initializing demo database...${NC}"
python scripts/init_db.py

echo -e "${GREEN}✅ Demo database initialized${NC}"

# Add enhanced demo data
echo -e "${BLUE}🎭 Adding enhanced demo scenarios...${NC}"
python scripts/add_demo_scenarios.py

# Return to main directory
cd ..

# Create demo launcher script
cat > start_demo.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting Aatra AI Live Demo..."
echo "================================="

# Kill any existing processes
pkill -f "uvicorn app.main:app" || true
pkill -f "python -m http.server" || true

# Wait for processes to stop
sleep 2

# Start backend
echo "🔧 Starting backend server..."
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Check if backend is running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend server started successfully"
else
    echo "❌ Backend server failed to start"
    exit 1
fi

cd ..

# Start frontend
echo "🌐 Starting frontend server..."
python -m http.server 3000 &
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
echo "Press Ctrl+C to stop the demo"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping demo servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    pkill -f "uvicorn app.main:app" || true
    pkill -f "python -m http.server" || true
    echo "👋 Demo stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Keep script running
wait
EOF

chmod +x start_demo.sh

# Create demo data script
cat > backend/scripts/add_demo_scenarios.py << 'EOF'
#!/usr/bin/env python3
"""
Add enhanced demo scenarios for live presentation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.database import SessionLocal, engine
from app.models import ThreatDetection, SystemStats, PlatformAnalytics

def add_demo_scenarios():
    """Add realistic demo scenarios for live presentation"""
    print("🎭 Adding enhanced demo scenarios...")
    
    db = SessionLocal()
    try:
        # Enhanced threat scenarios for live demo
        demo_threats = [
            {
                "title": "🚨 LIVE: Coordinated Bot Network Attacking Indian Elections",
                "content": "Massive coordinated attack detected: 'Indian elections are fake and fraudulent, democracy is a lie in India, boycott voting'",
                "platform": "Twitter",
                "region": "Delhi",
                "confidence": 96.8,
                "threat_type": "critical",
                "user_handle": "@election_bot_network",
                "source_url": "https://twitter.com/election_bot_network/status/live_demo_1"
            },
            {
                "title": "⚠️ HIGH ALERT: Anti-India Propaganda Spreading on Facebook",
                "content": "Breaking: Large scale propaganda detected - 'India is a terrorist state, destroy Indian economy, hate Indian government'",
                "platform": "Facebook",
                "region": "Punjab",
                "confidence": 94.2,
                "threat_type": "critical",
                "user_handle": "anti.india.propaganda.group",
                "source_url": "https://facebook.com/groups/anti_india_demo"
            },
            {
                "title": "🔍 DETECTED: Separatist Content Distribution Network",
                "content": "Khalistan zindabad, free Kashmir from India, break India into pieces, azad Kashmir movement",
                "platform": "Instagram",
                "region": "Kashmir",
                "confidence": 91.5,
                "threat_type": "high",
                "user_handle": "@separatist_content_live",
                "source_url": "https://instagram.com/p/separatist_demo_2024"
            },
            {
                "title": "📱 MONITORING: WhatsApp Groups Spreading Hate Against India",
                "content": "Forwarded message: India murdabad, Pakistan zindabad, Indian army terrorists, fake country India",
                "platform": "WhatsApp",
                "region": "Mumbai",
                "confidence": 89.3,
                "threat_type": "high",
                "user_handle": "hate_india_group_demo",
                "source_url": None
            },
            {
                "title": "🎯 ACTIVE: TikTok Anti-Indian Culture Campaign",
                "content": "Indian culture is backward, hate Indian traditions, destroy Indian festivals, boycott Indian movies",
                "platform": "TikTok",
                "region": "Bangalore",
                "confidence": 87.1,
                "threat_type": "medium",
                "user_handle": "@culture_attack_demo",
                "source_url": "https://tiktok.com/@culture_attack_demo/video/demo2024"
            },
            {
                "title": "🔴 LIVE THREAT: Reddit Anti-India Economic Discussion",
                "content": "India's economy is fake, Indian GDP numbers are lies, boycott Indian products worldwide",
                "platform": "Reddit",
                "region": "Chennai",
                "confidence": 78.6,
                "threat_type": "medium",
                "user_handle": "economic_sabotage_user",
                "source_url": "https://reddit.com/r/demo_anti_india/comments/live_threat"
            }
        ]
        
        # Add demo threats with recent timestamps for live feel
        for i, threat_data in enumerate(demo_threats):
            # Stagger timestamps to show recent activity
            minutes_ago = i * 5 + random.randint(1, 10)
            detected_time = datetime.now() - timedelta(minutes=minutes_ago)
            
            threat = ThreatDetection(
                title=threat_data["title"],
                content=threat_data["content"],
                platform=threat_data["platform"],
                region=threat_data["region"],
                confidence=threat_data["confidence"],
                threat_type=threat_data["threat_type"],
                detected_at=detected_time,
                source_url=threat_data["source_url"],
                user_handle=threat_data["user_handle"],
                social_media_id=f"demo_live_{i+1}_{random.randint(100000, 999999)}",
                analysis_result={
                    "riskLevel": f"{threat_data['threat_type'].title()} Risk",
                    "confidence": int(threat_data["confidence"]),
                    "summary": f"LIVE DEMO: {threat_data['threat_type'].title()}-level anti-India content detected in real-time monitoring.",
                    "indicators": [
                        f"Anti-India keywords detected in {threat_data['platform']} content",
                        f"{threat_data['threat_type'].title()}-risk content patterns identified",
                        "Coordinated messaging indicators present",
                        "Real-time threat classification active"
                    ],
                    "recommendedAction": f"DEMO MODE: {threat_data['threat_type'].upper()} PRIORITY - Report to cybercrime.gov.in and initiate investigation."
                }
            )
            db.add(threat)
        
        # Update system stats for live demo
        stats = db.query(SystemStats).first()
        if stats:
            stats.threats_detected_total = 342
            stats.threats_blocked_total = 156
            stats.system_load_percentage = 34.7
            stats.uptime_percentage = 99.96
            stats.threats_detected_hourly = 15
            stats.threats_blocked_hourly = 11
        
        # Update platform analytics for live demo
        platforms_live_data = [
            {"platform": "Twitter", "campaigns": 67, "threat_level": "CRITICAL", "activity": 95, "change": 12.3},
            {"platform": "Facebook", "campaigns": 54, "threat_level": "CRITICAL", "activity": 88, "change": 8.7},
            {"platform": "Instagram", "campaigns": 41, "threat_level": "HIGH", "activity": 76, "change": 15.2},
            {"platform": "WhatsApp", "campaigns": 38, "threat_level": "HIGH", "activity": 82, "change": 6.9},
            {"platform": "TikTok", "campaigns": 29, "threat_level": "MODERATE", "activity": 64, "change": -3.1},
            {"platform": "Telegram", "campaigns": 25, "threat_level": "MODERATE", "activity": 58, "change": 9.4},
            {"platform": "YouTube", "campaigns": 19, "threat_level": "LOW", "activity": 34, "change": -1.8},
            {"platform": "Reddit", "campaigns": 16, "threat_level": "MODERATE", "activity": 42, "change": 4.6}
        ]
        
        for platform_data in platforms_live_data:
            analytics = db.query(PlatformAnalytics).filter(
                PlatformAnalytics.platform_name == platform_data["platform"]
            ).first()
            
            if analytics:
                analytics.total_campaigns = platform_data["campaigns"]
                analytics.threat_level = platform_data["threat_level"]
                analytics.percentage_change = platform_data["change"]
                analytics.activity_percentage = platform_data["activity"]
                analytics.last_updated = datetime.now()
        
        db.commit()
        print("✅ Enhanced demo scenarios added successfully!")
        print(f"   - Added {len(demo_threats)} live threat scenarios")
        print(f"   - Updated {len(platforms_live_data)} platform analytics")
        print("   - Enhanced system statistics for live demo")
        
    except Exception as e:
        print(f"❌ Error adding demo scenarios: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🎬 Setting up live demo scenarios...")
    add_demo_scenarios()
    print("🎉 Live demo setup complete!")
EOF

chmod +x backend/scripts/add_demo_scenarios.py

echo ""
echo -e "${GREEN}🎉 Live Demo Setup Complete!${NC}"
echo "========================================="
echo ""
echo -e "${YELLOW}Quick Start Commands:${NC}"
echo -e "  ${BLUE}./start_demo.sh${NC}     # Start the complete demo"
echo -e "  ${BLUE}./stop_demo.sh${NC}      # Stop all demo services"
echo ""
echo -e "${YELLOW}Demo URLs:${NC}"
echo -e "  🌐 Frontend:       http://localhost:3000"
echo -e "  🔧 Backend API:    http://localhost:8000"
echo -e "  📚 API Docs:       http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Run './start_demo.sh' to start the demo"
echo "2. Open http://localhost:3000 in your browser"
echo "3. Follow the demo script in DEMO_PRESENTATION.md"
echo ""