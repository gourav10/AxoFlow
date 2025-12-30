"""Tests for authentication router."""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from fastapi import status


class TestRegister:
    """Tests for /api/auth/register endpoint."""

    @patch('app.routers.auth.get_candidate_by_email')
    @patch('app.routers.auth.create_candidate')
    def test_register_success(self, mock_create_candidate, mock_get_candidate_by_email, client):
        """Test successful user registration."""
        mock_get_candidate_by_email.return_value = None
        mock_create_candidate.return_value = {
            "Id": 1,
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "created_at": datetime.now().isoformat()
        }

        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "full_name": "New User",
                "password": "password123"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert data["id"] == 1
        assert data["is_active"] is True

    @patch('app.routers.auth.get_candidate_by_email')
    def test_register_duplicate_email(self, mock_get_candidate_by_email, client):
        """Test registration with existing email."""
        mock_get_candidate_by_email.return_value = {
            "Id": 1,
            "email": "existing@example.com"
        }

        response = client.post(
            "/api/auth/register",
            json={
                "email": "existing@example.com",
                "full_name": "Existing User",
                "password": "password123"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]

    @patch('app.routers.auth.get_candidate_by_email')
    @patch('app.routers.auth.create_candidate')
    def test_register_single_name(self, mock_create_candidate, mock_get_candidate_by_email, client):
        """Test registration with single name."""
        mock_get_candidate_by_email.return_value = None
        mock_create_candidate.return_value = {
            "Id": 2,
            "email": "singlename@example.com",
            "first_name": "Madonna",
            "last_name": "",
            "created_at": datetime.now().isoformat()
        }

        response = client.post(
            "/api/auth/register",
            json={
                "email": "singlename@example.com",
                "full_name": "Madonna",
                "password": "password123"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED

    @patch('app.routers.auth.get_candidate_by_email')
    @patch('app.routers.auth.create_candidate')
    def test_register_create_candidate_failure(self, mock_create_candidate, mock_get_candidate_by_email, client):
        """Test registration when create_candidate fails."""
        mock_get_candidate_by_email.return_value = None
        mock_create_candidate.side_effect = Exception("Database error")

        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "full_name": "Test User",
                "password": "password123"
            }
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to create user" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        """Test registration with invalid email."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "not-an-email",
                "full_name": "Test User",
                "password": "password123"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch('app.routers.auth.get_candidate_by_email')
    @patch('app.routers.auth.create_candidate')
    def test_register_multiple_name_parts(self, mock_create_candidate, mock_get_candidate_by_email, client):
        """Test registration with multiple name parts."""
        mock_get_candidate_by_email.return_value = None
        mock_create_candidate.return_value = {
            "Id": 3,
            "email": "multiname@example.com",
            "first_name": "John",
            "last_name": "von Neumann Jr",
            "created_at": datetime.now().isoformat()
        }

        response = client.post(
            "/api/auth/register",
            json={
                "email": "multiname@example.com",
                "full_name": "John von Neumann Jr",
                "password": "password123"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED


class TestLogin:
    """Tests for /api/auth/login endpoint."""

    @patch('app.routers.auth.get_candidate_by_email')
    @patch('app.routers.auth.verify_password')
    def test_login_success(self, mock_verify_password, mock_get_candidate_by_email, client):
        """Test successful login."""
        mock_get_candidate_by_email.return_value = {
            "Id": 1,
            "email": "user@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "encoded_password",
            "created_at": datetime.now().isoformat()
        }
        mock_verify_password.return_value = True

        response = client.post(
            "/api/auth/login",
            json={
                "email": "user@example.com",
                "password": "password123"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "user@example.com"

    @patch('app.routers.auth.get_candidate_by_email')
    def test_login_user_not_found(self, mock_get_candidate_by_email, client):
        """Test login with non-existent user."""
        mock_get_candidate_by_email.return_value = None

        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.json()["detail"]

    @patch('app.routers.auth.get_candidate_by_email')
    @patch('app.routers.auth.verify_password')
    def test_login_wrong_password(self, mock_verify_password, mock_get_candidate_by_email, client):
        """Test login with wrong password."""
        mock_get_candidate_by_email.return_value = {
            "Id": 1,
            "email": "user@example.com",
            "password": "encoded_password"
        }
        mock_verify_password.return_value = False

        response = client.post(
            "/api/auth/login",
            json={
                "email": "user@example.com",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.json()["detail"]

    @patch('app.routers.auth.get_candidate_by_email')
    @patch('app.routers.auth.verify_password')
    def test_login_token_format(self, mock_verify_password, mock_get_candidate_by_email, client):
        """Test login token format."""
        mock_get_candidate_by_email.return_value = {
            "Id": 42,
            "email": "user@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "encoded_password",
            "created_at": datetime.now().isoformat()
        }
        mock_verify_password.return_value = True

        response = client.post(
            "/api/auth/login",
            json={
                "email": "user@example.com",
                "password": "password123"
            }
        )

        data = response.json()
        assert data["access_token"] == "mock_token_42"


class TestLogout:
    """Tests for /api/auth/logout endpoint."""

    def test_logout_success(self, client):
        """Test successful logout."""
        response = client.post("/api/auth/logout")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "Successfully logged out" in data["message"]


class TestGetCurrentUser:
    """Tests for /api/auth/me endpoint."""

    @patch('app.routers.auth.get_candidate_by_email')
    def test_get_current_user_existing(self, mock_get_candidate_by_email, client):
        """Test getting current user when demo user exists."""
        mock_get_candidate_by_email.return_value = {
            "Id": 1,
            "email": "demo@axoflow.com",
            "first_name": "Demo",
            "last_name": "User",
            "created_at": datetime.now().isoformat()
        }

        response = client.get("/api/auth/me")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "demo@axoflow.com"
        assert data["full_name"] == "Demo User"

    @patch('app.routers.auth.get_candidate_by_email')
    @patch('app.routers.auth.create_candidate')
    def test_get_current_user_create_demo(self, mock_create_candidate, mock_get_candidate_by_email, client):
        """Test getting current user when demo user doesn't exist."""
        mock_get_candidate_by_email.return_value = None
        mock_create_candidate.return_value = {
            "Id": 1,
            "email": "demo@axoflow.com",
            "first_name": "Demo",
            "last_name": "User",
            "created_at": datetime.now().isoformat()
        }

        response = client.get("/api/auth/me")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "demo@axoflow.com"

    @patch('app.routers.auth.get_candidate_by_email')
    @patch('app.routers.auth.create_candidate')
    def test_get_current_user_create_failure(self, mock_create_candidate, mock_get_candidate_by_email, client):
        """Test getting current user when creation fails."""
        mock_get_candidate_by_email.return_value = None
        mock_create_candidate.side_effect = Exception("Database error")

        response = client.get("/api/auth/me")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to get current user" in response.json()["detail"]
