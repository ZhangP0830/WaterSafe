"""
Integration tests for WaterSafe backend
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock, MagicMock
import pandas as pd
import json

class TestIntegration:
    """Integration tests for backend functionality"""

    def test_full_prediction_workflow(self, client, mock_model_parameters, mock_site_data):
        """TC-BE-096: Test complete water quality prediction workflow"""
        with patch('api.water_quality_prediction.load_model_parameters') as mock_load_model, \
             patch('api.water_quality_prediction.get_site_data') as mock_get_site_data:
            
            mock_load_model.return_value = mock_model_parameters
            mock_get_site_data.return_value = mock_site_data
            
            # Test prediction request
            request_data = {"site_id": "site_001"}
            response = client.post("/api/prediction/predict", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            
            # Verify response structure
            assert "site_id" in data
            assert "prediction_date" in data
            assert "parameters" in data
            assert "wqi_score" in data
            assert "risk_level" in data
            assert "recommendations" in data
            
            # Verify data types
            assert isinstance(data["wqi_score"], (int, float))
            assert data["risk_level"] in ["Safe", "Moderate", "Unsafe"]
            assert isinstance(data["recommendations"], list)

    def test_full_guidance_workflow(self, client, sample_sanitation_request):
        """TC-BE-097: Test complete guidance generation workflow"""
        with patch('api.guidance._generate_llm_checklist') as mock_generate:
            from api.guidance import ChecklistResponse, ChecklistItem, ChecklistSection, ChecklistNote, ChecklistSource
            
            mock_item = ChecklistItem(
                title="Wash hands frequently",
                body="Use soap and water for 20 seconds",
                priority="critical",
                sources=[ChecklistSource(label="WHO", url="https://www.who.int")]
            )
            
            mock_section = ChecklistSection(name="Hand Hygiene", items=[mock_item])
            mock_note = ChecklistNote(type="general", text="Always check local guidance")
            mock_source = ChecklistSource(label="WHO WASH", url="https://www.who.int")
            
            mock_response = ChecklistResponse(
                summary_top3=[mock_item],
                sections=[mock_section],
                notes=[mock_note],
                sources=[mock_source]
            )
            
            mock_generate.return_value = mock_response
            
            # Test checklist generation
            response = client.post("/api/guidance/checklist", json=sample_sanitation_request)
            
            assert response.status_code == 200
            data = response.json()
            
            # Verify response structure
            assert "summary_top3" in data
            assert "sections" in data
            assert "notes" in data
            assert "sources" in data
            
            # Verify data content
            assert len(data["summary_top3"]) > 0
            assert len(data["sections"]) > 0
            assert len(data["notes"]) > 0
            assert len(data["sources"]) > 0

    def test_prediction_to_guidance_integration(self, client, mock_model_parameters, mock_site_data):
        """TC-BE-098: Test integration between prediction and guidance systems"""
        with patch('api.water_quality_prediction.load_model_parameters') as mock_load_model, \
             patch('api.water_quality_prediction.get_site_data') as mock_get_site_data, \
             patch('api.guidance._generate_llm_checklist') as mock_generate:
            
            # Setup prediction mocks
            mock_load_model.return_value = mock_model_parameters
            mock_get_site_data.return_value = mock_site_data
            
            # Setup guidance mocks
            from api.guidance import ChecklistResponse, ChecklistItem, ChecklistSection, ChecklistNote, ChecklistSource
            
            mock_item = ChecklistItem(
                title="Monitor water quality",
                body="Check WQI score regularly",
                priority="high"
            )
            
            mock_response = ChecklistResponse(
                summary_top3=[mock_item],
                sections=[ChecklistSection(name="Monitoring", items=[mock_item])],
                notes=[ChecklistNote(type="general", text="Based on prediction results")],
                sources=[ChecklistSource(label="WaterSafe", url="https://watersafe.com")]
            )
            
            mock_generate.return_value = mock_response
            
            # Test prediction
            prediction_request = {"site_id": "site_001"}
            prediction_response = client.post("/api/prediction/predict", json=prediction_request)
            assert prediction_response.status_code == 200
            
            # Test guidance based on prediction results
            guidance_request = {
                "mode": "general",
                "place": "home",
                "profile": {"pregnant": False, "infant": False},
                "issues": []
            }
            guidance_response = client.post("/api/guidance/checklist", json=guidance_request)
            assert guidance_response.status_code == 200
            
            # Verify both systems work together
            prediction_data = prediction_response.json()
            guidance_data = guidance_response.json()
            
            assert prediction_data["site_id"] == "site_001"
            assert len(guidance_data["summary_top3"]) > 0

    def test_database_to_prediction_integration(self, client, mock_available_sites, mock_available_suburbs):
        """TC-BE-099: Test database integration with prediction system"""
        with patch('api.water_quality_prediction.get_available_sites') as mock_get_sites, \
             patch('api.water_quality_prediction.get_available_suburbs') as mock_get_suburbs:
            
            mock_get_sites.return_value = mock_available_sites
            mock_get_suburbs.return_value = mock_available_suburbs
            
            # Test available sites endpoint
            sites_response = client.get("/api/prediction/sites")
            assert sites_response.status_code == 200
            sites_data = sites_response.json()
            assert sites_data["total_sites"] == 3
            
            # Test available suburbs endpoint
            suburbs_response = client.get("/api/prediction/suburbs")
            assert suburbs_response.status_code == 200
            suburbs_data = suburbs_response.json()
            assert suburbs_data["total_suburbs"] == 3

    def test_suburb_search_integration(self, client, mock_suburb_search_results):
        """TC-BE-100: Test suburb search integration"""
        with patch('api.water_quality_prediction.search_sites_by_suburb') as mock_search:
            mock_search.return_value = mock_suburb_search_results
            
            # Test suburb search
            search_request = {"suburb_name": "Melbourne"}
            response = client.post("/api/prediction/search-by-suburb", json=search_request)
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["suburb_name"] == "Melbourne"
            assert data["total_sites"] == 2
            assert len(data["sites"]) == 2
            assert data["sites"][0]["site_id"] == "site_001"

    def test_error_handling_integration(self, client):
        """TC-BE-101: Test error handling across integrated systems"""
        # Test prediction with invalid site
        with patch('api.water_quality_prediction.load_model_parameters') as mock_load_model:
            mock_load_model.return_value = {}
            
            request_data = {"site_id": "invalid_site"}
            response = client.post("/api/prediction/predict", json=request_data)
            
            assert response.status_code == 404
            assert "not found" in response.json()["detail"]

    def test_guidance_caching_integration(self, client, sample_sanitation_request):
        """TC-BE-102: Test guidance caching integration"""
        with patch('api.guidance._generate_llm_checklist') as mock_generate:
            from api.guidance import ChecklistResponse, ChecklistItem, ChecklistSection, ChecklistNote, ChecklistSource
            
            mock_item = ChecklistItem(title="Test Item")
            mock_response = ChecklistResponse(
                summary_top3=[mock_item],
                sections=[ChecklistSection(name="Test", items=[mock_item])],
                notes=[ChecklistNote(type="general", text="Test note")],
                sources=[ChecklistSource(label="Test", url="https://test.com")]
            )
            
            mock_generate.return_value = mock_response
            
            # First request - should call LLM
            response1 = client.post("/api/guidance/checklist", json=sample_sanitation_request)
            assert response1.status_code == 200
            
            # Second request with same data - should use cache
            response2 = client.post("/api/guidance/checklist", json=sample_sanitation_request)
            assert response2.status_code == 200
            
            # Verify same response (cached)
            assert response1.json() == response2.json()

    def test_health_check_integration(self, client):
        """TC-BE-103: Test health check integration across all systems"""
        # Test main app health
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        
        # Test prediction API health
        with patch('api.water_quality_prediction.load_model_parameters') as mock_load_model, \
             patch('api.water_quality_prediction.get_available_sites') as mock_get_sites:
            
            mock_load_model.return_value = {"site_001": {}}
            mock_get_sites.return_value = ["site_001"]
            
            response = client.get("/api/prediction/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["model_loaded"] is True
            assert data["database_connected"] is True

    def test_api_documentation_integration(self, client):
        """TC-BE-104: Test API documentation integration"""
        # Test OpenAPI schema
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "paths" in schema
        
        # Verify all endpoints are documented
        paths = schema["paths"]
        assert "/api/prediction/predict" in paths
        assert "/api/prediction/sites" in paths
        assert "/api/prediction/suburbs" in paths
        assert "/api/guidance/checklist" in paths
        assert "/api/guidance/explain" in paths
        assert "/api/guidance/chat" in paths

    def test_cors_integration(self, client):
        """TC-BE-105: Test CORS integration across all endpoints"""
        # Test CORS on prediction endpoint
        response = client.options("/api/prediction/sites", 
                                headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        
        # Test CORS on guidance endpoint
        response = client.options("/api/guidance/checklist", 
                                headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200

    def test_data_flow_integration(self, client, mock_model_parameters, mock_site_data):
        """TC-BE-106: Test complete data flow integration"""
        with patch('api.water_quality_prediction.load_model_parameters') as mock_load_model, \
             patch('api.water_quality_prediction.get_site_data') as mock_get_site_data, \
             patch('api.water_quality_prediction.get_available_sites') as mock_get_sites:
            
            # Setup mocks
            mock_load_model.return_value = mock_model_parameters
            mock_get_site_data.return_value = mock_site_data
            mock_get_sites.return_value = ["site_001", "site_002"]
            
            # Test complete workflow
            # 1. Get available sites
            sites_response = client.get("/api/prediction/sites")
            assert sites_response.status_code == 200
            
            # 2. Make prediction
            prediction_response = client.post("/api/prediction/predict", 
                                            json={"site_id": "site_001"})
            assert prediction_response.status_code == 200
            
            # 3. Verify data consistency
            sites_data = sites_response.json()
            prediction_data = prediction_response.json()
            
            assert "site_001" in [site["site_id"] for site in sites_data["sites"]]
            assert prediction_data["site_id"] == "site_001"

    def test_performance_integration(self, client, sample_sanitation_request):
        """TC-BE-107: Test performance integration across systems"""
        import time
        
        with patch('api.guidance._generate_llm_checklist') as mock_generate:
            from api.guidance import ChecklistResponse, ChecklistItem, ChecklistSection, ChecklistNote, ChecklistSource
            
            mock_item = ChecklistItem(title="Test Item")
            mock_response = ChecklistResponse(
                summary_top3=[mock_item],
                sections=[ChecklistSection(name="Test", items=[mock_item])],
                notes=[ChecklistNote(type="general", text="Test note")],
                sources=[ChecklistSource(label="Test", url="https://test.com")]
            )
            
            mock_generate.return_value = mock_response
            
            # Test response time
            start_time = time.time()
            response = client.post("/api/guidance/checklist", json=sample_sanitation_request)
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < 5.0  # Should respond within 5 seconds

    def test_error_propagation_integration(self, client):
        """TC-BE-108: Test error propagation across integrated systems"""
        # Test database error propagation
        with patch('api.water_quality_prediction.pd.read_sql') as mock_read_sql:
            mock_read_sql.side_effect = Exception("Database connection failed")
            
            response = client.get("/api/prediction/sites")
            assert response.status_code == 500
            assert "Failed to load sites" in response.json()["detail"]

    def test_concurrent_requests_integration(self, client, sample_sanitation_request):
        """TC-BE-109: Test concurrent request handling"""
        import threading
        import time
        
        results = []
        
        def make_request():
            with patch('api.guidance._generate_llm_checklist') as mock_generate:
                from api.guidance import ChecklistResponse, ChecklistItem, ChecklistSection, ChecklistNote, ChecklistSource
                
                mock_item = ChecklistItem(title="Test Item")
                mock_response = ChecklistResponse(
                    summary_top3=[mock_item],
                    sections=[ChecklistSection(name="Test", items=[mock_item])],
                    notes=[ChecklistNote(type="general", text="Test note")],
                    sources=[ChecklistSource(label="Test", url="https://test.com")]
                )
                
                mock_generate.return_value = mock_response
                
                response = client.post("/api/guidance/checklist", json=sample_sanitation_request)
                results.append(response.status_code)
        
        # Create multiple threads
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all requests succeeded
        assert len(results) == 3
        assert all(status == 200 for status in results)
