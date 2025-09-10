"""
Simplified hate detector for testing without heavy ML dependencies
"""
import re
import logging
from typing import Dict, List
from app.config import settings

logger = logging.getLogger(__name__)


class SimpleAntiIndiaHateDetector:
    """
    Simplified ML Pipeline for detecting anti-India hate speech using keyword analysis
    This version works without requiring heavy ML libraries for testing
    """
    
    def __init__(self):
        self.is_loaded = True  # Always loaded for simple detector
        
        # Anti-India specific keywords and patterns
        self.anti_india_keywords = [
            "hate india", "destroy india", "india terrorist", "fake india", 
            "india fake", "anti india", "india down", "boycott india", 
            "india enemy", "pakistan zindabad", "india murdabad",
            "hindu terrorist", "indian terrorist", "bharat down",
            "kashmir azad", "khalistan zindabad", "break india"
        ]
        
        # Separatist keywords
        self.separatist_keywords = [
            "khalistan", "azad kashmir", "independent kashmir", 
            "free kashmir", "naxal", "maoist india", "break bharat"
        ]
        
        logger.info("Simple hate detector initialized successfully!")
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def detect_anti_india_keywords(self, text: str) -> Dict:
        """Detect anti-India keywords and patterns"""
        text_lower = text.lower()
        detected_keywords = []
        separatist_detected = []
        
        # Check for anti-India keywords
        for keyword in self.anti_india_keywords:
            if keyword in text_lower:
                detected_keywords.append(keyword)
        
        # Check for separatist keywords
        for keyword in self.separatist_keywords:
            if keyword in text_lower:
                separatist_detected.append(keyword)
        
        return {
            "anti_india_keywords": detected_keywords,
            "separatist_keywords": separatist_detected,
            "keyword_score": len(detected_keywords) + len(separatist_detected) * 1.5
        }
    
    def classify_hate_speech(self, text: str) -> Dict:
        """Simple hate speech classification based on keywords and patterns"""
        text_lower = text.lower()
        
        # Simple hate speech indicators
        hate_indicators = [
            "hate", "destroy", "kill", "terrorist", "fake", "lie", "propaganda",
            "murdabad", "down with", "death to", "eliminate"
        ]
        
        hate_count = sum(1 for indicator in hate_indicators if indicator in text_lower)
        hate_score = min(hate_count * 0.2, 0.9)  # Max 90% confidence
        
        return {
            "hate_detected": hate_score > 0.5,
            "hate_confidence": hate_score * 100,
            "classification_result": [{"label": "TOXIC" if hate_score > 0.5 else "NON_TOXIC", "score": hate_score}]
        }
    
    def analyze_content(self, text: str, platform: str = "unknown") -> Dict:
        """
        Comprehensive analysis of content for anti-India hate detection
        
        Returns:
            Dict with analysis results matching frontend expectations
        """
        if not text or len(text.strip()) < 3:
            return {
                "riskLevel": "Low Risk",
                "confidence": 0,
                "summary": "Content too short for meaningful analysis.",
                "indicators": ["Insufficient content length"],
                "recommendedAction": "No action required."
            }
        
        # Preprocess text
        clean_text = self.preprocess_text(text)
        
        # Detect anti-India keywords
        keyword_analysis = self.detect_anti_india_keywords(clean_text)
        
        # Classify hate speech
        hate_analysis = self.classify_hate_speech(clean_text)
        
        # Calculate overall threat score
        threat_score = self._calculate_threat_score(
            keyword_analysis, hate_analysis, text
        )
        
        # Determine risk level
        risk_level = self._determine_risk_level(threat_score)
        
        # Generate indicators
        indicators = self._generate_indicators(keyword_analysis, hate_analysis, text)
        
        # Generate summary and recommendations
        summary = self._generate_summary(risk_level, keyword_analysis, hate_analysis)
        recommended_action = self._generate_recommendation(risk_level, threat_score)
        
        return {
            "riskLevel": risk_level,
            "confidence": min(int(threat_score), 100),
            "summary": summary,
            "indicators": indicators,
            "recommendedAction": recommended_action,
            "detailed_analysis": {
                "keyword_analysis": keyword_analysis,
                "hate_analysis": hate_analysis,
                "threat_score": threat_score,
                "platform": platform,
                "text_length": len(text)
            }
        }
    
    def _calculate_threat_score(self, keyword_analysis: Dict, hate_analysis: Dict, text: str) -> float:
        """Calculate overall threat score (0-100)"""
        score = 0.0
        
        # Base score from hate speech detection
        if not hate_analysis.get("error"):
            score += hate_analysis.get("hate_confidence", 0) * 0.4
        
        # Keyword-based scoring (enhanced for demo)
        keyword_score = keyword_analysis.get("keyword_score", 0)
        if keyword_score > 0:
            score += min(keyword_score * 25, 60)  # Max 60 points from keywords (increased)
        
        # Additional context factors (enhanced)
        if "terrorist" in text.lower():
            score += 30
        if "destroy" in text.lower() or "kill" in text.lower() or "death" in text.lower():
            score += 25  # Increased from 15
        if any(word in text.lower() for word in ["fake", "propaganda", "lie"]):
            score += 15  # Increased from 10
            
        # Strong anti-India indicators (new)
        if any(phrase in text.lower() for phrase in ["hate india", "fuck india", "destroy india"]):
            score += 35  # Strong boost for direct anti-India hate
            
        # Threat language detection (new)
        if any(word in text.lower() for word in ["bomb", "attack", "violence", "war"]):
            score += 20
        
        # Separatist content gets higher score
        if keyword_analysis.get("separatist_keywords"):
            score += 25
        
        return min(score, 100.0)
    
    def _determine_risk_level(self, threat_score: float) -> str:
        """Determine risk level based on threat score"""
        if threat_score >= 80:
            return "Critical Risk"
        elif threat_score >= 60:
            return "High Risk"
        elif threat_score >= 30:
            return "Moderate Risk"
        else:
            return "Low Risk"
    
    def _generate_indicators(self, keyword_analysis: Dict, hate_analysis: Dict, text: str) -> List[str]:
        """Generate list of detected indicators"""
        indicators = []
        
        # Keyword indicators
        if keyword_analysis.get("anti_india_keywords"):
            indicators.append(f"Anti-India keywords detected: {', '.join(keyword_analysis['anti_india_keywords'][:3])}")
        
        if keyword_analysis.get("separatist_keywords"):
            indicators.append(f"Separatist content detected: {', '.join(keyword_analysis['separatist_keywords'][:2])}")
        
        # Hate speech indicators
        if hate_analysis.get("hate_detected"):
            indicators.append(f"Hate speech patterns identified (confidence: {hate_analysis.get('hate_confidence', 0):.1f}%)")
        
        # Context indicators
        if "terrorist" in text.lower():
            indicators.append("Terrorism-related terminology used")
        
        if not indicators:
            indicators.append("No significant threat indicators detected")
        
        # Ensure we have at least 3-4 indicators
        while len(indicators) < 3:
            indicators.append("Simple keyword-based analysis completed")
        
        return indicators[:4]
    
    def _generate_summary(self, risk_level: str, keyword_analysis: Dict, hate_analysis: Dict) -> str:
        """Generate analysis summary"""
        if risk_level == "Critical Risk":
            return "Critical anti-India hate content detected with high confidence. The content contains explicit anti-national sentiment, potential separatist messaging, or severe hate speech targeting India. Immediate action and reporting to authorities is recommended."
        
        elif risk_level == "High Risk":
            return "High-risk content identified with concerning anti-India sentiment or hate speech elements. The content shows patterns consistent with organized anti-national campaigns or inflammatory messaging that could incite hatred against India."
        
        elif risk_level == "Moderate Risk":
            return "Moderate risk content detected with some anti-India elements or mild hate speech indicators. While not immediately threatening, this content should be monitored as it may be part of broader negative sentiment campaigns."
        
        else:
            return "Low risk content with minimal or no detectable anti-India sentiment. The analysis found no significant indicators of hate speech or anti-national messaging. Content appears to be within normal parameters."
    
    def _generate_recommendation(self, risk_level: str, threat_score: float) -> str:
        """Generate recommended action based on analysis"""
        if risk_level == "Critical Risk":
            return "IMMEDIATE ACTION: Report to cybercrime.gov.in, document evidence, consider content removal request, and notify relevant authorities for investigation."
        
        elif risk_level == "High Risk":
            return "HIGH PRIORITY: Report to appropriate authorities, monitor for related content, document for pattern analysis, and consider escalation to cybercrime portal."
        
        elif risk_level == "Moderate Risk":
            return "MONITOR: Add to watchlist, track for escalation, document patterns, and prepare for potential reporting if content escalates."
        
        else:
            return "NO ACTION: Continue routine monitoring. Content appears legitimate with no immediate threat indicators detected."


# Global instance
hate_detector = SimpleAntiIndiaHateDetector()