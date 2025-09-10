from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import logging
from app.config import settings

# Try to import redis, fallback gracefully
try:
    import redis
    redis_available = True
except ImportError:
    redis_available = False
    redis = None

logger = logging.getLogger(__name__)

# Database engine with SQLite support
connect_args = {}
if "sqlite" in settings.database_url:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    poolclass=StaticPool,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis connection with fallback
redis_client = None
if redis_available:
    try:
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        # Test connection
        redis_client.ping()
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.warning(f"Redis not available: {e}, using in-memory fallback")
        redis_client = None
else:
    logger.info("Redis module not available, using in-memory fallback")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_redis():
    return redis_client