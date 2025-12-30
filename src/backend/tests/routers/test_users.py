"""Tests for users and applications router."""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from fastapi import status
from app.routers.users import profiles_db, applications_db


class TestGetUserProfile:
    """Tests for /api/users/profile endpoint (GET)."""

    def test_get_user_profile_success(self, client):
        """Test getting user profile successfully."""
        response = client.get("/api/users/profile")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["email"] == "demo@axoflow.com"
        assert "skills" in data

    def test_get_user_profile_not_found(self, client):
        """Test getting user profile when not found."""
        # Temporarily clear the profiles_db
        original_profiles = profiles_db.copy()
        profiles_db.clear()

        response = client.get("/api/users/profile")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Profile not found" in response.json()["detail"]

        # Restore profiles_db
        profiles_db.update(original_profiles)


class TestUpdateUserProfile:
    """Tests for /api/users/profile endpoint (PUT)."""

    def test_update_user_profile_success(self, client):
        """Test updating user profile successfully."""
        response = client.put(
            "/api/users/profile",
            json={
                "full_name": "Updated Name",
                "phone": "+1-555-9999",
                "current_company": "NewCorp"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["phone"] == "+1-555-9999"
        assert data["current_company"] == "NewCorp"

        # Restore original data
        profiles_db[1]["full_name"] = "Demo User"
        profiles_db[1]["phone"] = "+1-555-0123"
        profiles_db[1]["current_company"] = "TechCorp"

    def test_update_user_profile_partial(self, client):
        """Test updating user profile with partial data."""
        response = client.put(
            "/api/users/profile",
            json={
                "skills": ["Python", "Django", "PostgreSQL"]
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "Django" in data["skills"]

        # Restore original data
        profiles_db[1]["skills"] = ["Python", "FastAPI", "React", "AWS"]

    def test_update_user_profile_not_found(self, client):
        """Test updating profile when not found."""
        # Temporarily clear the profiles_db
        original_profiles = profiles_db.copy()
        profiles_db.clear()

        response = client.put(
            "/api/users/profile",
            json={"full_name": "Test"}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Profile not found" in response.json()["detail"]

        # Restore profiles_db
        profiles_db.update(original_profiles)

    def test_update_user_profile_years_of_experience(self, client):
        """Test updating years of experience."""
        response = client.put(
            "/api/users/profile",
            json={"years_of_experience": 10}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["years_of_experience"] == 10

        # Restore original data
        profiles_db[1]["years_of_experience"] = 5


class TestUploadResume:
    """Tests for /api/users/resume endpoint."""

    def test_upload_resume_success(self, client):
        """Test uploading resume successfully."""
        from io import BytesIO

        file_content = b"PDF content here"
        files = {
            "file": ("resume.pdf", BytesIO(file_content), "application/pdf")
        }

        response = client.post("/api/users/resume", files=files)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "Resume uploaded successfully" in data["message"]
        assert data["filename"] == "resume.pdf"
        assert data["content_type"] == "application/pdf"
        assert "resume_url" in data

    def test_upload_resume_docx(self, client):
        """Test uploading DOCX resume."""
        from io import BytesIO

        file_content = b"DOCX content here"
        files = {
            "file": ("resume.docx", BytesIO(file_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        }

        response = client.post("/api/users/resume", files=files)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["filename"] == "resume.docx"


class TestListApplications:
    """Tests for /api/applications endpoint (GET)."""

    def test_list_applications_empty(self, client):
        """Test listing applications when empty."""
        # Clear applications_db
        applications_db.clear()

        response = client.get("/api/applications")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == []

    def test_list_applications_with_data(self, client):
        """Test listing applications with data."""
        # Add test application
        applications_db[1] = {
            "id": 1,
            "user_id": 1,
            "job_id": 10,
            "status": "pending",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        response = client.get("/api/applications")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert data[0]["job_title"] == "Software Engineer"
        assert data[0]["company"] == "TechCorp"

        # Clean up
        applications_db.clear()


class TestCreateApplication:
    """Tests for /api/applications endpoint (POST)."""

    def test_create_application_success(self, client):
        """Test creating application successfully."""
        # Clear applications first
        applications_db.clear()

        response = client.post(
            "/api/applications",
            json={
                "job_id": 1,
                "cover_letter": "I am very interested in this position",
                "custom_resume": None
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["job_id"] == 1
        assert data["status"] == "pending"
        assert data["user_id"] == 1
        assert "created_at" in data

    def test_create_application_minimal(self, client):
        """Test creating application with minimal data."""
        response = client.post(
            "/api/applications",
            json={
                "job_id": 5
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["job_id"] == 5
        assert data["cover_letter"] is None

    def test_create_application_with_custom_resume(self, client):
        """Test creating application with custom resume."""
        response = client.post(
            "/api/applications",
            json={
                "job_id": 3,
                "cover_letter": "Cover letter text",
                "custom_resume": "https://example.com/custom_resume.pdf"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["custom_resume"] == "https://example.com/custom_resume.pdf"


class TestGetApplication:
    """Tests for /api/applications/{app_id} endpoint (GET)."""

    def test_get_application_success(self, client):
        """Test getting application by ID successfully."""
        # Add test application
        applications_db[100] = {
            "id": 100,
            "user_id": 1,
            "job_id": 10,
            "status": "submitted",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        response = client.get("/api/applications/100")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 100
        assert data["status"] == "submitted"

    def test_get_application_not_found(self, client):
        """Test getting non-existent application."""
        response = client.get("/api/applications/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Application not found" in response.json()["detail"]


class TestUpdateApplication:
    """Tests for /api/applications/{app_id} endpoint (PUT)."""

    def test_update_application_status(self, client):
        """Test updating application status."""
        # Add test application
        applications_db[200] = {
            "id": 200,
            "user_id": 1,
            "job_id": 10,
            "status": "pending",
            "submitted_at": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        response = client.put(
            "/api/applications/200",
            json={"status": "submitted"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "submitted"
        assert data["submitted_at"] is not None

    def test_update_application_cover_letter(self, client):
        """Test updating application cover letter."""
        # Add test application
        applications_db[201] = {
            "id": 201,
            "user_id": 1,
            "job_id": 10,
            "status": "pending",
            "cover_letter": "Old cover letter",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        response = client.put(
            "/api/applications/201",
            json={"cover_letter": "New cover letter"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["cover_letter"] == "New cover letter"

    def test_update_application_not_found(self, client):
        """Test updating non-existent application."""
        response = client.put(
            "/api/applications/99999",
            json={"status": "submitted"}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Application not found" in response.json()["detail"]

    def test_update_application_multiple_fields(self, client):
        """Test updating multiple application fields."""
        # Add test application
        applications_db[202] = {
            "id": 202,
            "user_id": 1,
            "job_id": 10,
            "status": "pending",
            "cover_letter": "Old",
            "custom_resume": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        response = client.put(
            "/api/applications/202",
            json={
                "status": "in_review",
                "cover_letter": "Updated cover letter",
                "custom_resume": "https://example.com/resume.pdf"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "in_review"
        assert data["cover_letter"] == "Updated cover letter"
        assert data["custom_resume"] == "https://example.com/resume.pdf"

    def test_update_application_submitted_at_only_once(self, client):
        """Test that submitted_at is only set once."""
        # Add test application that's already submitted
        now = datetime.now()
        applications_db[203] = {
            "id": 203,
            "user_id": 1,
            "job_id": 10,
            "status": "submitted",
            "submitted_at": now,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        response = client.put(
            "/api/applications/203",
            json={"status": "submitted"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # submitted_at should not change
        assert data["submitted_at"] == now.isoformat()
