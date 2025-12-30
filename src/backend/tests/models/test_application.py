"""Tests for application models."""

import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.application import (
    ApplicationStatus, ApplicationBase, ApplicationCreate,
    Application, ApplicationUpdate, ApplicationWithJob
)


class TestApplicationStatus:
    """Tests for ApplicationStatus enum."""

    def test_application_status_values(self):
        """Test ApplicationStatus enum values."""
        assert ApplicationStatus.PENDING.value == "pending"
        assert ApplicationStatus.SUBMITTED.value == "submitted"
        assert ApplicationStatus.IN_REVIEW.value == "in_review"
        assert ApplicationStatus.INTERVIEWING.value == "interviewing"
        assert ApplicationStatus.OFFERED.value == "offered"
        assert ApplicationStatus.REJECTED.value == "rejected"
        assert ApplicationStatus.WITHDRAWN.value == "withdrawn"

    def test_application_status_is_string_enum(self):
        """Test that ApplicationStatus is a string enum."""
        assert isinstance(ApplicationStatus.PENDING, str)


class TestApplicationBase:
    """Tests for ApplicationBase model."""

    def test_valid_application_base(self):
        """Test creating a valid ApplicationBase instance."""
        app = ApplicationBase(
            job_id=1,
            cover_letter="I am interested in this position",
            custom_resume="https://example.com/resume.pdf"
        )
        assert app.job_id == 1
        assert app.cover_letter == "I am interested in this position"
        assert app.custom_resume == "https://example.com/resume.pdf"

    def test_application_base_optional_fields(self):
        """Test ApplicationBase with optional fields as None."""
        app = ApplicationBase(job_id=5)
        assert app.job_id == 5
        assert app.cover_letter is None
        assert app.custom_resume is None

    def test_application_base_missing_job_id(self):
        """Test ApplicationBase without required job_id."""
        with pytest.raises(ValidationError):
            ApplicationBase()


class TestApplicationCreate:
    """Tests for ApplicationCreate model."""

    def test_valid_application_create(self):
        """Test creating a valid ApplicationCreate instance."""
        app = ApplicationCreate(
            job_id=10,
            cover_letter="Test cover letter",
            custom_resume=None
        )
        assert app.job_id == 10
        assert app.cover_letter == "Test cover letter"

    def test_application_create_minimal(self):
        """Test ApplicationCreate with minimal data."""
        app = ApplicationCreate(job_id=20)
        assert app.job_id == 20
        assert app.cover_letter is None


class TestApplication:
    """Tests for Application model."""

    def test_valid_application(self):
        """Test creating a valid Application instance."""
        now = datetime.now()
        app = Application(
            id=1,
            user_id=100,
            job_id=50,
            cover_letter="Sample cover letter",
            custom_resume="https://example.com/custom_resume.pdf",
            status=ApplicationStatus.SUBMITTED,
            submitted_at=now,
            created_at=now,
            updated_at=now
        )
        assert app.id == 1
        assert app.user_id == 100
        assert app.job_id == 50
        assert app.status == ApplicationStatus.SUBMITTED

    def test_application_default_status(self):
        """Test Application with default status."""
        now = datetime.now()
        app = Application(
            id=2,
            user_id=200,
            job_id=75,
            created_at=now,
            updated_at=now
        )
        assert app.status == ApplicationStatus.PENDING

    def test_application_optional_submitted_at(self):
        """Test Application with optional submitted_at."""
        now = datetime.now()
        app = Application(
            id=3,
            user_id=300,
            job_id=80,
            status=ApplicationStatus.PENDING,
            created_at=now,
            updated_at=now
        )
        assert app.submitted_at is None

    def test_application_from_attributes_config(self):
        """Test Application model has from_attributes config."""
        assert Application.model_config.get("from_attributes") is True


class TestApplicationUpdate:
    """Tests for ApplicationUpdate model."""

    def test_valid_application_update(self):
        """Test creating a valid ApplicationUpdate instance."""
        update = ApplicationUpdate(
            status=ApplicationStatus.IN_REVIEW,
            cover_letter="Updated cover letter"
        )
        assert update.status == ApplicationStatus.IN_REVIEW
        assert update.cover_letter == "Updated cover letter"

    def test_application_update_all_optional(self):
        """Test ApplicationUpdate with all fields as None."""
        update = ApplicationUpdate()
        assert update.status is None
        assert update.cover_letter is None
        assert update.custom_resume is None

    def test_application_update_status_only(self):
        """Test ApplicationUpdate with only status."""
        update = ApplicationUpdate(status=ApplicationStatus.REJECTED)
        assert update.status == ApplicationStatus.REJECTED
        assert update.cover_letter is None


class TestApplicationWithJob:
    """Tests for ApplicationWithJob model."""

    def test_valid_application_with_job(self):
        """Test creating a valid ApplicationWithJob instance."""
        now = datetime.now()
        app = ApplicationWithJob(
            id=1,
            user_id=100,
            job_id=50,
            cover_letter="Cover letter",
            status=ApplicationStatus.SUBMITTED,
            created_at=now,
            updated_at=now,
            job_title="Software Engineer",
            company="TechCorp",
            job_location="San Francisco, CA"
        )
        assert app.id == 1
        assert app.job_title == "Software Engineer"
        assert app.company == "TechCorp"
        assert app.job_location == "San Francisco, CA"

    def test_application_with_job_inherits_application(self):
        """Test that ApplicationWithJob has all Application fields."""
        now = datetime.now()
        app = ApplicationWithJob(
            id=2,
            user_id=200,
            job_id=60,
            status=ApplicationStatus.INTERVIEWING,
            created_at=now,
            updated_at=now,
            job_title="Backend Developer",
            company="StartupXYZ",
            job_location="Remote"
        )
        # Check inherited fields
        assert app.user_id == 200
        assert app.job_id == 60
        assert app.status == ApplicationStatus.INTERVIEWING
        # Check new fields
        assert app.job_title == "Backend Developer"
        assert app.company == "StartupXYZ"
        assert app.job_location == "Remote"
