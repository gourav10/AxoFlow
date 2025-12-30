"""Tests for job models."""

import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.job import (
    JobType, JobStatus, JobBase, JobCreate, Job, JobSearch
)


class TestJobType:
    """Tests for JobType enum."""

    def test_job_type_values(self):
        """Test JobType enum values."""
        assert JobType.FULL_TIME.value == "full_time"
        assert JobType.PART_TIME.value == "part_time"
        assert JobType.CONTRACT.value == "contract"
        assert JobType.INTERNSHIP.value == "internship"

    def test_job_type_is_string_enum(self):
        """Test that JobType is a string enum."""
        assert isinstance(JobType.FULL_TIME, str)


class TestJobStatus:
    """Tests for JobStatus enum."""

    def test_job_status_values(self):
        """Test JobStatus enum values."""
        assert JobStatus.ACTIVE.value == "active"
        assert JobStatus.CLOSED.value == "closed"
        assert JobStatus.DRAFT.value == "draft"

    def test_job_status_is_string_enum(self):
        """Test that JobStatus is a string enum."""
        assert isinstance(JobStatus.ACTIVE, str)


class TestJobBase:
    """Tests for JobBase model."""

    def test_valid_job_base(self):
        """Test creating a valid JobBase instance."""
        job = JobBase(
            title="Software Engineer",
            company="TechCorp",
            location="San Francisco, CA",
            job_type=JobType.FULL_TIME,
            description="Great opportunity",
            requirements=["Python", "FastAPI"],
            salary_range="$120k - $150k",
            url="https://example.com/job/123"
        )
        assert job.title == "Software Engineer"
        assert job.company == "TechCorp"
        assert job.job_type == JobType.FULL_TIME
        assert len(job.requirements) == 2

    def test_job_base_without_salary(self):
        """Test JobBase without salary range."""
        job = JobBase(
            title="Developer",
            company="StartupXYZ",
            location="Remote",
            job_type=JobType.CONTRACT,
            description="Join our team",
            requirements=["JavaScript"],
            url="https://example.com/job/456"
        )
        assert job.salary_range is None

    def test_invalid_url(self):
        """Test JobBase with invalid URL."""
        with pytest.raises(ValidationError):
            JobBase(
                title="Test Job",
                company="Test Co",
                location="Test City",
                job_type=JobType.FULL_TIME,
                description="Test description",
                requirements=["Test"],
                url="not-a-valid-url"
            )

    def test_empty_requirements_list(self):
        """Test JobBase with empty requirements."""
        job = JobBase(
            title="Entry Level",
            company="StartupXYZ",
            location="Remote",
            job_type=JobType.INTERNSHIP,
            description="No experience needed",
            requirements=[],
            url="https://example.com/job/789"
        )
        assert job.requirements == []


class TestJobCreate:
    """Tests for JobCreate model."""

    def test_valid_job_create(self):
        """Test creating a valid JobCreate instance."""
        job = JobCreate(
            title="Backend Developer",
            company="Tech Solutions",
            location="New York, NY",
            job_type=JobType.FULL_TIME,
            description="Looking for backend developer",
            requirements=["Python", "Django", "PostgreSQL"],
            salary_range="$140k - $180k",
            url="https://example.com/jobs/backend"
        )
        assert job.title == "Backend Developer"
        assert job.company == "Tech Solutions"


class TestJob:
    """Tests for Job model."""

    def test_valid_job(self):
        """Test creating a valid Job instance."""
        now = datetime.now()
        job = Job(
            id=1,
            title="Frontend Developer",
            company="WebCorp",
            location="Seattle, WA",
            job_type=JobType.PART_TIME,
            description="Build amazing UIs",
            requirements=["React", "TypeScript"],
            url="https://example.com/jobs/frontend",
            status=JobStatus.ACTIVE,
            created_at=now,
            posted_date=now
        )
        assert job.id == 1
        assert job.status == JobStatus.ACTIVE
        assert job.created_at == now

    def test_job_default_status(self):
        """Test Job with default status."""
        job = Job(
            id=2,
            title="DevOps Engineer",
            company="CloudTech",
            location="Austin, TX",
            job_type=JobType.CONTRACT,
            description="Manage infrastructure",
            requirements=["Kubernetes", "Docker"],
            url="https://example.com/jobs/devops",
            created_at=datetime.now()
        )
        assert job.status == JobStatus.ACTIVE

    def test_job_optional_posted_date(self):
        """Test Job with optional posted_date."""
        job = Job(
            id=3,
            title="Data Scientist",
            company="DataCorp",
            location="Boston, MA",
            job_type=JobType.FULL_TIME,
            description="Analyze data",
            requirements=["Python", "Machine Learning"],
            url="https://example.com/jobs/data",
            created_at=datetime.now()
        )
        assert job.posted_date is None

    def test_job_from_attributes_config(self):
        """Test Job model has from_attributes config."""
        assert Job.model_config.get("from_attributes") is True


class TestJobSearch:
    """Tests for JobSearch model."""

    def test_valid_job_search(self):
        """Test creating a valid JobSearch instance."""
        search = JobSearch(
            query="software engineer",
            location="San Francisco",
            job_type=JobType.FULL_TIME,
            company="Google"
        )
        assert search.query == "software engineer"
        assert search.location == "San Francisco"
        assert search.job_type == JobType.FULL_TIME
        assert search.company == "Google"

    def test_job_search_all_optional(self):
        """Test JobSearch with all fields as None."""
        search = JobSearch()
        assert search.query is None
        assert search.location is None
        assert search.job_type is None
        assert search.company is None

    def test_job_search_partial(self):
        """Test JobSearch with partial fields."""
        search = JobSearch(
            query="python developer",
            job_type=JobType.REMOTE if hasattr(JobType, 'REMOTE') else JobType.FULL_TIME
        )
        assert search.query == "python developer"
        assert search.location is None
        assert search.company is None
