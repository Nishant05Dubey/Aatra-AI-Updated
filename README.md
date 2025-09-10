# Aatra AI - Anti-India Campaign Monitoring System (AICMS)

<div align="center">

🛡️ **Real-time AI-powered Anti-India Hate Detection System** 🛡️

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 🎯 **Project Overview**

Aatra AI is a comprehensive cybersecurity operations center designed to detect, analyze, and report anti-India campaigns across social media platforms. Built for hackathons and real-world deployment, it combines advanced machine learning with real-time monitoring to protect India's digital sovereignty.

### 🚀 **Key Features**

- **Real-time Social Media Monitoring** - Twitter/X integration with automated content scanning
- **AI-Powered Hate Detection** - Advanced ML models for anti-India sentiment analysis
- **Live Threat Dashboard** - Real-time threat visualization and analytics
- **Automated Reporting** - Direct integration with cybercrime.gov.in portal
- **Platform Analytics** - Cross-platform campaign tracking (Facebook, Twitter, Instagram, etc.)
- **ML Model Performance Tracking** - Continuous learning and accuracy monitoring

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Frontend      │    │   Backend API    │    │   ML Pipeline      │
│   (HTML/JS)     │◄──►│   (FastAPI)      │◄──►│   (Transformers)    │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
            ┌───────▼────┐ ┌────▼────┐ ┌───▼────────┐
            │ PostgreSQL │ │  Redis  │ │ Twitter API│
            │ Database   │ │ Cache   │ │Integration │
            └────────────┘ └─────────┘ └────────────┘
```

## 🛠️ **Technology Stack**

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Robust relational database
- **Redis** - High-performance caching
- **SQLAlchemy** - Python SQL toolkit
- **Hugging Face Transformers** - ML model pipeline

### Machine Learning
- **BERT-based Models** - For hate speech detection
- **Custom Anti-India Classifiers** - Specialized sentiment analysis
- **Real-time Processing** - Stream processing for social media content

### Frontend
- **Vanilla JavaScript** - Lightweight and fast
- **Tailwind CSS** - Modern styling framework
- **Chart.js** - Data visualization

### Deployment
- **Docker & Docker Compose** - Containerized deployment
- **Nginx** - Reverse proxy and static serving
- **Health Checks** - Monitoring and auto-recovery

## 🚀 **Quick Start**

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Twitter API credentials (optional for demo)

### 1. **Clone Repository**
```bash
git clone <repository-url>
cd Aatra-AI-Updated
```

### 2. **Environment Setup**
```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit .env file with your configurations
nano backend/.env
```

### 3. **Start with Docker** (Recommended)
```bash
# Start all services
docker-compose up -d

# Initialize database with sample data
docker-compose exec backend python scripts/init_db.py

# View logs
docker-compose logs -f
```

### 4. **Manual Development Setup**
```bash
# Setup backend
cd backend
pip install -r requirements.txt
python scripts/init_db.py
uvicorn app.main:app --reload

# Serve frontend
cd ..
python -m http.server 3000
```

## 📊 **API Endpoints**

### Dashboard APIs
- `GET /api/dashboard/stats` - Real-time threat statistics
- `GET /api/dashboard/threats/live` - Live threat feed
- `GET /api/dashboard/platforms/analytics` - Platform analytics
- `POST /api/dashboard/threats/summarize` - AI threat summary

### Analysis APIs
- `POST /api/analysis/content` - Analyze text content
- `GET /api/analysis/keywords` - Get monitoring keywords
- `POST /api/analysis/keywords` - Add new keywords

### Reporting APIs
- `POST /api/reports/create` - Create threat report
- `GET /api/reports/generate/{threat_id}` - Generate report content
- `GET /api/reports/list` - List all reports

## 🎛️ **Configuration**

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/aatra_db

# Redis
REDIS_URL=redis://localhost:6379

# Twitter API (Optional - demo works without)
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret

# Security
SECRET_KEY=your_super_secret_key
```

### ML Model Configuration
The system uses pre-trained models for hate speech detection:
- **Primary Model**: `martin-ha/toxic-comment-model`
- **Fallback Processing**: Custom keyword-based detection
- **Confidence Threshold**: 70% (configurable)

## 📈 **Monitoring Keywords**

The system monitors for various anti-India patterns:
- **Hate Speech**: "anti india", "hate india", "destroy india"
- **Separatist Content**: "khalistan", "azad kashmir", "free kashmir" 
- **Anti-National**: "pakistan zindabad", "india down", "boycott india"

## 🔧 **Development**

### Project Structure
```
Aatra-AI-Updated/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── ml/             # ML pipeline
│   │   ├── models.py       # Database models
│   │   ├── services/       # Business logic
│   │   └── main.py         # Application entry
│   ├── scripts/            # Utility scripts
│   └── requirements.txt    # Python dependencies
├── index.html              # Frontend application
├── docker-compose.yml      # Docker orchestration
└── README.md              # This file
```

### Adding New Features

1. **New ML Models**: Add to `backend/app/ml/`
2. **API Endpoints**: Create in `backend/app/api/`
3. **Database Models**: Update `backend/app/models.py`
4. **Frontend Features**: Modify `index.html`

## 🚨 **Security Considerations**

- **API Keys**: Use environment variables, never hardcode
- **Rate Limiting**: Implement for public endpoints
- **Input Validation**: Sanitize all user inputs
- **HTTPS**: Use SSL/TLS in production
- **Database Security**: Use parameterized queries

## 📸 **Screenshots**

### Dashboard
- Real-time threat monitoring
- Platform-wise analytics
- Live threat feed with confidence scores

### Content Analysis
- AI-powered hate speech detection
- Risk assessment and recommendations
- Detailed threat indicators

### Reporting System
- Automated cybercrime.gov.in integration
- Comprehensive threat documentation
- Evidence collection and tracking

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛡️ **Disclaimer**

This system is designed for defensive cybersecurity purposes only. It should be used responsibly and in compliance with applicable laws and regulations. The developers are not responsible for any misuse of this technology.

## 📞 **Support**

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check the [documentation](./docs/) for detailed guides

---

<div align="center">

**Built with ❤️ for India's Digital Security**

🇮🇳 **Jai Hind** 🇮🇳

</div>