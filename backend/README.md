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

## 📊 API Documentation

### 🗺️ Water Sources API

#### Get All Water Sources
```http
GET /api/water-sources/
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 100, max: 1000)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Melbourne Water Treatment Plant",
    "type": "Treatment Plant",
    "status": "Active",
    "latitude": -37.8136,
    "longitude": 144.9631,
    "lga": "Melbourne",
    "town": "Melbourne"
  }
]
```

#### Find Nearby Water Sources
```http
GET /api/water-sources/nearby?lat=-37.8136&lon=144.9631&radius_km=10.0
```

**Query Parameters:**
- `lat` (float): Center point latitude
- `lon` (float): Center point longitude
- `radius_km` (float): Search radius in kilometers (default: 10.0)

#### Filter Water Sources
```http
GET /api/water-sources/filter?status=Active&source_type=Treatment Plant&lga=Melbourne
```

**Query Parameters:**
- `status` (string): Filter by status
- `source_type` (string): Filter by source type
- `lga` (string): Filter by local government area
- `town` (string): Filter by town

### 📈 Water Quality Prediction API

#### Predict Water Quality
```http
POST /api/prediction/predict
```

**Request Body:**
```json
{
  "site_id": "MEL001"
}
```

**Response:**
```json
{
  "site_id": "MEL001",
  "prediction_date": "2024-02-15",
  "parameters": {
    "Chloride as Cl": 45.2,
    "Calcium (Total)": 78.5,
    "Total Magnesium": 32.1,
    "Sodium as Na": 89.3,
    "Potassium as K": 8.7,
    "Salinity as EC@25 (lab)": 234.5,
    "pH": 7.2
  },
  "wqi_score": 85.4,
  "risk_level": "Safe",
  "recommendations": [
    "Water quality is safe for drinking",
    "Continue regular monitoring",
    "No immediate action required"
  ]
}
```

#### Get Available Sites
```http
GET /api/prediction/sites
```

#### Search Sites by Suburb
```http
POST /api/prediction/search-by-suburb
```

**Request Body:**
```json
{
  "suburb_name": "Melbourne"
}
```

### 🤖 AI Guidance API

#### Generate Sanitation Checklist
```http
POST /api/guidance/checklist
```

**Request Body:**
```json
{
  "mode": "general",
  "place": "home",
  "profile": {
    "pregnant": false,
    "infant": true
  },
  "issues": ["toilet_unusable", "no_running_water"]
}
```

**Response:**
```json
{
  "summary_top3": [
    {
      "title": "Set up hand hygiene points",
      "body": "Soap + water; ABHR (≥60%) as fallback",
      "priority": "critical",
      "badges": ["Infant Priority"],
      "sources": [
        {
          "label": "WHO",
          "url": "https://www.who.int/health-topics/water-sanitation-and-hygiene-wash"
        }
      ]
    }
  ],
  "sections": [
    {
      "name": "General Hygiene",
      "items": [...]
    }
  ],
  "notes": [
    {
      "type": "infant",
      "text": "Infants are more vulnerable to infections"
    }
  ],
  "sources": [...]
}
```

#### Chat with AI Assistant
```http
POST /api/guidance/chat
```

**Request Body:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do I safely dispose of waste during a flood?"
    }
  ],
  "context": {
    "mode": "flood",
    "place": "home",
    "profile": {
      "pregnant": false,
      "infant": false
    }
  },
  "checklist": {},
  "sources": []
}
```

## 🧠 Machine Learning Models

### Water Quality Prediction Model

The system uses a hybrid approach combining:
- **Linear Regression** for trend-based predictions
- **Historical Data Analysis** for pattern recognition
- **Water Quality Index (WQI)** calculation for risk assessment

#### Model Parameters
- **Chloride as Cl**: 250 mg/L standard
- **Calcium (Total)**: 200 mg/L standard
- **Total Magnesium**: 150 mg/L standard
- **Sodium as Na**: 200 mg/L standard
- **Potassium as K**: 12 mg/L standard
- **Salinity as EC@25**: 500 μS/cm standard
- **pH**: 6.5-8.5 range

#### WQI Calculation
```python
def calculate_wqi(parameters):
    scores = []
    for param, value in parameters.items():
        if param in WQI_WEIGHTS:
            score = calculate_score(value, WQI_STANDARDS[param], param)
            scores.append(score * WQI_WEIGHTS[param])
    return sum(scores) / sum(WQI_WEIGHTS.values())
```

## 🗄️ Database Schema

### Water Sources Table
```sql
CREATE TABLE water_sources (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    status VARCHAR(50),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    lga VARCHAR(100),
    town VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Site Suburb Data Table
```sql
CREATE TABLE site_suburb_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    site_id VARCHAR(50),
    chloride_cl DECIMAL(10, 2),
    calcium_total DECIMAL(10, 2),
    magnesium_total DECIMAL(10, 2),
    sodium_na DECIMAL(10, 2),
    potassium_k DECIMAL(10, 2),
    salinity_ec DECIMAL(10, 2),
    ph_value DECIMAL(4, 2),
    value_date DATE,
    nearest_suburb VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_guidance_cache.py

# Run with coverage
python -m pytest --cov=api --cov-report=html
```

### Test Files
- `test_guidance_cache.py` - Guidance system caching tests
- `test_integration_guidance.py` - Integration tests for guidance API
- `test_llm_debug.py` - LLM integration debugging
- `test_simple.py` - Basic functionality tests
- `test_sources_implementation.py` - Water sources API tests

## 📈 Performance Optimization

### Caching Strategy
- **In-memory caching** for checklist responses (15-minute TTL)
- **Database query optimization** with proper indexing
- **Response compression** for large datasets

### Database Optimization
```sql
-- Indexes for better query performance
CREATE INDEX idx_water_sources_location ON water_sources(latitude, longitude);
CREATE INDEX idx_water_sources_status ON water_sources(status);
CREATE INDEX idx_site_data_site_date ON site_suburb_data(site_id, value_date);
```

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

- **API Documentation**: http://localhost:8000/docs
- **Issues**: [GitHub Issues](https://github.com/your-username/WaterSafe/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/WaterSafe/discussions)

---

<div align="center">
  <strong>Built with ❤️ using FastAPI</strong>
  <br>
  <em>High-performance water safety API</em>
</div>