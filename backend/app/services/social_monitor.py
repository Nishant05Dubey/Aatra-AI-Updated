# Try to import tweepy, fallback gracefully
try:
    import tweepy
    tweepy_available = True
except ImportError:
    tweepy_available = False
    tweepy = None

import asyncio
from typing import List, Dict, Optional
import logging
from datetime import datetime
import json
from app.config import settings
try:
    from app.ml.hate_detector import hate_detector
except ImportError:
    from app.ml.simple_detector import hate_detector
from app.database import get_db, get_redis
from app.models import ThreatDetection, PlatformAnalytics
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class SocialMediaMonitor:
    """
    Real-time social media monitoring for anti-India hate content
    """
    
    def __init__(self):
        self.twitter_api = None
        self.is_monitoring = False
        self.monitored_keywords = settings.monitoring_keywords
        self._setup_twitter_api()
    
    def _setup_twitter_api(self):
        """Initialize Twitter API connection"""
        try:
            if not tweepy_available:
                logger.warning("Tweepy not available - using mock data only")
                return
                
            if not all([
                settings.twitter_api_key,
                settings.twitter_api_secret,
                settings.twitter_access_token,
                settings.twitter_access_token_secret
            ]):
                logger.warning("Twitter API credentials not provided - using mock data")
                return
            
            auth = tweepy.OAuth1UserHandler(
                settings.twitter_api_key,
                settings.twitter_api_secret,
                settings.twitter_access_token,
                settings.twitter_access_token_secret
            )
            
            self.twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
            
            # Test connection
            self.twitter_api.verify_credentials()
            logger.info("Twitter API connected successfully!")
            
        except Exception as e:
            logger.error(f"Failed to setup Twitter API: {e}")
            self.twitter_api = None
    
    async def fetch_twitter_content(self, keywords: List[str], count: int = 20) -> List[Dict]:
        """
        Fetch recent tweets containing specified keywords
        """
        if not self.twitter_api:
            return self._generate_mock_twitter_data(count)
        
        try:
            tweets = []
            if tweepy_available and self.twitter_api:
                for keyword in keywords[:3]:  # Limit to prevent API exhaustion
                    search_results = tweepy.Cursor(
                        self.twitter_api.search_tweets,
                        q=keyword,
                        lang="en",
                        result_type="recent",
                        tweet_mode="extended"
                    ).items(count // len(keywords))
                    
                    for tweet in search_results:
                        tweet_data = {
                            "id": str(tweet.id),
                            "text": tweet.full_text,
                            "user": tweet.user.screen_name,
                            "created_at": tweet.created_at.isoformat(),
                            "retweet_count": tweet.retweet_count,
                            "like_count": tweet.favorite_count,
                            "platform": "Twitter",
                            "url": f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}",
                            "keyword_matched": keyword
                        }
                        tweets.append(tweet_data)
                
                return tweets
            else:
                return self._generate_mock_twitter_data(count)
            
        except Exception as e:
            logger.error(f"Error fetching Twitter content: {e}")
            return self._generate_mock_twitter_data(count)
    
    def _generate_mock_twitter_data(self, count: int = 20) -> List[Dict]:
        """Generate mock Twitter data for demo purposes"""
        mock_tweets = [
            {
                "id": f"tweet_{i}",
                "text": f"Mock anti-India hate content example {i} - this would be real social media content in production",
                "user": f"user_{i}",
                "created_at": datetime.now().isoformat(),
                "retweet_count": 10 + i,
                "like_count": 25 + i * 2,
                "platform": "Twitter",
                "url": f"https://twitter.com/user_{i}/status/tweet_{i}",
                "keyword_matched": settings.monitoring_keywords[i % len(settings.monitoring_keywords)]
            }
            for i in range(1, min(count + 1, 21))
        ]
        
        return mock_tweets
    
    async def process_social_content(self, content_list: List[Dict]) -> List[Dict]:
        """
        Process social media content through ML pipeline
        """
        processed_threats = []
        
        for content in content_list:
            try:
                # Analyze content with ML model
                analysis_result = hate_detector.analyze_content(
                    content["text"], 
                    content.get("platform", "unknown")
                )
                
                # Determine threat type based on confidence
                confidence = analysis_result["confidence"]
                if confidence >= 80:
                    threat_type = "critical"
                elif confidence >= 60:
                    threat_type = "high"
                elif confidence >= 30:
                    threat_type = "medium"
                else:
                    threat_type = "low"
                
                # Create threat object
                threat = {
                    "id": content["id"],
                    "title": self._generate_threat_title(analysis_result, content),
                    "content": content["text"],
                    "platform": content["platform"],
                    "region": self._determine_region(content),
                    "confidence": confidence,
                    "threat_type": threat_type,
                    "detected_at": datetime.now(),
                    "source_url": content.get("url"),
                    "social_media_id": content["id"],
                    "user_handle": content.get("user"),
                    "analysis_result": analysis_result,
                    "description": analysis_result["summary"][:200] + "..."
                }
                
                processed_threats.append(threat)
                
            except Exception as e:
                logger.error(f"Error processing content {content.get('id')}: {e}")
                continue
        
        return processed_threats
    
    def _generate_threat_title(self, analysis: Dict, content: Dict) -> str:
        """Generate appropriate threat title based on analysis"""
        indicators = analysis.get("indicators", [])
        
        if "separatist" in str(indicators).lower():
            return f"Separatist Content Distribution Network"
        elif "terrorist" in str(indicators).lower():
            return f"Terrorism-Related Anti-India Content"
        elif "hate speech" in str(indicators).lower():
            return f"Coordinated Anti-India Hate Campaign"
        elif "propaganda" in str(indicators).lower() or "fake" in str(indicators).lower():
            return f"Fabricated Stories About Indian Achievements"
        else:
            return f"Suspicious Anti-India Social Media Activity"
    
    def _determine_region(self, content: Dict) -> str:
        """Determine region based on content analysis (simplified)"""
        regions = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Punjab", "Kashmir", "Online"]
        # This would ideally use geolocation or user profile analysis
        return regions[hash(content.get("user", "unknown")) % len(regions)]
    
    async def save_threats_to_db(self, threats: List[Dict]):
        """Save detected threats to database"""
        try:
            db = next(get_db())
            
            for threat_data in threats:
                # Check if threat already exists
                existing = db.query(ThreatDetection).filter(
                    ThreatDetection.social_media_id == threat_data["social_media_id"]
                ).first()
                
                if not existing:
                    threat = ThreatDetection(**threat_data)
                    db.add(threat)
            
            db.commit()
            logger.info(f"Saved {len(threats)} threats to database")
            
        except Exception as e:
            logger.error(f"Error saving threats to database: {e}")
            if db:
                db.rollback()
        finally:
            if db:
                db.close()
    
    async def update_platform_analytics(self):
        """Update platform analytics based on recent threat data"""
        try:
            db = next(get_db())
            redis_client = get_redis()
            
            # Get recent threat counts by platform
            platforms = ["Twitter", "Facebook", "Instagram", "WhatsApp", "Telegram", "YouTube", "TikTok", "Reddit"]
            
            for platform in platforms:
                # Count threats for this platform in last 24 hours
                count = db.query(ThreatDetection).filter(
                    ThreatDetection.platform == platform
                ).count()
                
                # Determine threat level based on count
                if count >= 30:
                    threat_level = "CRITICAL"
                elif count >= 20:
                    threat_level = "HIGH"
                elif count >= 10:
                    threat_level = "MODERATE"
                else:
                    threat_level = "LOW"
                
                # Update or create analytics record
                analytics = db.query(PlatformAnalytics).filter(
                    PlatformAnalytics.platform_name == platform
                ).first()
                
                if analytics:
                    old_count = analytics.total_campaigns
                    analytics.total_campaigns = count
                    analytics.threat_level = threat_level
                    analytics.percentage_change = ((count - old_count) / max(old_count, 1)) * 100
                    analytics.activity_percentage = min((count / 50) * 100, 100)  # Normalize to 0-100
                    analytics.last_updated = datetime.now()
                else:
                    analytics = PlatformAnalytics(
                        platform_name=platform,
                        total_campaigns=count,
                        threat_level=threat_level,
                        percentage_change=0.0,
                        activity_percentage=min((count / 50) * 100, 100),
                        last_updated=datetime.now()
                    )
                    db.add(analytics)
                
                # Cache in Redis for fast access
                redis_client.hset(
                    f"platform_analytics:{platform}", 
                    mapping={
                        "total_campaigns": count,
                        "threat_level": threat_level,
                        "percentage_change": analytics.percentage_change,
                        "activity_percentage": analytics.activity_percentage
                    }
                )
            
            db.commit()
            logger.info("Platform analytics updated successfully")
            
        except Exception as e:
            logger.error(f"Error updating platform analytics: {e}")
            if db:
                db.rollback()
        finally:
            if db:
                db.close()
    
    async def start_monitoring(self):
        """Start continuous social media monitoring"""
        self.is_monitoring = True
        logger.info("Starting social media monitoring...")
        
        while self.is_monitoring:
            try:
                # Fetch content from social media
                content = await self.fetch_twitter_content(self.monitored_keywords)
                
                # Process through ML pipeline
                threats = await self.process_social_content(content)
                
                # Save to database
                if threats:
                    await self.save_threats_to_db(threats)
                    await self.update_platform_analytics()
                
                # Wait before next cycle (adjust based on API limits)
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Error in monitoring cycle: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry
    
    def stop_monitoring(self):
        """Stop social media monitoring"""
        self.is_monitoring = False
        logger.info("Social media monitoring stopped")


# Global instance
social_monitor = SocialMediaMonitor()