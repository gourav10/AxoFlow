"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }


@pytest.fixture
def sample_job_data():
    """Sample job data for testing."""
    return {
        "title": "Test Engineer",
        "company": "Test Company",
        "location": "Test City",
        "job_type": "full_time",
        "description": "Test job description",
        "requirements": ["Python", "Testing"],
        "salary_range": "$100k - $150k",
        "url": "https://example.com/job/123"
    }


@pytest.fixture
def sample_application_data():
    """Sample application data for testing."""
    return {
        "job_id": 1,
        "cover_letter": "Test cover letter",
        "custom_resume": None
    }
