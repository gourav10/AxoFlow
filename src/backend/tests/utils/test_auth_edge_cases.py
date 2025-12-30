"""Additional tests for authentication utilities edge cases."""

import pytest
from unittest.mock import patch
from app.utils.auth import verify_password


class TestVerifyPasswordEdgeCases:
    """Tests for edge cases in verify_password function."""

    def test_verify_password_exception_with_invalid_base64(self):
        """Test verify_password with completely invalid base64 string."""
        plain_password = "testpassword"
        # Create an invalid base64 that will cause decode error
        invalid_encoded = "!!!invalid_base64_@@@"

        # Should catch exception and return False
        result = verify_password(plain_password, invalid_encoded)
        assert result is False

    def test_verify_password_with_corrupted_encoding(self):
        """Test verify_password with corrupted encoding."""
        plain_password = "testpassword"
        # Partially valid base64 but will fail comparison
        corrupted = "YWJj"  # This is valid base64 for "abc"

        result = verify_password(plain_password, corrupted)
        assert result is False

    @patch('app.utils.auth.base64.b64encode')
    def test_verify_password_exception_in_encoding(self, mock_b64encode):
        """Test verify_password when encoding raises exception."""
        # Make base64.b64encode raise an exception
        mock_b64encode.side_effect = Exception("Encoding error")

        plain_password = "testpassword"
        encoded_password = "dGVzdHBhc3N3b3Jk"

        # Should catch exception and return False
        result = verify_password(plain_password, encoded_password)
        assert result is False
