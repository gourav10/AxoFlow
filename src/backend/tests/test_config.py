"""Tests for configuration module."""

import pytest
from app.config import Settings, settings


class TestSettings:
    """Tests for Settings class."""

    def test_settings_default_values(self):
        """Test default settings values."""
        test_settings = Settings()

        assert test_settings.API_V1_STR == "/api"
        assert test_settings.PROJECT_NAME == "AxoFlow API"
        assert test_settings.VERSION == "1.0.0"
        assert test_settings.DESCRIPTION == "Job Copilot - Automated Job Application System"

    def test_settings_cors_origins(self):
        """Test CORS origins configuration."""
        test_settings = Settings()

        assert "http://localhost:5173" in test_settings.BACKEND_CORS_ORIGINS
        assert "http://localhost:3000" in test_settings.BACKEND_CORS_ORIGINS
        assert "http://localhost:8000" in test_settings.BACKEND_CORS_ORIGINS

    def test_settings_security_defaults(self):
        """Test security settings defaults."""
        test_settings = Settings()

        assert test_settings.SECRET_KEY == "your-secret-key-here-change-in-production"
        assert test_settings.ALGORITHM == "HS256"
        assert test_settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30

    def test_settings_database_url(self):
        """Test database URL configuration."""
        test_settings = Settings()

        assert test_settings.DATABASE_URL == "sqlite:///./axoflow.db"

    def test_settings_nocodb_configuration(self):
        """Test NocoDB configuration defaults."""
        test_settings = Settings()

        assert test_settings.NOCODB_URL == "https://anton-server-station.tailfa58fb.ts.net:8081"
        assert test_settings.NOCODB_API_TOKEN == ""
        assert test_settings.NOCODB_BASE_ID == ""
        assert test_settings.NOCODB_TABLE_ID == ""

    def test_settings_case_sensitive(self):
        """Test that settings are case sensitive."""
        assert Settings.model_config.get("case_sensitive") is True

    def test_settings_env_file_config(self):
        """Test that env_file is configured."""
        assert Settings.model_config.get("env_file") == ".env"

    def test_global_settings_instance(self):
        """Test that global settings instance exists."""
        assert settings is not None
        assert isinstance(settings, Settings)

    def test_settings_can_be_overridden(self):
        """Test that settings can be overridden via constructor."""
        custom_settings = Settings(
            PROJECT_NAME="Custom Project",
            VERSION="2.0.0"
        )

        assert custom_settings.PROJECT_NAME == "Custom Project"
        assert custom_settings.VERSION == "2.0.0"
        # Default values should still be present
        assert custom_settings.API_V1_STR == "/api"

    def test_settings_cors_origins_is_list(self):
        """Test that CORS origins is a list."""
        test_settings = Settings()

        assert isinstance(test_settings.BACKEND_CORS_ORIGINS, list)
        assert len(test_settings.BACKEND_CORS_ORIGINS) >= 3

    def test_settings_access_token_expire_is_int(self):
        """Test that access token expire minutes is an integer."""
        test_settings = Settings()

        assert isinstance(test_settings.ACCESS_TOKEN_EXPIRE_MINUTES, int)
        assert test_settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0
