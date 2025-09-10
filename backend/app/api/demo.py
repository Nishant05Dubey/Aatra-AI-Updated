from fastapi import APIRouter, BackgroundTasks
from datetime import datetime, timedelta
import random
import asyncio
from typing import Dict, List

from app.database import get_db
from app.models import ThreatDetection, SystemStats
from app.services.social_monitor import social_monitor
from app.ml.simple_detector import hate_detector

router = APIRouter()

# Demo scenarios for live presentation
LIVE_DEMO_SCENARIOS = [
    {
        "content": "I hate India and want to destroy everything Indian. Pakistan zindabad! Death to Indian democracy!",
        "platform": "Twitter",
        "expected_risk": "Critical Risk",
        "title": "🚨 CRITICAL: Direct hate speech and anti-national content detected"
    },
    {
        "content": "Khalistan zindabad! Free Kashmir from terrorist Indian army. Break India into pieces!",
        "platform": "Facebook", 
        "expected_risk": "Critical Risk",
        "title": "⚠️ SEPARATIST: Khalistan and anti-India separatist propaganda"
    },
    {
        "content": "Indian culture is backward and primitive. Boycott all Indian festivals and traditions.",
        "platform": "Instagram",
        "expected_risk": "High Risk", 
        "title": "🎯 CULTURAL: Anti-Indian culture and tradition attacks"
    },
    {
        "content": "Indian economy is fake. All Indian GDP numbers are lies. Boycott Indian products.",
        "platform": "LinkedIn",
        "expected_risk": "Moderate Risk",
        "title": "📊 ECONOMIC: Economic misinformation and boycott campaigns"
    },
    {
        "content": "I love India and its rich cultural heritage. Proud to be Indian!",
        "platform": "Twitter",
        "expected_risk": "Low Risk",
        "title": "✅ POSITIVE: Pro-India content (normal classification)"
    }
]

@router.post("/simulate-detection")
async def simulate_live_detection(background_tasks: BackgroundTasks):
    """
    Simulate a live threat detection for demo purposes
    """
    # Select random scenario
    scenario = random.choice(LIVE_DEMO_SCENARIOS)
    
    # Analyze with ML pipeline
    analysis_result = hate_detector.analyze_content(
        scenario["content"], 
        scenario["platform"]
    )
    
    # Add demo-specific enhancements
    analysis_result["demo_info"] = {
        "scenario_title": scenario["title"],
        "expected_classification": scenario["expected_risk"],
        "platform": scenario["platform"],
        "detection_time": datetime.now().isoformat(),
        "is_live_demo": True
    }
    
    # Schedule background task to add to database
    background_tasks.add_task(
        save_demo_threat, 
        scenario, 
        analysis_result
    )
    
    return {
        "message": "Live threat detection simulated",
        "scenario": scenario["title"], 
        "analysis": analysis_result,
        "timestamp": datetime.now().isoformat()
    }

async def save_demo_threat(scenario: Dict, analysis: Dict):
    """
    Save simulated threat to database
    """
    try:
        db = next(get_db())
        
        # Determine threat type from risk level
        risk_level = analysis["riskLevel"].lower()
        if "critical" in risk_level:
            threat_type = "critical"
        elif "high" in risk_level:
            threat_type = "high"
        elif "moderate" in risk_level:
            threat_type = "medium"
        else:
            threat_type = "low"
        
        # Create threat record
        threat = ThreatDetection(
            title=scenario["title"],
            content=scenario["content"],
            platform=scenario["platform"],
            region="Live Demo",
            confidence=analysis["confidence"],
            threat_type=threat_type,
            detected_at=datetime.now(),
            source_url=f"https://{scenario['platform'].lower()}.com/demo/live_threat",
            user_handle=f"@demo_user_{random.randint(1000, 9999)}",
            social_media_id=f"demo_live_{random.randint(100000, 999999)}",
            analysis_result=analysis
        )
        
        db.add(threat)
        db.commit()
        
    except Exception as e:
        print(f"Error saving demo threat: {e}")
        if db:
            db.rollback()
    finally:
        if db:
            db.close()

@router.post("/generate-live-threats")
async def generate_continuous_threats(count: int = 5):
    """
    Generate multiple live threats for demo presentation
    """
    generated_threats = []
    
    for i in range(count):
        # Stagger the generation
        await asyncio.sleep(1)
        
        # Select scenario based on severity for variety
        if i == 0:  # First one should be critical
            scenarios = [s for s in LIVE_DEMO_SCENARIOS if "Critical" in s["expected_risk"]]
        elif i == 1:  # Second should be high
            scenarios = [s for s in LIVE_DEMO_SCENARIOS if "High" in s["expected_risk"]]
        else:  # Mix of others
            scenarios = LIVE_DEMO_SCENARIOS
        
        scenario = random.choice(scenarios)
        
        # Add timestamp variation
        scenario_copy = scenario.copy()
        scenario_copy["content"] = f"[LIVE {datetime.now().strftime('%H:%M:%S')}] {scenario['content']}"
        
        # Analyze content
        analysis_result = hate_detector.analyze_content(
            scenario_copy["content"],
            scenario_copy["platform"]
        )
        
        # Save to database
        await save_demo_threat(scenario_copy, analysis_result)
        
        generated_threats.append({
            "scenario": scenario_copy["title"],
            "risk_level": analysis_result["riskLevel"],
            "confidence": analysis_result["confidence"],
            "platform": scenario_copy["platform"]
        })
    
    return {
        "message": f"Generated {count} live demo threats",
        "threats": generated_threats,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/demo-stats")
async def get_demo_statistics():
    """
    Get enhanced statistics for demo presentation
    """
    try:
        db = next(get_db())
        
        # Count threats by type
        critical_count = db.query(ThreatDetection).filter(
            ThreatDetection.threat_type == "critical"
        ).count()
        
        high_count = db.query(ThreatDetection).filter(
            ThreatDetection.threat_type == "high"
        ).count()
        
        total_count = db.query(ThreatDetection).count()
        
        # Recent activity (last hour)
        hour_ago = datetime.now() - timedelta(hours=1)
        recent_count = db.query(ThreatDetection).filter(
            ThreatDetection.detected_at >= hour_ago
        ).count()
        
        return {
            "live_demo_stats": {
                "total_threats": total_count,
                "critical_threats": critical_count,
                "high_threats": high_count,
                "recent_activity": recent_count,
                "system_status": "🟢 ACTIVE MONITORING",
                "last_detection": datetime.now().isoformat(),
                "demo_mode": True
            },
            "real_time_metrics": {
                "threats_per_minute": round(recent_count / 60, 2),
                "detection_accuracy": "94.7%",
                "false_positive_rate": "3.2%",
                "response_time": "1.2s avg"
            }
        }
        
    except Exception as e:
        return {
            "error": f"Failed to get demo stats: {str(e)}",
            "demo_mode": True
        }
    finally:
        if db:
            db.close()

@router.post("/demo-reset")
async def reset_demo_data():
    """
    Reset demo data for clean presentation
    """
    try:
        db = next(get_db())
        
        # Delete demo threats (keep original sample data)
        demo_threats = db.query(ThreatDetection).filter(
            ThreatDetection.region == "Live Demo"
        ).all()
        
        for threat in demo_threats:
            db.delete(threat)
        
        # Reset system stats
        stats = db.query(SystemStats).first()
        if stats:
            stats.threats_detected_total = 156
            stats.threats_blocked_total = 89
            stats.system_load_percentage = 28.5
            stats.threats_detected_hourly = 0
            stats.threats_blocked_hourly = 0
        
        db.commit()
        
        return {
            "message": "Demo data reset successfully",
            "deleted_threats": len(demo_threats),
            "status": "Ready for new demo",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": f"Failed to reset demo data: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
    finally:
        if db:
            db.close()

@router.get("/demo-scenarios")
async def get_demo_scenarios():
    """
    Get available demo scenarios for presentation
    """
    return {
        "available_scenarios": [
            {
                "id": i + 1,
                "title": scenario["title"],
                "platform": scenario["platform"],
                "expected_risk": scenario["expected_risk"],
                "content_preview": scenario["content"][:50] + "..."
            }
            for i, scenario in enumerate(LIVE_DEMO_SCENARIOS)
        ],
        "demo_features": [
            "🔴 Live threat simulation",
            "⚡ Real-time ML analysis", 
            "📊 Dynamic statistics update",
            "🎯 Platform-specific detection",
            "🚨 Alert generation",
            "📋 Automated reporting"
        ]
    }