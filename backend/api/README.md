# API Directory 🚀

This directory contains all the backend API endpoints for the WaterSafe application. These APIs handle data processing, AI guidance, and water quality predictions.

## 🎯 What's Inside

The API provides three main service areas:
- **Water Sources** - Location data and source management
- **Water Quality Prediction** - ML-powered quality analysis
- **AI Guidance** - Intelligent sanitation and hygiene recommendations

## 📁 Main API Modules

### 🗺️ Water Sources API (`water_sources.py`)
Manages water source data and location services:
- **Source Database** - All available water sources
- **Geographic Search** - Find sources by location and radius
- **Filtering** - Search by type, status, and area
- **Real-time Updates** - Current source availability

### 📊 Water Quality Prediction API (`water_quality_prediction.py`)
Provides machine learning predictions:
- **Quality Predictions** - Forecast water quality parameters
- **Risk Assessment** - Safety levels and recommendations
- **Site Management** - Historical data and trends
- **WQI Calculation** - Water Quality Index scoring

### 🤖 AI Guidance API (`guidance.py`)
Offers intelligent assistance:
- **Sanitation Checklists** - Personalized hygiene guidance
- **AI Chat Assistant** - Conversational support
- **Context Awareness** - Tailored recommendations
- **Emergency Procedures** - Crisis response guidance

## 🚀 API Features

### RESTful Design
- **Standard HTTP Methods** - GET, POST, PUT, DELETE
- **Clean URLs** - Intuitive endpoint structure
- **JSON Responses** - Consistent data format
- **Status Codes** - Proper HTTP response codes

### Performance Optimization
- **Caching** - 15-minute cache for AI responses
- **Pagination** - Efficient data retrieval
- **Database Indexing** - Fast query performance
- **Response Compression** - Reduced data transfer

### Error Handling
- **Validation** - Input data checking
- **Graceful Failures** - Fallback responses
- **Clear Messages** - User-friendly error descriptions
- **Logging** - Comprehensive error tracking

## 🔧 API Endpoints

### Water Sources
- `GET /api/water-sources/` - Get all water sources
- `GET /api/water-sources/nearby` - Find nearby sources
- `GET /api/water-sources/filter` - Filter by criteria
- `GET /api/water-sources/count` - Get total count

### Water Quality Prediction
- `POST /api/prediction/predict` - Predict water quality
- `GET /api/prediction/sites` - Get available sites
- `GET /api/prediction/suburbs` - Get available suburbs
- `POST /api/prediction/search-by-suburb` - Search by suburb

### AI Guidance
- `POST /api/guidance/checklist` - Generate sanitation checklist
- `POST /api/guidance/chat` - Chat with AI assistant
- `POST /api/guidance/explain` - Get item explanations

## 📱 Mobile Optimization

### Efficient Data Transfer
- **Minimal Payloads** - Only necessary data
- **Compression** - Reduced bandwidth usage
- **Caching** - Offline data availability
- **Batch Requests** - Multiple operations in one call

### Real-time Features
- **Live Updates** - Real-time data synchronization
- **Push Notifications** - Important alerts
- **Background Sync** - Data updates when offline
- **Location Services** - GPS integration

## 🔒 Security Features

### Data Protection
- **Input Validation** - Sanitize all user inputs
- **SQL Injection Prevention** - Safe database queries
- **CORS Configuration** - Cross-origin request control
- **Rate Limiting** - Prevent abuse and overload

### Authentication
- **API Keys** - Secure access control
- **Token Validation** - Verify user permissions
- **Session Management** - Secure user sessions
- **Audit Logging** - Track API usage

## 🧪 API Testing

### Quality Assurance
- **Unit Tests** - Individual endpoint testing
- **Integration Tests** - End-to-end functionality
- **Performance Tests** - Load and stress testing
- **Security Tests** - Vulnerability assessment

### Monitoring
- **Response Times** - Track API performance
- **Error Rates** - Monitor failure frequency
- **Usage Analytics** - Understand API usage patterns
- **Health Checks** - System status monitoring

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI** - Available at `/docs` endpoint
- **ReDoc** - Alternative documentation at `/redoc`
- **OpenAPI Spec** - Machine-readable API specification
- **Examples** - Sample requests and responses

### Developer Resources
- **Getting Started Guide** - Quick setup instructions
- **Authentication Guide** - How to use API keys
- **Rate Limits** - Usage guidelines and limits
- **Error Codes** - Complete error reference

## 🔄 API Versioning

### Version Management
- **Backward Compatibility** - Support older versions
- **Deprecation Notices** - Advance warning of changes
- **Migration Guides** - Help with version upgrades
- **Feature Flags** - Gradual feature rollouts

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [API Security Guidelines](https://owasp.org/www-project-api-security/)

---

<div align="center">
  <strong>Backend APIs for WaterSafe</strong>
  <br>
  <em>RESTful services for water safety data</em>
</div>
