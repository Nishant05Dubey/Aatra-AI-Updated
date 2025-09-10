#!/usr/bin/env python3
"""
Initialize database with sample data for demo purposes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.database import SessionLocal, engine
from app.models import Base, ThreatDetection, SystemStats, PlatformAnalytics, AIModelMetrics, MonitoringKeywords


def init_database():
    """Initialize database with tables and sample data"""
    print("🔧 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("📊 Adding sample threat data...")
        
        # Sample threat data
        sample_threats = [
            {
                "title": "Coordinated Anti-India Disinformation Campaign",
                "content": "Spreading false information about Indian achievements and promoting anti-national sentiment",
                "platform": "Twitter",
                "region": "Mumbai",
                "confidence": 89.5,
                "threat_type": "high",
                "user_handle": "@suspicious_user1",
                "source_url": "https://twitter.com/suspicious_user1/status/123456789"
            },
            {
                "title": "Separatist Content Distribution Network",
                "content": "Large-scale distribution of separatist content with inflammatory messaging",
                "platform": "Facebook",
                "region": "Punjab",
                "confidence": 94.2,
                "threat_type": "critical",
                "user_handle": "separatist.group",
                "source_url": "https://facebook.com/post/987654321"
            },
            {
                "title": "Hate Speech Against Indian Policies",
                "content": "Systematic hate speech targeting Indian government policies and institutions",
                "platform": "Instagram",
                "region": "Delhi",
                "confidence": 76.8,
                "threat_type": "medium",
                "user_handle": "@anti_policy_user",
                "source_url": "https://instagram.com/p/ABC123DEF456"
            },
            {
                "title": "Anti-National Propaganda Bot Network",
                "content": "Automated bot network spreading coordinated anti-national propaganda",
                "platform": "Twitter",
                "region": "Bangalore",
                "confidence": 91.7,
                "threat_type": "critical",
                "user_handle": "@bot_network_lead",
                "source_url": "https://twitter.com/bot_network_lead/status/456789123"
            },
            {
                "title": "Misleading Information About Indian Economy",
                "content": "Spreading false economic data and misleading information about India's growth",
                "platform": "WhatsApp",
                "region": "Chennai",
                "confidence": 68.3,
                "threat_type": "medium",
                "user_handle": "economic_misinformation_group",
                "source_url": None
            }
        ]
        
        # Add sample threats
        for threat_data in sample_threats:
            # Random time in the last 24 hours
            random_hours = random.randint(1, 24)
            detected_time = datetime.now() - timedelta(hours=random_hours)
            
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
                social_media_id=f"demo_{random.randint(100000, 999999)}",
                analysis_result={
                    "riskLevel": f"{threat_data['threat_type'].title()} Risk",
                    "confidence": int(threat_data["confidence"]),
                    "summary": f"Analysis detected {threat_data['threat_type']}-level anti-India content requiring attention.",
                    "indicators": [
                        "Anti-India keywords detected",
                        f"{threat_data['threat_type'].title()}-risk content patterns",
                        "Coordinated messaging indicators"
                    ],
                    "recommendedAction": "Monitor and report to appropriate authorities"
                }
            )
            db.add(threat)
        
        print("📈 Adding system statistics...")
        
        # Initialize system stats
        stats = SystemStats(
            threats_detected_total=len(sample_threats) + 150,
            threats_blocked_total=89,
            system_load_percentage=28.5,
            uptime_percentage=99.94,
            threats_detected_hourly=8,
            threats_blocked_hourly=6
        )
        db.add(stats)
        
        print("🌐 Adding platform analytics...")
        
        # Platform analytics
        platforms_data = [
            {"platform": "Twitter", "campaigns": 45, "threat_level": "HIGH", "activity": 85},
            {"platform": "Facebook", "campaigns": 38, "threat_level": "CRITICAL", "activity": 92},
            {"platform": "Instagram", "campaigns": 28, "threat_level": "MODERATE", "activity": 65},
            {"platform": "WhatsApp", "campaigns": 32, "threat_level": "MODERATE", "activity": 70},
            {"platform": "Telegram", "campaigns": 19, "threat_level": "HIGH", "activity": 45},
            {"platform": "YouTube", "campaigns": 15, "threat_level": "LOW", "activity": 28},
            {"platform": "TikTok", "campaigns": 12, "threat_level": "MODERATE", "activity": 22},
            {"platform": "Reddit", "campaigns": 9, "threat_level": "LOW", "activity": 18}
        ]
        
        for platform_data in platforms_data:
            analytics = PlatformAnalytics(
                platform_name=platform_data["platform"],
                total_campaigns=platform_data["campaigns"],
                threat_level=platform_data["threat_level"],
                percentage_change=random.uniform(-5.0, 8.0),
                activity_percentage=platform_data["activity"]
            )
            db.add(analytics)
        
        print("🤖 Adding AI model metrics...")
        
        # AI Model metrics
        ai_metrics = AIModelMetrics(
            model_version="v2.4.1",
            accuracy_rate=94.2,
            verified_campaigns=156,
            false_positives=12,
            total_reports=168,
            pattern_recognition_rate=96.7,
            realtime_learning_rate=91.4,
            analyses_per_minute=842,
            daily_analysis_count=2567
        )
        db.add(ai_metrics)
        
        print("🔍 Adding monitoring keywords...")
        
        # Monitoring keywords
        keywords_data = [
            {"keyword": "anti india", "category": "hate_speech", "weight": 2.0},
            {"keyword": "hate india", "category": "hate_speech", "weight": 2.5},
            {"keyword": "destroy india", "category": "hate_speech", "weight": 3.0},
            {"keyword": "india terrorist", "category": "hate_speech", "weight": 2.8},
            {"keyword": "khalistan", "category": "separatist", "weight": 2.5},
            {"keyword": "azad kashmir", "category": "separatist", "weight": 2.3},
            {"keyword": "free kashmir", "category": "separatist", "weight": 2.0},
            {"keyword": "pakistan zindabad", "category": "anti_national", "weight": 1.8},
        ]
        
        for keyword_data in keywords_data:
            keyword = MonitoringKeywords(
                keyword=keyword_data["keyword"],
                category=keyword_data["category"],
                weight=keyword_data["weight"]
            )
            db.add(keyword)
        
        db.commit()
        print("✅ Database initialized successfully!")
        print(f"   - Created {len(sample_threats)} sample threats")
        print(f"   - Added {len(platforms_data)} platform analytics")
        print(f"   - Configured {len(keywords_data)} monitoring keywords")
        print(f"   - Initialized system statistics and AI metrics")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Initializing Aatra AI database...")
    init_database()
    print("🎉 Database initialization complete!")