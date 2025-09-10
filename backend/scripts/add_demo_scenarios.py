#!/usr/bin/env python3
"""
Add enhanced demo scenarios to the database for live presentations
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import ThreatDetection, SystemStats, PlatformAnalytics
import random

# Database setup
DATABASE_URL = "sqlite:///./aatra_test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Enhanced demo threat scenarios
DEMO_SCENARIOS = [
    {
        "content": "I hate India and want to destroy everything Indian. Pakistan zindabad! Death to Indian democracy!",
        "platform": "twitter",
        "risk_level": "critical",
        "confidence_score": 0.94,
        "keywords": ["hate", "destroy", "death", "pakistan zindabad"],
        "location": "Unknown"
    },
    {
        "content": "Khalistan zindabad! Free Kashmir from terrorist Indian army. Break India into pieces!",
        "platform": "facebook",
        "risk_level": "critical", 
        "confidence_score": 0.91,
        "keywords": ["khalistan", "free kashmir", "terrorist", "break india"],
        "location": "Canada"
    },
    {
        "content": "Indian government are terrorists. Death to all Indians. Destroy Hinduism completely!",
        "platform": "instagram",
        "risk_level": "critical",
        "confidence_score": 0.89,
        "keywords": ["terrorists", "death", "destroy hinduism"],
        "location": "Pakistan"
    },
    {
        "content": "Indian culture is backward and primitive. Boycott all Indian festivals and traditions.",
        "platform": "twitter",
        "risk_level": "high",
        "confidence_score": 0.76,
        "keywords": ["backward", "primitive", "boycott"],
        "location": "UK"
    },
    {
        "content": "India's economy is fake. All Indian GDP numbers are lies. Boycott Indian products.",
        "platform": "reddit",
        "risk_level": "high", 
        "confidence_score": 0.72,
        "keywords": ["fake economy", "gdp lies", "boycott"],
        "location": "USA"
    },
    {
        "content": "Indian army kills innocent people. India is a terrorist nation spreading violence.",
        "platform": "youtube",
        "risk_level": "high",
        "confidence_score": 0.78,
        "keywords": ["army kills", "terrorist nation"],
        "location": "Unknown"
    },
    {
        "content": "India has many problems with corruption and poverty issues that need addressing.",
        "platform": "twitter",
        "risk_level": "moderate",
        "confidence_score": 0.45,
        "keywords": ["corruption", "poverty"],
        "location": "India"
    },
    {
        "content": "Some Indian policies are questionable and need international review and oversight.",
        "platform": "facebook",
        "risk_level": "moderate",
        "confidence_score": 0.38,
        "keywords": ["questionable policies"],
        "location": "USA"
    },
    {
        "content": "I love India and its rich cultural heritage. Proud to be Indian! Jai Hind!",
        "platform": "instagram",
        "risk_level": "low",
        "confidence_score": 0.12,
        "keywords": ["love india", "proud", "jai hind"],
        "location": "India"
    },
    {
        "content": "India has made great progress in technology and space exploration. ISRO achievements!",
        "platform": "twitter", 
        "risk_level": "low",
        "confidence_score": 0.08,
        "keywords": ["progress", "technology", "isro"],
        "location": "India"
    }
]

def add_demo_scenarios():
    """Add enhanced demo scenarios to database"""
    print("🎭 Adding enhanced demo scenarios...")
    
    db = SessionLocal()
    
    try:
        # Clear existing demo data
        db.query(ThreatDetection).delete()
        db.commit()
        
        # Add demo scenarios
        for i, scenario in enumerate(DEMO_SCENARIOS):
            # Create realistic timestamps (recent activity)
            created_time = datetime.utcnow() - timedelta(
                hours=random.randint(1, 48),
                minutes=random.randint(0, 59)
            )
            
            threat = ThreatDetection(
                title=f"Threat Detection #{i+1}",
                content=scenario["content"],
                platform=scenario["platform"],
                threat_type=scenario["risk_level"],
                confidence=scenario["confidence_score"] * 100,  # Convert to 0-100 scale
                region=scenario.get("location", "Unknown"),
                detected_at=created_time,
                analysis_result={"keywords": scenario["keywords"]}
            )
            
            db.add(threat)
        
        # Update system metrics with demo data
        current_time = datetime.utcnow()
        
        # Check if metrics exist, update or create
        metrics = db.query(SystemStats).first()
        if metrics:
            metrics.threats_detected_total = len(DEMO_SCENARIOS)
            metrics.threats_blocked_total = len([s for s in DEMO_SCENARIOS if s["risk_level"] in ["critical", "high"]])
            metrics.system_load_percentage = 34.7
            metrics.uptime_percentage = 99.96
            metrics.threats_detected_hourly = random.randint(15, 45)
            metrics.threats_blocked_hourly = random.randint(8, 25)
            metrics.last_updated = current_time
        else:
            metrics = SystemStats(
                threats_detected_total=len(DEMO_SCENARIOS),
                threats_blocked_total=len([s for s in DEMO_SCENARIOS if s["risk_level"] in ["critical", "high"]]),
                system_load_percentage=34.7,
                uptime_percentage=99.96,
                threats_detected_hourly=random.randint(15, 45),
                threats_blocked_hourly=random.randint(8, 25),
                last_updated=current_time
            )
            db.add(metrics)
        
        # Update platform analytics with threat counts
        platforms = ["twitter", "facebook", "instagram", "youtube", "reddit", "telegram", "whatsapp", "tiktok"]
        
        for platform in platforms:
            platform_threats = [s for s in DEMO_SCENARIOS if s["platform"] == platform]
            threat_count = len(platform_threats) if platform_threats else random.randint(15, 75)
            
            # Get or create platform analytics
            analytics = db.query(PlatformAnalytics).filter_by(platform_name=platform).first()
            if analytics:
                analytics.total_campaigns = threat_count
                analytics.threat_level = "CRITICAL" if threat_count > 50 else "HIGH" if threat_count > 30 else "MODERATE"
                analytics.activity_percentage = min(95, threat_count + random.randint(10, 30))
                analytics.percentage_change = random.uniform(-15.5, 25.8)
                analytics.last_updated = current_time
            else:
                analytics = PlatformAnalytics(
                    platform_name=platform,
                    total_campaigns=threat_count,
                    threat_level="CRITICAL" if threat_count > 50 else "HIGH" if threat_count > 30 else "MODERATE",
                    activity_percentage=min(95, threat_count + random.randint(10, 30)),
                    percentage_change=random.uniform(-15.5, 25.8),
                    last_updated=current_time
                )
                db.add(analytics)
        
        db.commit()
        
        print(f"✅ Added {len(DEMO_SCENARIOS)} enhanced demo scenarios")
        print(f"✅ Updated system metrics and platform analytics") 
        print("🎬 Demo data ready for live presentations!")
        
    except Exception as e:
        print(f"❌ Error adding demo scenarios: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_demo_scenarios()