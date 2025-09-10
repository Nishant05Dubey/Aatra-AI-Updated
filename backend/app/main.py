from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.api import dashboard, analysis, reports, demo
from app.services.social_monitor import social_monitor


# Create database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan - start background monitoring
    """
    # Start social media monitoring in background
    monitoring_task = asyncio.create_task(social_monitor.start_monitoring())
    
    yield
    
    # Cleanup
    social_monitor.stop_monitoring()
    monitoring_task.cancel()


# Initialize FastAPI app
app = FastAPI(
    title=settings.project_name,
    description="Real-time Anti-India hate detection and monitoring system with ML-powered threat analysis",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Content Analysis"])
app.include_router(reports.router, prefix="/api/reports", tags=["Threat Reports"])
app.include_router(demo.router, prefix="/api/demo", tags=["Live Demo"])


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    API root endpoint with basic information
    """
    return """
    <html>
        <head>
            <title>Aatra AI - Anti-India Hate Detection System</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a3d; color: white; }
                .header { text-align: center; margin-bottom: 30px; }
                .endpoint { background: #2a2a5d; padding: 15px; margin: 10px 0; border-radius: 8px; }
                .method { color: #4ade80; font-weight: bold; }
                .path { color: #60a5fa; }
                .status { background: #16a34a; padding: 5px 15px; border-radius: 20px; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🛡️ Aatra AI - AICMS Backend</h1>
                <p>Anti-India Campaign Monitoring System</p>
                <span class="status">● SYSTEM ONLINE</span>
            </div>
            
            <h2>📊 Dashboard Endpoints</h2>
            <div class="endpoint">
                <span class="method">GET</span> <span class="path">/api/dashboard/stats</span><br>
                <small>Get real-time threat statistics</small>
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <span class="path">/api/dashboard/threats/live</span><br>
                <small>Get live threat detections</small>
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <span class="path">/api/dashboard/platforms/analytics</span><br>
                <small>Get platform-wise analytics</small>
            </div>
            
            <h2>🤖 AI Analysis Endpoints</h2>
            <div class="endpoint">
                <span class="method">POST</span> <span class="path">/api/analysis/content</span><br>
                <small>Analyze content for anti-India hate detection</small>
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <span class="path">/api/analysis/keywords</span><br>
                <small>Get monitoring keywords</small>
            </div>
            
            <h2>📋 Reporting Endpoints</h2>
            <div class="endpoint">
                <span class="method">POST</span> <span class="path">/api/reports/create</span><br>
                <small>Create threat report for cybercrime.gov.in</small>
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <span class="path">/api/reports/generate/{threat_id}</span><br>
                <small>Generate formatted report content</small>
            </div>
            
            <p style="text-align: center; margin-top: 40px;">
                <a href="/docs" style="color: #60a5fa;">📖 Interactive API Documentation</a> | 
                <a href="/redoc" style="color: #60a5fa;">📚 ReDoc Documentation</a>
            </p>
        </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "system": "Aatra AI - AICMS",
        "version": "1.0.0",
        "monitoring": social_monitor.is_monitoring,
        "ml_model": hate_detector.is_loaded if 'hate_detector' in globals() else False
    }


@app.post("/admin/refresh-monitoring")
async def refresh_monitoring(background_tasks: BackgroundTasks):
    """
    Admin endpoint to refresh monitoring data
    """
    background_tasks.add_task(social_monitor.start_monitoring)
    return {"message": "Monitoring refresh initiated"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False
    )