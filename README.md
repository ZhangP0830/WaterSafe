# WaterSafe 

[![Live Demo](https://img.shields.io/badge/Live%20Demo-water--safety.netlify.app-blue?style=for-the-badge&logo=netlify)](https://water-safety-guard.netlify.app/)
[![Frontend](https://img.shields.io/badge/Frontend-Vue.js%203-4FC08D?style=for-the-badge&logo=vue.js)](https://vuejs.org/)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Database](https://img.shields.io/badge/Database-MySQL-4479A1?style=for-the-badge&logo=mysql)](https://mysql.com/)

> A comprehensive water safety awareness and trusted alternatives finder application designed to help communities access safe water sources and receive personalized guidance during water quality issues.

## 🎯 Overview

WaterSafe is a comprehensive water safety platform that protects families from water contamination risks. The application provides personalized guidance for hydration, nutrition, hygiene, and health monitoring during water safety disruptions, with special focus on pregnant women and infants.

### 🌟 Key Features

- **🛡️ Maternal & Infant Health Shield**: Comprehensive protection combining hydration, nutrition, hygiene, and health support
- **💧 Hydration Safety Hub**: Daily safe water intake guidance tailored for pregnancy and infant formula preparation
- **🍼 Feeding & Tracking**: Mother's hydration tracker and infant feeding/hydration schedule with offline capabilities
- **🔍 Symptom Checker**: AI-powered tool to guide mothers when noticing early symptoms in themselves or their infant
- **🧼 Sanitation Support**: Practical checklists for handwashing, safe surfaces, and waste handling during disruptions
- **🚨 Emergency First-Response**: Immediate "what to do" cards for contamination, illness, or dehydration situations
- **📊 Water Quality Prediction**: AI-powered predictions for water quality parameters using machine learning models
- **🗺️ Trusted Alternatives**: Interactive map showing nearby safe water sources with status updates
- **📱 Responsive Design**: Modern, mobile-first interface built with Vue.js and Material Design

## 🏗️ Architecture

```
WaterSafe/
├── 📁 Frontend (Vue.js 3)
│   ├── 🎨 Material Design Components
│   ├── 🗺️ Interactive Maps (Google Maps)
│   ├── 📱 Responsive UI/UX
│   └── 🔄 Real-time Data Integration
├── 📁 Backend (FastAPI)
│   ├── 🚀 RESTful API Endpoints
│   ├── 🤖 AI/ML Integration
│   ├── 🗄️ Database Management
│   └── 📊 Water Quality Prediction Models
└── 📁 Data & Models
    ├── 📈 Historical Water Quality Data
    ├── 🧠 Trained ML Models
    └── 📍 Geographic Data
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** 16+ 
- **Python** 3.8+
- **MySQL** 8.0+
- **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/ZhangP0830/WaterSafe.git
cd WaterSafe
```

### 2. Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```
🌐 Frontend will be available at: http://localhost:5173

### 3. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database and API credentials

# Start backend server
python main.py
```
🔧 Backend will be available at: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs

## 🛠️ Technology Stack

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Fast build tool and dev server
- **Material Kit Pro** - Premium UI components
- **Google Maps API** - Interactive mapping
- **Pinia** - State management
- **Vue Router** - Client-side routing

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **MySQL** - Relational database
- **OpenAI API** - AI-powered guidance
- **Pandas & NumPy** - Data processing
- **Uvicorn** - ASGI server

### DevOps & Deployment
- **Netlify** - Frontend hosting
- **Vercel** - Alternative deployment
- **GitHub Actions** - CI/CD pipeline


## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
npm run test
```

## 📈 Performance

- **Frontend**: Lighthouse score 95+
- **Backend**: < 200ms average response time
- **Database**: Optimized queries with indexing
- **Caching**: Redis integration for improved performance

## 🔒 Security

- **CORS** configuration for cross-origin requests
- **Input validation** with Pydantic models
- **SQL injection** prevention with SQLAlchemy ORM
- **API rate limiting** and authentication
- **Environment variables** for sensitive data

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributors

### Core Team
- **Peng Zhang** - *Full-Stack Developer* - [GitHub](https://github.com/ZhangP0830)
- **Nithesh Reddy** - *AI Engineer & Full-Stack Developer* - [GitHub](https://github.com/Nryreddy)
- **Amrit Jain** - *Cyber security & Quality Assurance*
- **Bohan Zhou** - *Data Scientist* 
- **Haohao Tang** - *Data Scientist* 
- **Jianyao Qian** - *Business analyst* 

### Special Thanks
- **Monash University** - Academic supervision and guidance
- **Open Source Community** - Libraries and tools that made this possible

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ZhangP0830/WaterSafe/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ZhangP0830/WaterSafe/discussions)

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Core water source discovery
- ✅ Basic water quality prediction
- ✅ AI guidance system
- ✅ Responsive web interface

### Phase 2 (Future)
- 🔄 Mobile app development
- 🔄 Real-time notifications
- 🔄 IoT sensor integration
- 🔄 Government agency integration

---

<div align="center">
  <strong>Made with ❤️ for water safety awareness</strong>
  <br>
  <em>Empowering communities through technology</em>
</div>
