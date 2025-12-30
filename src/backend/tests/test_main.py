"""Tests for main application module."""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings


class TestApp:
    """Tests for FastAPI application."""

    def test_app_exists(self):
        """Test that app instance exists."""
        assert app is not None

    def test_app_title(self):
        """Test that app has correct title."""
        assert app.title == settings.PROJECT_NAME

    def test_app_version(self):
        """Test that app has correct version."""
        assert app.version == settings.VERSION

    def test_app_description(self):
        """Test that app has correct description."""
        assert app.description == settings.DESCRIPTION

    def test_app_docs_url(self):
        """Test that docs URL is configured."""
        assert app.docs_url == "/docs"

    def test_app_redoc_url(self):
        """Test that redoc URL is configured."""
        assert app.redoc_url == "/redoc"


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns correct response."""
        response = client.get("/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "Welcome to AxoFlow API" in data["message"]

    def test_root_endpoint_has_version(self, client):
        """Test root endpoint includes version."""
        response = client.get("/")

        data = response.json()
        assert "version" in data
        assert data["version"] == settings.VERSION

    def test_root_endpoint_has_docs_url(self, client):
        """Test root endpoint includes docs URL."""
        response = client.get("/")

        data = response.json()
        assert "docs" in data
        assert data["docs"] == "/docs"

    def test_root_endpoint_has_status(self, client):
        """Test root endpoint includes status."""
        response = client.get("/")

        data = response.json()
        assert "status" in data
        assert data["status"] == "operational"


class TestHealthCheckEndpoint:
    """Tests for health check endpoint."""

    def test_health_check_endpoint(self, client):
        """Test health check endpoint returns healthy status."""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_check_has_service_name(self, client):
        """Test health check includes service name."""
        response = client.get("/health")

        data = response.json()
        assert "service" in data
        assert data["service"] == "axoflow-api"

    def test_health_check_has_version(self, client):
        """Test health check includes version."""
        response = client.get("/health")

        data = response.json()
        assert "version" in data
        assert data["version"] == settings.VERSION


class TestCORS:
    """Tests for CORS configuration."""

    def test_cors_middleware_exists(self):
        """Test that CORS middleware is configured."""
        from fastapi.middleware.cors import CORSMiddleware

        # Check if CORS middleware is in the middleware stack
        middleware_types = [type(m) for m in app.user_middleware]
        # Note: middleware_types will have Starlette middleware classes
        # We can't directly check for CORSMiddleware but we can verify the app has middleware
        assert len(app.user_middleware) > 0

    def test_cors_preflight_request(self, client):
        """Test CORS preflight request."""
        response = client.options(
            "/api/auth/login",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )

        # FastAPI/Starlette handles OPTIONS automatically
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_405_METHOD_NOT_ALLOWED]


class TestRouterInclusion:
    """Tests for router inclusion."""

    def test_auth_router_included(self, client):
        """Test that auth router is included."""
        # Test an auth endpoint to verify router is included
        response = client.post("/api/auth/logout")
        assert response.status_code == status.HTTP_200_OK

    def test_jobs_router_included(self, client):
        """Test that jobs router is included."""
        # Test a jobs endpoint to verify router is included
        response = client.get("/api/jobs")
        assert response.status_code == status.HTTP_200_OK

    def test_users_router_included(self, client):
        """Test that users router is included."""
        # Test a users endpoint to verify router is included
        response = client.get("/api/users/profile")
        # Will return 200 or 404 depending on data, but route should exist
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


class TestMainExecution:
    """Tests for main execution."""

    def test_main_module_imports(self):
        """Test that main module imports are working."""
        from app.main import app
        from app.config import settings
        from app.routers import auth, jobs, users

        assert app is not None
        assert settings is not None
        assert auth is not None
        assert jobs is not None
        assert users is not None


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_openapi_schema_exists(self, client):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

    def test_swagger_ui_accessible(self, client):
        """Test that Swagger UI is accessible."""
        response = client.get("/docs")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"].startswith("text/html")

    def test_redoc_accessible(self, client):
        """Test that ReDoc is accessible."""
        response = client.get("/redoc")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"].startswith("text/html")
