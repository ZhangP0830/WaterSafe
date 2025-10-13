"""
Test configuration and fixtures for WaterSafe backend tests
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import json
import os
from datetime import datetime, timedelta

# Import the FastAPI app
from main import app

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)

@pytest.fixture
def mock_database():
    """Mock database connection and operations"""
    with patch('database.engine') as mock_engine:
        mock_engine.connect.return_value.__enter__.return_value = Mock()
        yield mock_engine

@pytest.fixture
def mock_model_parameters():
    """Mock model parameters data"""
    return {
        ' "site_001"': {
            'Chloride as Cl': {
                'method': 'linear_regression',
                'coef': [0.1, 10.0]
            },
            'Calcium (Total)': {
                'method': 'repeat_last',
                'coef': [0.0, 0.0]
            },
            'Total Magnesium': {
                'method': 'linear_regression',
                'coef': [0.05, 5.0]
            },
            'Sodium as Na': {
                'method': 'repeat_last',
                'coef': [0.0, 0.0]
            },
            'Potassium as K': {
                'method': 'linear_regression',
                'coef': [0.02, 2.0]
            },
            'Salinity as EC@25 (lab)': {
                'method': 'linear_regression',
                'coef': [0.3, 30.0]
            },
            'pH': {
                'method': 'repeat_last',
                'coef': [0.0, 0.0]
            }
        }
    }

@pytest.fixture
def mock_site_data():
    """Mock site data from database"""
    return pd.DataFrame({
        'site_id': ['site_001', 'site_001', 'site_001'],
        'Chloride as Cl': [15.0, 16.0, 17.0],
        'Calcium (Total)': [45.0, 46.0, 47.0],
        'Total Magnesium': [8.0, 8.5, 9.0],
        'Sodium as Na': [25.0, 26.0, 27.0],
        'Potassium as K': [3.0, 3.2, 3.4],
        'Salinity as EC@25 (lab)': [180.0, 185.0, 190.0],
        'Date': [
            datetime.now() - timedelta(days=60),
            datetime.now() - timedelta(days=30),
            datetime.now() - timedelta(days=1)
        ],
        'pH': [7.2, 7.3, 7.4],
        'Site ID': [' "site_001"', ' "site_001"', ' "site_001"']
    })

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    return {
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "summary_top3": [
                            {
                                "title": "Wash hands frequently",
                                "why": "Prevents spread of germs",
                                "priority": "critical",
                                "badges": ["Essential"],
                                "sources": [{"label": "WHO", "url": "https://www.who.int/health-topics/water-sanitation-and-hygiene-wash"}]
                            }
                        ],
                        "sections": [
                            {
                                "name": "Hand Hygiene",
                                "items": [
                                    {
                                        "id": "hand-wash",
                                        "title": "Wash hands with soap",
                                        "body": "Use soap and water for 20 seconds",
                                        "icons": ["🧼"],
                                        "actions": ["Wet hands", "Apply soap", "Scrub", "Rinse"],
                                        "priority": "critical",
                                        "sources": [{"label": "WHO", "url": "https://www.who.int/health-topics/water-sanitation-and-hygiene-wash"}]
                                    }
                                ]
                            }
                        ],
                        "notes": [
                            {
                                "type": "general",
                                "text": "Always check local health guidance"
                            }
                        ],
                        "sources": [
                            {"label": "WHO WASH Guidelines", "url": "https://www.who.int/health-topics/water-sanitation-and-hygiene-wash"}
                        ]
                    })
                }
            }
        ]
    }

@pytest.fixture
def sample_prediction_request():
    """Sample prediction request data"""
    return {
        "site_id": "site_001"
    }

@pytest.fixture
def sample_sanitation_request():
    """Sample sanitation request data"""
    return {
        "mode": "general",
        "place": "home",
        "profile": {
            "pregnant": True,
            "infant": False
        },
        "issues": ["no_running_water"]
    }

@pytest.fixture
def sample_suburb_search_request():
    """Sample suburb search request data"""
    return {
        "suburb_name": "Melbourne"
    }

@pytest.fixture
def mock_available_sites():
    """Mock available sites data"""
    return ["site_001", "site_002", "site_003"]

@pytest.fixture
def mock_available_suburbs():
    """Mock available suburbs data"""
    return [
        {"nearest_suburb": "Melbourne", "site_count": 5},
        {"nearest_suburb": "Sydney", "site_count": 3},
        {"nearest_suburb": "Brisbane", "site_count": 2}
    ]

@pytest.fixture
def mock_suburb_search_results():
    """Mock suburb search results"""
    return [
        {"site_id": "site_001", "nearest_suburb": "Melbourne"},
        {"site_id": "site_002", "nearest_suburb": "Melbourne"}
    ]

# Environment variable mocks
@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test-api-key',
        'OPENAI_MODEL': 'gpt-4o-mini-2024-07-18',
        'HOST': '0.0.0.0',
        'PORT': '8000'
    }):
        yield
