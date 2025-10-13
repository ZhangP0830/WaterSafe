"""
Test cases for water quality prediction API
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, MagicMock
import pandas as pd
import json
from datetime import datetime, timedelta

class TestWaterQualityPrediction:
    """Test cases for water quality prediction functionality"""

    def test_prediction_request_model(self, sample_prediction_request):
        """TC-BE-016: Test prediction request model validation"""
        from api.water_quality_prediction import PredictionRequest
        
        # Test valid request
        request = PredictionRequest(**sample_prediction_request)
        assert request.site_id == "site_001"
        
        # Test invalid request (missing site_id)
        with pytest.raises(ValueError):
            PredictionRequest()

    def test_suburb_search_request_model(self, sample_suburb_search_request):
        """TC-BE-017: Test suburb search request model validation"""
        from api.water_quality_prediction import SuburbSearchRequest
        
        # Test valid request
        request = SuburbSearchRequest(**sample_suburb_search_request)
        assert request.suburb_name == "Melbourne"
        
        # Test invalid request (missing suburb_name)
        with pytest.raises(ValueError):
            SuburbSearchRequest()

    def test_prediction_response_model(self):
        """TC-BE-018: Test prediction response model structure"""
        from api.water_quality_prediction import PredictionResponse
        
        # Test valid response
        response_data = {
            "site_id": "site_001",
            "prediction_date": "2024-01-15",
            "parameters": {
                "Chloride as Cl": 15.0,
                "Calcium (Total)": 45.0,
                "pH": 7.2
            },
            "wqi_score": 85.5,
            "risk_level": "Safe",
            "recommendations": ["Water quality is safe for drinking"]
        }
        
        response = PredictionResponse(**response_data)
        assert response.site_id == "site_001"
        assert response.wqi_score == 85.5
        assert response.risk_level == "Safe"

    @patch('api.water_quality_prediction.load_model_parameters')
    def test_load_model_parameters_success(self, mock_load, mock_model_parameters):
        """TC-BE-019: Test successful model parameters loading"""
        from api.water_quality_prediction import load_model_parameters
        
        mock_load.return_value = mock_model_parameters
        result = load_model_parameters()
        
        assert result == mock_model_parameters
        assert ' "site_001"' in result

    @patch('api.water_quality_prediction.load_model_parameters')
    def test_load_model_parameters_file_not_found(self, mock_load):
        """TC-BE-020: Test model parameters file not found error"""
        from api.water_quality_prediction import load_model_parameters
        from fastapi import HTTPException
        
        mock_load.side_effect = FileNotFoundError("File not found")
        
        with pytest.raises(HTTPException) as exc_info:
            load_model_parameters()
        
        assert exc_info.value.status_code == 500
        assert "Model parameters file not found" in str(exc_info.value.detail)

    @patch('api.water_quality_prediction.pd.read_sql')
    def test_load_site_data_success(self, mock_read_sql, mock_site_data):
        """TC-BE-021: Test successful site data loading"""
        from api.water_quality_prediction import load_site_data
        
        mock_read_sql.return_value = mock_site_data
        result = load_site_data()
        
        assert len(result) == 3
        assert 'site_id' in result.columns
        assert 'Chloride as Cl' in result.columns

    @patch('api.water_quality_prediction.pd.read_sql')
    def test_load_site_data_database_error(self, mock_read_sql):
        """TC-BE-022: Test database error handling in site data loading"""
        from api.water_quality_prediction import load_site_data
        from fastapi import HTTPException
        
        mock_read_sql.side_effect = Exception("Database connection failed")
        
        with pytest.raises(HTTPException) as exc_info:
            load_site_data()
        
        assert exc_info.value.status_code == 500
        assert "Database query failed" in str(exc_info.value.detail)

    @patch('api.water_quality_prediction.pd.read_sql')
    def test_get_site_data_success(self, mock_read_sql, mock_site_data):
        """TC-BE-023: Test successful site-specific data retrieval"""
        from api.water_quality_prediction import get_site_data
        
        mock_read_sql.return_value = mock_site_data
        result = get_site_data("site_001")
        
        assert result is not None
        assert len(result) == 3
        assert all(result['site_id'] == 'site_001')

    @patch('api.water_quality_prediction.pd.read_sql')
    def test_get_site_data_no_data(self, mock_read_sql):
        """TC-BE-024: Test site data retrieval when no data exists"""
        from api.water_quality_prediction import get_site_data
        
        mock_read_sql.return_value = pd.DataFrame()
        result = get_site_data("nonexistent_site")
        
        assert result is None

    @patch('api.water_quality_prediction.pd.read_sql')
    def test_get_available_sites_success(self, mock_read_sql, mock_available_sites):
        """TC-BE-025: Test successful available sites retrieval"""
        from api.water_quality_prediction import get_available_sites
        
        mock_df = pd.DataFrame({'site_id': mock_available_sites})
        mock_read_sql.return_value = mock_df
        
        result = get_available_sites()
        
        assert result == mock_available_sites
        assert len(result) == 3

    @patch('api.water_quality_prediction.pd.read_sql')
    def test_get_available_sites_error(self, mock_read_sql):
        """TC-BE-026: Test error handling in available sites retrieval"""
        from api.water_quality_prediction import get_available_sites
        
        mock_read_sql.side_effect = Exception("Database error")
        result = get_available_sites()
        
        assert result == []

    def test_calculate_score_ph_normal(self):
        """TC-BE-027: Test pH score calculation for normal range"""
        from api.water_quality_prediction import calculate_score
        
        # Test pH in normal range (6.5-8.5)
        score = calculate_score(7.0, (6.5, 8.5), 'pH')
        assert score == 100

    def test_calculate_score_ph_abnormal(self):
        """TC-BE-028: Test pH score calculation for abnormal range"""
        from api.water_quality_prediction import calculate_score
        
        # Test pH outside normal range
        score = calculate_score(5.0, (6.5, 8.5), 'pH')
        assert score == 0

    def test_calculate_score_other_parameters(self):
        """TC-BE-029: Test score calculation for other parameters"""
        from api.water_quality_prediction import calculate_score
        
        # Test chloride score calculation
        score = calculate_score(100.0, 250, 'Chloride as Cl')
        assert score == 60.0  # 100 - (100/250 * 100)

    def test_calculate_score_nan_value(self):
        """TC-BE-030: Test score calculation for NaN values"""
        from api.water_quality_prediction import calculate_score
        import pandas as pd
        
        score = calculate_score(pd.NA, 250, 'Chloride as Cl')
        assert score == 0

    def test_calculate_wqi_success(self):
        """TC-BE-031: Test WQI calculation with valid parameters"""
        from api.water_quality_prediction import calculate_wqi
        
        parameters = {
            'Chloride as Cl': 100.0,
            'Calcium (Total)': 50.0,
            'Total Magnesium': 30.0,
            'Sodium as Na': 80.0,
            'Potassium as K': 5.0,
            'Salinity as EC@25 (lab)': 200.0,
            'pH': 7.0
        }
        
        wqi = calculate_wqi(parameters)
        assert isinstance(wqi, float)
        assert 0 <= wqi <= 100

    def test_calculate_wqi_empty_parameters(self):
        """TC-BE-032: Test WQI calculation with empty parameters"""
        from api.water_quality_prediction import calculate_wqi
        
        wqi = calculate_wqi({})
        assert wqi == 0

    def test_get_risk_level_safe(self):
        """TC-BE-033: Test risk level determination for safe water"""
        from api.water_quality_prediction import get_risk_level
        
        risk_level = get_risk_level(85.0)
        assert risk_level == "Safe"

    def test_get_risk_level_moderate(self):
        """TC-BE-034: Test risk level determination for moderate risk"""
        from api.water_quality_prediction import get_risk_level
        
        risk_level = get_risk_level(60.0)
        assert risk_level == "Moderate"

    def test_get_risk_level_unsafe(self):
        """TC-BE-035: Test risk level determination for unsafe water"""
        from api.water_quality_prediction import get_risk_level
        
        risk_level = get_risk_level(30.0)
        assert risk_level == "Unsafe"

    def test_get_recommendations_safe(self):
        """TC-BE-036: Test recommendations for safe water"""
        from api.water_quality_prediction import get_recommendations
        
        parameters = {'pH': 7.0, 'Salinity as EC@25 (lab)': 300.0}
        recommendations = get_recommendations("Safe", parameters)
        
        assert "Water quality is safe for drinking" in recommendations
        assert "Continue regular monitoring" in recommendations

    def test_get_recommendations_unsafe_ph(self):
        """TC-BE-037: Test recommendations for unsafe pH"""
        from api.water_quality_prediction import get_recommendations
        
        parameters = {'pH': 5.0, 'Salinity as EC@25 (lab)': 300.0}
        recommendations = get_recommendations("Unsafe", parameters)
        
        assert any("pH level outside optimal range" in rec for rec in recommendations)

    def test_get_recommendations_high_salinity(self):
        """TC-BE-038: Test recommendations for high salinity"""
        from api.water_quality_prediction import get_recommendations
        
        parameters = {'pH': 7.0, 'Salinity as EC@25 (lab)': 600.0}
        recommendations = get_recommendations("Moderate", parameters)
        
        assert any("High salinity detected" in rec for rec in recommendations)

    @patch('api.water_quality_prediction.load_model_parameters')
    @patch('api.water_quality_prediction.get_site_data')
    def test_predict_water_quality_success(self, mock_get_site_data, mock_load_model, 
                                         mock_model_parameters, mock_site_data):
        """TC-BE-039: Test successful water quality prediction"""
        from api.water_quality_prediction import predict_water_quality
        
        mock_load_model.return_value = mock_model_parameters
        mock_get_site_data.return_value = mock_site_data
        
        result = predict_water_quality("site_001")
        
        assert result["site_id"] == "site_001"
        assert "prediction_date" in result
        assert "parameters" in result
        assert "wqi_score" in result
        assert "risk_level" in result
        assert "recommendations" in result

    @patch('api.water_quality_prediction.load_model_parameters')
    def test_predict_water_quality_site_not_found(self, mock_load_model, mock_model_parameters):
        """TC-BE-040: Test water quality prediction for non-existent site"""
        from api.water_quality_prediction import predict_water_quality
        from fastapi import HTTPException
        
        mock_load_model.return_value = mock_model_parameters
        
        with pytest.raises(HTTPException) as exc_info:
            predict_water_quality("nonexistent_site")
        
        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail)

    @patch('api.water_quality_prediction.load_model_parameters')
    @patch('api.water_quality_prediction.get_site_data')
    def test_predict_water_quality_no_historical_data(self, mock_get_site_data, 
                                                    mock_load_model, mock_model_parameters):
        """TC-BE-041: Test water quality prediction with no historical data"""
        from api.water_quality_prediction import predict_water_quality
        from fastapi import HTTPException
        
        mock_load_model.return_value = mock_model_parameters
        mock_get_site_data.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            predict_water_quality("site_001")
        
        assert exc_info.value.status_code == 404
        assert "No historical data found" in str(exc_info.value.detail)

    def test_predict_water_quality_api_endpoint(self, client, sample_prediction_request):
        """TC-BE-042: Test prediction API endpoint"""
        with patch('api.water_quality_prediction.predict_water_quality') as mock_predict:
            mock_predict.return_value = {
                "site_id": "site_001",
                "prediction_date": "2024-01-15",
                "parameters": {"pH": 7.0},
                "wqi_score": 85.0,
                "risk_level": "Safe",
                "recommendations": ["Water is safe"]
            }
            
            response = client.post("/api/prediction/predict", json=sample_prediction_request)
            
            assert response.status_code == 200
            data = response.json()
            assert data["site_id"] == "site_001"
            assert data["wqi_score"] == 85.0

    def test_get_available_sites_api_endpoint(self, client, mock_available_sites):
        """TC-BE-043: Test available sites API endpoint"""
        with patch('api.water_quality_prediction.get_available_sites') as mock_get_sites:
            mock_get_sites.return_value = mock_available_sites
            
            response = client.get("/api/prediction/sites")
            
            assert response.status_code == 200
            data = response.json()
            assert "total_sites" in data
            assert "sites" in data
            assert data["total_sites"] == 3

    def test_get_available_suburbs_api_endpoint(self, client, mock_available_suburbs):
        """TC-BE-044: Test available suburbs API endpoint"""
        with patch('api.water_quality_prediction.get_available_suburbs') as mock_get_suburbs:
            mock_get_suburbs.return_value = mock_available_suburbs
            
            response = client.get("/api/prediction/suburbs")
            
            assert response.status_code == 200
            data = response.json()
            assert "total_suburbs" in data
            assert "suburbs" in data
            assert data["total_suburbs"] == 3

    def test_search_sites_by_suburb_api_endpoint(self, client, sample_suburb_search_request, 
                                               mock_suburb_search_results):
        """TC-BE-045: Test suburb search API endpoint"""
        with patch('api.water_quality_prediction.search_sites_by_suburb') as mock_search:
            mock_search.return_value = mock_suburb_search_results
            
            response = client.post("/api/prediction/search-by-suburb", 
                                 json=sample_suburb_search_request)
            
            assert response.status_code == 200
            data = response.json()
            assert "suburb_name" in data
            assert "total_sites" in data
            assert data["total_sites"] == 2

    def test_prediction_health_check_endpoint(self, client):
        """TC-BE-046: Test prediction API health check endpoint"""
        with patch('api.water_quality_prediction.load_model_parameters') as mock_load_model, \
             patch('api.water_quality_prediction.get_available_sites') as mock_get_sites:
            
            mock_load_model.return_value = {"site_001": {}}
            mock_get_sites.return_value = ["site_001", "site_002"]
            
            response = client.get("/api/prediction/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["model_loaded"] is True
            assert data["database_connected"] is True

    def test_prediction_health_check_unhealthy(self, client):
        """TC-BE-047: Test prediction API health check when unhealthy"""
        with patch('api.water_quality_prediction.load_model_parameters') as mock_load_model:
            mock_load_model.side_effect = Exception("Model loading failed")
            
            response = client.get("/api/prediction/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "unhealthy"
            assert data["model_loaded"] is False
            assert data["database_connected"] is False
