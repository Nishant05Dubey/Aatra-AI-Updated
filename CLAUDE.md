# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aatra AI is a comprehensive cybersecurity operations center focused on the "Anti-India Campaign Monitoring System (AICMS)". The system provides:

- **Real-time threat detection** and monitoring dashboard
- **AI-powered content analysis** for anti-India sentiment detection  
- **Integration with cybercrime.gov.in** for automated reporting
- **Platform-specific campaign analytics** across social media platforms
- **Machine learning model performance** tracking
- **Twitter/X API integration** for real-time social media monitoring
- **Complete backend infrastructure** with PostgreSQL and Redis

## Architecture

This is a **full-stack application** with separate frontend and backend:

### Backend (FastAPI)
- **FastAPI**: Modern Python web framework with automatic API documentation
- **PostgreSQL**: Robust database for threat storage and analytics
- **Redis**: High-performance caching for real-time data
- **ML Pipeline**: Hugging Face Transformers for hate speech detection
- **Social Media Integration**: Twitter API for real-time monitoring
- **Automated Reporting**: Integration with cybercrime.gov.in portal

### Frontend (HTML/JavaScript)
- **Single `index.html`** file with vanilla JavaScript
- **Backend Integration**: Consumes FastAPI endpoints instead of hardcoded data
- **Styling**: Tailwind CSS (via CDN) with custom glass-morphism effects
- **Charts**: Chart.js integration for data visualization
- **Real-time Updates**: Periodic API calls for live data refresh

### Key Components

- **Dashboard Section**: Main monitoring interface with threat statistics and real-time alerts
- **Content Analysis Section**: Text/URL analysis interface using Gemini AI
- **AI Learning Center**: Model performance metrics and learning event tracking
- **Reporting Modal**: Integrated cybercrime.gov.in reporting functionality

### JavaScript Architecture

Located in `index.html:427-841`, the application uses:

- **Mock Data**: Predefined threat scenarios for demonstration (`threatsData` array)
- **Gemini API Integration**: Real AI-powered content analysis with retry logic
- **Event-Driven UI**: Tab switching, modal management, and dynamic content rendering
- **Real-time Updates**: Live time display and threat level indicators

## Development Workflow

### Quick Start (Recommended)

```bash
# Run the complete setup
./run_setup.sh
```

### Manual Development Setup

1. **Backend Development**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python scripts/init_db.py  # Initialize with sample data
   uvicorn app.main:app --reload --port 8000
   ```

2. **Frontend Development**:
   ```bash
   python -m http.server 3000  # Serve index.html
   ```

3. **Docker Development**:
   ```bash
   docker-compose up -d  # Start all services
   docker-compose logs -f  # View logs
   ```

### Key Files Structure

```
backend/
├── app/
│   ├── api/              # API route handlers
│   ├── ml/               # ML pipeline (hate_detector.py)
│   ├── services/         # Business logic (social_monitor.py)
│   ├── models.py         # Database models
│   ├── config.py         # Configuration settings
│   └── main.py           # FastAPI application
├── scripts/
│   └── init_db.py        # Database initialization
└── requirements.txt      # Python dependencies

index.html                # Frontend application (updated to use backend APIs)
docker-compose.yml        # Complete deployment setup
```

## API Endpoints

The backend provides RESTful APIs for all functionality:

### Dashboard APIs
- `GET /api/dashboard/stats` - Real-time threat statistics
- `GET /api/dashboard/threats/live` - Live threat feed with filtering
- `GET /api/dashboard/platforms/analytics` - Platform-wise campaign analytics
- `POST /api/dashboard/threats/summarize` - AI-generated threat summaries

### Analysis APIs
- `POST /api/analysis/content` - Analyze text for anti-India hate detection
- `GET /api/analysis/keywords` - Get current monitoring keywords
- `POST /api/analysis/keywords` - Add new monitoring keywords

### Reporting APIs
- `POST /api/reports/create` - Create cybercrime report
- `GET /api/reports/generate/{threat_id}` - Generate formatted report
- `GET /api/reports/list` - List all submitted reports

## Machine Learning Pipeline

- **Primary Model**: `martin-ha/toxic-comment-model` (Hugging Face)
- **Custom Detection**: Anti-India keyword analysis
- **Processing**: Real-time content analysis with confidence scoring
- **Integration**: Twitter API for live social media monitoring
- **Location**: `backend/app/ml/hate_detector.py`

## Configuration

Key environment variables in `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/aatra_db

# Twitter API (optional for demo)
TWITTER_API_KEY=your_api_key
TWITTER_BEARER_TOKEN=your_bearer_token

# Security
SECRET_KEY=your_secret_key
```

## Styling System

- **Framework**: Tailwind CSS v3 via CDN
- **Theme**: Dark mode with blue/purple gradient backgrounds
- **Effects**: Custom glass-morphism styling with backdrop blur
- **Responsive**: Mobile-first design with responsive grid layouts
- **Animations**: CSS animations for loading states and hover effects

## Browser Compatibility

Requires modern browser support for:
- ES6+ JavaScript features (async/await, fetch)
- CSS backdrop-filter for glass effects
- Clipboard API for report copying functionality