from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ThreatDetection(Base):
    __tablename__ = "threat_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    platform = Column(String(50), nullable=False)  # twitter, facebook, etc.
    region = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=False)  # 0-100
    threat_type = Column(String(20), nullable=False)  # critical, high, medium, low
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    source_url = Column(String(1000), nullable=True)
    social_media_id = Column(String(100), nullable=True)  # Original post ID
    user_handle = Column(String(100), nullable=True)
    is_verified = Column(Boolean, default=False)
    is_reported = Column(Boolean, default=False)
    analysis_result = Column(JSON, nullable=True)  # Store detailed ML analysis
    
    # Relationships
    reports = relationship("ThreatReport", back_populates="threat")


class ThreatReport(Base):
    __tablename__ = "threat_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    threat_id = Column(Integer, ForeignKey("threat_detections.id"))
    reporter_contact = Column(String(200), nullable=True)
    additional_details = Column(Text, nullable=True)
    is_urgent = Column(Boolean, default=False)
    reported_at = Column(DateTime(timezone=True), server_default=func.now())
    cybercrime_reference = Column(String(100), nullable=True)  # Reference from cybercrime.gov.in
    status = Column(String(20), default="submitted")  # submitted, under_review, resolved
    
    # Relationships
    threat = relationship("ThreatDetection", back_populates="reports")


class PlatformAnalytics(Base):
    __tablename__ = "platform_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    platform_name = Column(String(50), nullable=False)  # Facebook, Twitter, etc.
    total_campaigns = Column(Integer, default=0)
    threat_level = Column(String(20), nullable=False)  # CRITICAL, HIGH, MODERATE, LOW
    percentage_change = Column(Float, default=0.0)  # Percentage change from previous period
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    activity_percentage = Column(Float, default=0.0)  # Activity level 0-100


class SystemStats(Base):
    __tablename__ = "system_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    threats_detected_total = Column(Integer, default=0)
    threats_blocked_total = Column(Integer, default=0)
    system_load_percentage = Column(Float, default=0.0)
    uptime_percentage = Column(Float, default=99.85)
    threats_detected_hourly = Column(Integer, default=0)
    threats_blocked_hourly = Column(Integer, default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())


class AIModelMetrics(Base):
    __tablename__ = "ai_model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String(20), default="v2.4.1")
    accuracy_rate = Column(Float, default=93.2)
    verified_campaigns = Column(Integer, default=0)
    false_positives = Column(Integer, default=0)
    total_reports = Column(Integer, default=0)
    pattern_recognition_rate = Column(Float, default=95.8)
    realtime_learning_rate = Column(Float, default=89.3)
    analyses_per_minute = Column(Integer, default=828)
    daily_analysis_count = Column(Integer, default=2468)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())


class MonitoringKeywords(Base):
    __tablename__ = "monitoring_keywords"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)  # hate_speech, anti_national, etc.
    weight = Column(Float, default=1.0)  # Importance weight
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())