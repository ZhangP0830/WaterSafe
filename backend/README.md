# WaterSafe Backend API 🚀

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)](https://python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql)](https://mysql.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=for-the-badge&logo=openai)](https://openai.com/)

> High-performance REST API for water safety data management, quality prediction, and AI-powered guidance.

## 🎯 Overview

The WaterSafe Backend is a robust FastAPI-based service that provides comprehensive water safety data management, machine learning-powered water quality predictions, and intelligent guidance systems. Built with modern Python technologies, it offers scalable and maintainable solutions for water safety applications.

## 🏗️ Architecture

```
backend/
├── 📁 api/                    # API route handlers
│   ├── water_sources.py      # Water source management
│   ├── water_quality_prediction.py  # ML prediction endpoints
│   └── guidance.py           # AI guidance system
├── 📁 model/                 # ML models and data
│   ├── site_model_params_1Month.json  # Trained model parameters
│   ├── site_suburb_data.csv  # Historical water quality data
│   └── Pridict_Model.ipynb   # Model training notebook
├── 📄 main.py               # FastAPI application entry point
├── 📄 database.py           # Database configuration
├── 📄 models.py             # SQLAlchemy data models
├── 📄 crud.py              # Database operations
└── 📄 requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- **Python** 3.8+
- **MySQL** 8.0+
- **OpenAI API Key** (for AI guidance features)

### Installation

1. **Clone and navigate to backend**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Set up database**
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE watersafe;
```

6. **Run the application**
```bash
python main.py
```

🌐 **API Server**: http://localhost:8000  
📚 **Interactive Docs**: http://localhost:8000/docs  
🔧 **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/watersafe
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=watersafe

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://water-safety.netlify.app
```





## 🧠 Machine Learning Models

### Water Quality Prediction Model

The system uses a hybrid approach combining:
- **Linear Regression** for trend-based predictions
- **Historical Data Analysis** for pattern recognition
- **Water Quality Index (WQI)** calculation for risk assessment



## 🔒 Security Features

### Input Validation
- **Pydantic models** for request/response validation
- **SQL injection prevention** with SQLAlchemy ORM
- **Type checking** and data sanitization

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://water-safety.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🚀 Deployment

### Production Setup
```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export DATABASE_URL=mysql+pymysql://user:pass@host:port/db
export OPENAI_API_KEY=your_production_key

# Run with production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 Monitoring & Logging

### Health Check Endpoints
- `GET /health` - Basic health check
- `GET /api/prediction/health` - Prediction service health
- `GET /api/guidance/health` - Guidance service health

### Logging Configuration
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Run tests before committing
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function parameters
- Add docstrings for all public functions
- Write tests for new features

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ZhangP0830/WaterSafe/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ZhangP0830/WaterSafe/discussions)

---