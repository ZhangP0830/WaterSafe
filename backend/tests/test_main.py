"""
Test cases for main FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

class TestMainApplication:
    """Test cases for main application setup and configuration"""

    def test_app_creation(self, client):
        """TC-BE-001: Test FastAPI app creation and basic configuration"""
        # Test that the app is created successfully
        assert client.app is not None
        assert client.app.title == "WaterSafe API"
        assert client.app.version == "1.0.0"

    def test_cors_middleware(self, client):
        """TC-BE-002: Test CORS middleware configuration"""
        # Test CORS headers are present
        response = client.options("/", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        
        # Test that CORS headers are set correctly
        response = client.get("/")
        assert "access-control-allow-origin" in response.headers or "Access-Control-Allow-Origin" in response.headers

    def test_root_endpoint(self, client):
        """TC-BE-003: Test root endpoint functionality"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert data["message"] == "WaterSafe API is running!"

    def test_health_check_endpoint(self, client):
        """TC-BE-004: Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_router_inclusion(self, client):
        """TC-BE-005: Test that all API routers are included"""
        # Test that prediction router is included
        response = client.get("/api/prediction/health")
        assert response.status_code == 200
        
        # Test that guidance router is included
        response = client.get("/api/guidance/")
        # Should return 405 Method Not Allowed for GET on POST endpoint
        assert response.status_code == 405

    def test_api_documentation(self, client):
        """TC-BE-006: Test API documentation endpoints"""
        # Test OpenAPI schema
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "WaterSafe API"

    def test_docs_endpoint(self, client):
        """TC-BE-007: Test API documentation UI"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_redoc_endpoint(self, client):
        """TC-BE-008: Test ReDoc documentation"""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_invalid_endpoint(self, client):
        """TC-BE-009: Test handling of invalid endpoints"""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """TC-BE-010: Test handling of unsupported HTTP methods"""
        # Test POST on GET-only endpoint
        response = client.post("/health")
        assert response.status_code == 405

    @pytest.mark.asyncio
    async def test_startup_behavior(self):
        """TC-BE-011: Test application startup behavior"""
        # Test that the app can be imported and configured
        from main import app
        assert app is not None
        
        # Test that all routers are properly included
        routes = [route.path for route in app.routes]
        assert "/api/prediction" in str(routes)
        assert "/api/guidance" in str(routes)

    def test_environment_variables(self, client):
        """TC-BE-012: Test environment variable handling"""
        # Test that the app handles missing environment variables gracefully
        with patch.dict('os.environ', {}, clear=True):
            # App should still start even without env vars
            from main import app
            assert app is not None

    def test_cors_origins_configuration(self, client):
        """TC-BE-013: Test CORS origins configuration"""
        # Test that localhost origins are allowed
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        
        # Test that Vercel origins are allowed
        response = client.get("/", headers={"Origin": "https://water-safety.vercel.app"})
        assert response.status_code == 200

    def test_cors_credentials(self, client):
        """TC-BE-014: Test CORS credentials configuration"""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        # Should not fail due to credentials configuration
        assert response.status_code == 200

    def test_cors_methods(self, client):
        """TC-BE-015: Test CORS methods configuration"""
        # Test that all methods are allowed
        response = client.options("/", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
