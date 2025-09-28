# WaterSafe Deployment Guide 🚀

This guide provides comprehensive instructions for deploying the WaterSafe application in various environments.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Frontend Deployment](#frontend-deployment)
- [Backend Deployment](#backend-deployment)
- [Database Setup](#database-setup)
- [Environment Configuration](#environment-configuration)
- [Production Deployment](#production-deployment)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### System Requirements
- **Node.js** 16+ (for frontend)
- **Python** 3.8+ (for backend)
- **MySQL** 8.0+ (for database)
- **Git** (for version control)

### External Services
- **OpenAI API Key** (for AI guidance features)
- **Google Maps API Key** (for mapping features)
- **Domain name** (for production deployment)

## 🎨 Frontend Deployment

### Netlify Deployment (Recommended)

1. **Build the Frontend**
```bash
# Install dependencies
npm install

# Build for production
npm run build
```

2. **Deploy to Netlify**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy
netlify deploy --prod --dir=dist
```

3. **Configure Environment Variables**
In Netlify dashboard, add:
```
VITE_API_BASE_URL=https://your-backend-api.com
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_key
```

### Vercel Deployment (Alternative)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy**
```bash
vercel --prod
```

3. **Configure Environment Variables**
In Vercel dashboard, add the same environment variables as Netlify.

### Manual Deployment

1. **Build the Application**
```bash
npm run build
```

2. **Upload to Web Server**
Upload the `dist/` folder contents to your web server's public directory.

3. **Configure Web Server**
Ensure your web server serves the `index.html` file for all routes (SPA routing).

## 🚀 Backend Deployment

### Docker Deployment (Recommended)

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and Run**
```bash
# Build Docker image
docker build -t watersafe-backend .

# Run container
docker run -p 8000:8000 --env-file .env watersafe-backend
```

### Cloud Platform Deployment

#### Heroku
1. **Create Procfile**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. **Deploy**
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create watersafe-backend

# Set environment variables
heroku config:set DATABASE_URL=your_database_url
heroku config:set OPENAI_API_KEY=your_openai_key

# Deploy
git push heroku main
```

#### Railway
1. **Connect Repository**
- Connect your GitHub repository to Railway
- Railway will automatically detect the Python project

2. **Configure Environment Variables**
- Add all required environment variables in Railway dashboard

3. **Deploy**
- Railway will automatically build and deploy on every push

#### DigitalOcean App Platform
1. **Create App**
- Create a new app in DigitalOcean App Platform
- Connect your GitHub repository

2. **Configure Build Settings**
- Build command: `pip install -r requirements.txt`
- Run command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
- Add all required environment variables

## 🗄️ Database Setup

### MySQL Setup

1. **Install MySQL**
```bash
# Ubuntu/Debian
sudo apt-get install mysql-server

# macOS
brew install mysql

# Windows
# Download from MySQL website
```

2. **Create Database**
```sql
CREATE DATABASE watersafe;
CREATE USER 'watersafe_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON watersafe.* TO 'watersafe_user'@'localhost';
FLUSH PRIVILEGES;
```

3. **Import Data**
```bash
# Import water sources data
mysql -u watersafe_user -p watersafe < water_sources.sql

# Import site data
mysql -u watersafe_user -p watersafe < site_suburb_data.sql
```

### Cloud Database Options

#### PlanetScale
1. Create a new database in PlanetScale
2. Get the connection string
3. Update your environment variables

#### AWS RDS
1. Create a MySQL RDS instance
2. Configure security groups
3. Get the connection endpoint
4. Update your environment variables

## ⚙️ Environment Configuration

### Production Environment Variables

```env
# Database
DATABASE_URL=mysql+pymysql://user:password@host:port/database
DB_HOST=your-db-host
DB_PORT=3306
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=watersafe

# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False
ENVIRONMENT=production

# CORS
ALLOWED_ORIGINS=https://water-safety.netlify.app,https://your-domain.com

# Security
SECRET_KEY=your_very_secure_secret_key
JWT_SECRET_KEY=your_jwt_secret_key

# External APIs
GOOGLE_MAPS_API_KEY=your_google_maps_key
```

## 🔒 Production Security

### SSL/TLS Configuration
- Use HTTPS for all production deployments
- Configure SSL certificates (Let's Encrypt recommended)
- Enable HSTS headers

### Security Headers
```python
# Add to FastAPI app
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["your-domain.com", "*.your-domain.com"]
)
```

### Database Security
- Use strong passwords
- Enable SSL connections
- Restrict database access by IP
- Regular security updates

## 📊 Monitoring and Maintenance

### Health Checks
- Set up health check endpoints
- Monitor API response times
- Track error rates
- Monitor database performance

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Backup Strategy
- Regular database backups
- Code repository backups
- Environment configuration backups
- Test restore procedures

## 🔧 Troubleshooting

### Common Issues

#### Frontend Build Failures
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### Backend Connection Issues
- Check database connection string
- Verify environment variables
- Check firewall settings
- Test database connectivity

#### API CORS Issues
- Verify CORS configuration
- Check allowed origins
- Ensure proper headers

### Performance Issues
- Monitor database query performance
- Check API response times
- Optimize frontend bundle size
- Use CDN for static assets

### Debug Mode
```bash
# Enable debug mode for development
export DEBUG=True
export LOG_LEVEL=DEBUG
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancers
- Implement database read replicas
- Use Redis for caching
- Consider microservices architecture

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Use connection pooling
- Implement caching strategies

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v1.2
        with:
          publish-dir: './dist'
          production-branch: main
          github-token: ${{ secrets.GITHUB_TOKEN }}
          deploy-message: "Deploy from GitHub Actions"
```

## 📞 Support

For deployment issues:
- Check the logs for error messages
- Verify environment variables
- Test locally first
- Contact the development team

---

<div align="center">
  <strong>Deploy with Confidence</strong>
  <br>
  <em>WaterSafe Deployment Guide</em>
</div>
