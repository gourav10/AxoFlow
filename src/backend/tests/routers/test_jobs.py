"""Tests for jobs router."""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from fastapi import status
from app.routers.jobs import jobs_db, next_job_id
from app.models.job import JobType, JobStatus


class TestListJobs:
    """Tests for /api/jobs endpoint (GET)."""

    def test_list_jobs_default(self, client):
        """Test listing jobs with default pagination."""
        response = client.get("/api/jobs")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3  # We have 3 default jobs

    def test_list_jobs_with_pagination(self, client):
        """Test listing jobs with pagination."""
        response = client.get("/api/jobs?skip=1&limit=1")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_list_jobs_skip_all(self, client):
        """Test listing jobs with skip beyond available jobs."""
        response = client.get("/api/jobs?skip=100&limit=10")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == []

    def test_list_jobs_large_limit(self, client):
        """Test listing jobs with large limit."""
        response = client.get("/api/jobs?skip=0&limit=100")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_list_jobs_response_structure(self, client):
        """Test that job response has correct structure."""
        response = client.get("/api/jobs")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        if len(data) > 0:
            job = data[0]
            assert "id" in job
            assert "title" in job
            assert "company" in job
            assert "location" in job
            assert "job_type" in job
            assert "status" in job


class TestGetJob:
    """Tests for /api/jobs/{job_id} endpoint (GET)."""

    def test_get_job_success(self, client):
        """Test getting job by ID successfully."""
        response = client.get("/api/jobs/1")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Senior Software Engineer"
        assert data["company"] == "TechCorp"

    def test_get_job_not_found(self, client):
        """Test getting non-existent job."""
        response = client.get("/api/jobs/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Job not found" in response.json()["detail"]

    def test_get_job_all_fields(self, client):
        """Test that all job fields are returned."""
        response = client.get("/api/jobs/1")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "requirements" in data
        assert "salary_range" in data
        assert "url" in data
        assert "description" in data


class TestSearchJobs:
    """Tests for /api/jobs/search endpoint (POST)."""

    def test_search_jobs_by_query(self, client):
        """Test searching jobs by query."""
        response = client.post(
            "/api/jobs/search",
            json={
                "query": "software"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        # Should match "Senior Software Engineer"
        assert any("Software" in job["title"] for job in data)

    def test_search_jobs_by_location(self, client):
        """Test searching jobs by location."""
        response = client.post(
            "/api/jobs/search",
            json={
                "location": "remote"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all("Remote" in job["location"] for job in data)

    def test_search_jobs_by_job_type(self, client):
        """Test searching jobs by job type."""
        response = client.post(
            "/api/jobs/search",
            json={
                "job_type": "full_time"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(job["job_type"] == "full_time" for job in data)

    def test_search_jobs_by_company(self, client):
        """Test searching jobs by company."""
        response = client.post(
            "/api/jobs/search",
            json={
                "company": "TechCorp"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all("TechCorp" in job["company"] for job in data)

    def test_search_jobs_multiple_criteria(self, client):
        """Test searching jobs with multiple criteria."""
        response = client.post(
            "/api/jobs/search",
            json={
                "query": "engineer",
                "job_type": "full_time"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Results should match both criteria
        for job in data:
            assert "engineer" in job["title"].lower()
            assert job["job_type"] == "full_time"

    def test_search_jobs_no_results(self, client):
        """Test searching jobs with no matches."""
        response = client.post(
            "/api/jobs/search",
            json={
                "query": "nonexistentjobtitle12345"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == []

    def test_search_jobs_empty_criteria(self, client):
        """Test searching jobs with empty criteria."""
        response = client.post(
            "/api/jobs/search",
            json={}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Should return all jobs when no criteria specified
        assert len(data) >= 3

    def test_search_jobs_case_insensitive(self, client):
        """Test that job search is case insensitive."""
        response = client.post(
            "/api/jobs/search",
            json={
                "query": "SOFTWARE"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1


class TestCreateJob:
    """Tests for /api/jobs endpoint (POST)."""

    def test_create_job_success(self, client, sample_job_data):
        """Test creating a job successfully."""
        response = client.post("/api/jobs", json=sample_job_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == sample_job_data["title"]
        assert data["company"] == sample_job_data["company"]
        assert data["status"] == "active"
        assert "id" in data
        assert "created_at" in data

    def test_create_job_minimal(self, client):
        """Test creating a job with minimal required fields."""
        job_data = {
            "title": "Test Job",
            "company": "Test Company",
            "location": "Test Location",
            "job_type": "full_time",
            "description": "Test description",
            "requirements": [],
            "url": "https://example.com/job"
        }

        response = client.post("/api/jobs", json=job_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["salary_range"] is None

    def test_create_job_with_all_fields(self, client):
        """Test creating a job with all fields."""
        job_data = {
            "title": "Full Stack Developer",
            "company": "WebCorp",
            "location": "Seattle, WA",
            "job_type": "full_time",
            "description": "Build web applications",
            "requirements": ["JavaScript", "Python", "SQL"],
            "salary_range": "$100k - $140k",
            "url": "https://example.com/jobs/fullstack"
        }

        response = client.post("/api/jobs", json=job_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["salary_range"] == "$100k - $140k"
        assert len(data["requirements"]) == 3

    def test_create_job_invalid_url(self, client):
        """Test creating a job with invalid URL."""
        job_data = {
            "title": "Test Job",
            "company": "Test Company",
            "location": "Test Location",
            "job_type": "full_time",
            "description": "Test description",
            "requirements": [],
            "url": "not-a-valid-url"
        }

        response = client.post("/api/jobs", json=job_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_job_invalid_job_type(self, client):
        """Test creating a job with invalid job type."""
        job_data = {
            "title": "Test Job",
            "company": "Test Company",
            "location": "Test Location",
            "job_type": "invalid_type",
            "description": "Test description",
            "requirements": [],
            "url": "https://example.com/job"
        }

        response = client.post("/api/jobs", json=job_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_job_missing_required_field(self, client):
        """Test creating a job without required field."""
        job_data = {
            "company": "Test Company",
            "location": "Test Location",
            "job_type": "full_time",
            "description": "Test description",
            "requirements": [],
            "url": "https://example.com/job"
            # Missing title
        }

        response = client.post("/api/jobs", json=job_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_job_contract_type(self, client):
        """Test creating a contract job."""
        job_data = {
            "title": "Contract Developer",
            "company": "ContractCorp",
            "location": "Remote",
            "job_type": "contract",
            "description": "6 month contract",
            "requirements": ["Python"],
            "url": "https://example.com/contract"
        }

        response = client.post("/api/jobs", json=job_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["job_type"] == "contract"

    def test_create_job_internship_type(self, client):
        """Test creating an internship job."""
        job_data = {
            "title": "Summer Intern",
            "company": "InternCorp",
            "location": "Boston, MA",
            "job_type": "internship",
            "description": "Summer internship program",
            "requirements": ["Student", "Eager to learn"],
            "url": "https://example.com/intern"
        }

        response = client.post("/api/jobs", json=job_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["job_type"] == "internship"
