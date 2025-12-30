"""Tests for authentication utilities."""

import base64
import pytest
from app.utils.auth import encode_password, verify_password


class TestEncodePassword:
    """Tests for encode_password function."""

    def test_encode_password_basic(self):
        """Test basic password encoding."""
        password = "testpassword"
        encoded = encode_password(password)

        # Verify it's base64 encoded
        expected = base64.b64encode(password.encode()).decode()
        assert encoded == expected

    def test_encode_password_special_characters(self):
        """Test encoding password with special characters."""
        password = "p@ssw0rd!#$%"
        encoded = encode_password(password)

        # Verify decoding works
        decoded = base64.b64decode(encoded.encode()).decode()
        assert decoded == password

    def test_encode_password_empty_string(self):
        """Test encoding empty password."""
        password = ""
        encoded = encode_password(password)

        expected = base64.b64encode(password.encode()).decode()
        assert encoded == expected

    def test_encode_password_unicode(self):
        """Test encoding password with unicode characters."""
        password = "пароль密码"
        encoded = encode_password(password)

        # Verify it can be decoded back
        decoded = base64.b64decode(encoded.encode()).decode()
        assert decoded == password

    def test_encode_password_long_string(self):
        """Test encoding very long password."""
        password = "a" * 1000
        encoded = encode_password(password)

        decoded = base64.b64decode(encoded.encode()).decode()
        assert decoded == password


class TestVerifyPassword:
    """Tests for verify_password function."""

    def test_verify_password_correct(self):
        """Test verifying correct password."""
        plain_password = "mypassword123"
        encoded_password = encode_password(plain_password)

        assert verify_password(plain_password, encoded_password) is True

    def test_verify_password_incorrect(self):
        """Test verifying incorrect password."""
        plain_password = "mypassword123"
        wrong_password = "wrongpassword"
        encoded_password = encode_password(plain_password)

        assert verify_password(wrong_password, encoded_password) is False

    def test_verify_password_empty_strings(self):
        """Test verifying empty passwords."""
        plain_password = ""
        encoded_password = encode_password(plain_password)

        assert verify_password(plain_password, encoded_password) is True

    def test_verify_password_case_sensitive(self):
        """Test that password verification is case sensitive."""
        plain_password = "Password123"
        encoded_password = encode_password(plain_password)

        assert verify_password("password123", encoded_password) is False

    def test_verify_password_special_characters(self):
        """Test verifying password with special characters."""
        plain_password = "p@ssw0rd!#$%"
        encoded_password = encode_password(plain_password)

        assert verify_password(plain_password, encoded_password) is True

    def test_verify_password_with_spaces(self):
        """Test verifying password with spaces."""
        plain_password = "my password 123"
        encoded_password = encode_password(plain_password)

        assert verify_password(plain_password, encoded_password) is True

    def test_verify_password_invalid_encoded(self):
        """Test verifying against invalid encoded password."""
        plain_password = "testpassword"
        invalid_encoded = "not-valid-base64!@#"

        # Should return False for invalid encoding
        result = verify_password(plain_password, invalid_encoded)
        assert result is False

    def test_verify_password_unicode(self):
        """Test verifying unicode password."""
        plain_password = "пароль密码"
        encoded_password = encode_password(plain_password)

        assert verify_password(plain_password, encoded_password) is True

    def test_verify_password_exception_handling(self):
        """Test that exceptions are handled gracefully."""
        # Pass None or invalid types should be caught by try/except
        plain_password = "test"

        # This should not raise an exception, just return False
        result = verify_password(plain_password, "")
        assert result is False
