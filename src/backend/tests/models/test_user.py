"""Tests for user models."""

import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.user import (
    UserBase, UserCreate, UserLogin, User, UserProfile, UserProfileUpdate
)


class TestUserBase:
    """Tests for UserBase model."""

    def test_valid_user_base(self):
        """Test creating a valid UserBase instance."""
        user = UserBase(
            email="test@example.com",
            full_name="Test User"
        )
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"

    def test_invalid_email(self):
        """Test UserBase with invalid email."""
        with pytest.raises(ValidationError):
            UserBase(
                email="invalid-email",
                full_name="Test User"
            )

    def test_empty_full_name(self):
        """Test UserBase with empty full name."""
        user = UserBase(
            email="test@example.com",
            full_name=""
        )
        assert user.full_name == ""


class TestUserCreate:
    """Tests for UserCreate model."""

    def test_valid_user_create(self):
        """Test creating a valid UserCreate instance."""
        user = UserCreate(
            email="test@example.com",
            full_name="Test User",
            password="securepassword123"
        )
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.password == "securepassword123"

    def test_missing_password(self):
        """Test UserCreate without password."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                full_name="Test User"
            )


class TestUserLogin:
    """Tests for UserLogin model."""

    def test_valid_user_login(self):
        """Test creating a valid UserLogin instance."""
        login = UserLogin(
            email="test@example.com",
            password="mypassword"
        )
        assert login.email == "test@example.com"
        assert login.password == "mypassword"

    def test_invalid_email_format(self):
        """Test UserLogin with invalid email format."""
        with pytest.raises(ValidationError):
            UserLogin(
                email="not-an-email",
                password="password123"
            )


class TestUser:
    """Tests for User model."""

    def test_valid_user(self):
        """Test creating a valid User instance."""
        now = datetime.now()
        user = User(
            id=1,
            email="test@example.com",
            full_name="Test User",
            created_at=now,
            is_active=True
        )
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.created_at == now
        assert user.is_active is True

    def test_user_default_is_active(self):
        """Test User with default is_active value."""
        user = User(
            id=1,
            email="test@example.com",
            full_name="Test User",
            created_at=datetime.now()
        )
        assert user.is_active is True

    def test_user_from_attributes_config(self):
        """Test User model has from_attributes config."""
        assert User.model_config.get("from_attributes") is True


class TestUserProfile:
    """Tests for UserProfile model."""

    def test_valid_user_profile(self):
        """Test creating a valid UserProfile instance."""
        profile = UserProfile(
            id=1,
            email="test@example.com",
            full_name="Test User",
            phone="+1-555-0123",
            current_company="TechCorp",
            current_title="Software Engineer",
            years_of_experience=5,
            skills=["Python", "FastAPI"],
            resume_url="https://example.com/resume.pdf"
        )
        assert profile.id == 1
        assert profile.phone == "+1-555-0123"
        assert profile.current_company == "TechCorp"
        assert profile.years_of_experience == 5
        assert len(profile.skills) == 2

    def test_user_profile_optional_fields(self):
        """Test UserProfile with optional fields as None."""
        profile = UserProfile(
            id=1,
            email="test@example.com",
            full_name="Test User"
        )
        assert profile.phone is None
        assert profile.current_company is None
        assert profile.current_title is None
        assert profile.years_of_experience is None
        assert profile.skills == []
        assert profile.resume_url is None

    def test_user_profile_from_attributes_config(self):
        """Test UserProfile model has from_attributes config."""
        assert UserProfile.model_config.get("from_attributes") is True


class TestUserProfileUpdate:
    """Tests for UserProfileUpdate model."""

    def test_valid_user_profile_update(self):
        """Test creating a valid UserProfileUpdate instance."""
        update = UserProfileUpdate(
            full_name="Updated Name",
            phone="+1-555-9999"
        )
        assert update.full_name == "Updated Name"
        assert update.phone == "+1-555-9999"

    def test_user_profile_update_all_optional(self):
        """Test UserProfileUpdate with all fields as None."""
        update = UserProfileUpdate()
        assert update.full_name is None
        assert update.phone is None
        assert update.current_company is None
        assert update.current_title is None
        assert update.years_of_experience is None
        assert update.skills is None

    def test_user_profile_update_skills(self):
        """Test UserProfileUpdate with skills list."""
        update = UserProfileUpdate(
            skills=["Python", "Django", "PostgreSQL"]
        )
        assert len(update.skills) == 3
        assert "Django" in update.skills
