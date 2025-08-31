# WaterSafe Backend

Python + FastAPI backend service

## Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start Backend

```bash
# Local development
python main.py

# With custom host/port
HOST=127.0.0.1 PORT=8000 python main.py

# Server deployment
HOST=0.0.0.0 PORT=8000 python main.py
```

Service will be available at: http://localhost:8000

## Environment Variables

Copy `env.example` to `.env` and update the values:

```bash
cp env.example .env
# Edit .env file with your configuration
```
