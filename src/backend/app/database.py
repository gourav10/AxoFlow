"""
NocoDB Database Integration Module

This module provides functions to interact with NocoDB via REST API.
"""

import requests
import urllib3
from typing import Dict, List, Optional, Any
from app.config import settings

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NocoDBClient:
    """Client for interacting with NocoDB REST API."""
    
    def __init__(self):
        self.base_url = settings.NOCODB_URL
        self.api_token = settings.NOCODB_API_TOKEN
        self.base_id = settings.NOCODB_BASE_ID
        self.table_id = settings.NOCODB_TABLE_ID
        
        # Construct API endpoint - use table_id directly
        self.api_endpoint = f"{self.base_url}/api/v1/db/data/v1/{self.base_id}/{self.table_id}"
        
        # Default headers
        self.headers = {
            "xc-token": self.api_token,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request to NocoDB API.
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint
            **kwargs: Additional arguments for requests
            
        Returns:
            Response JSON data
            
        Raises:
            Exception: If request fails
        """
        url = f"{self.api_endpoint}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                verify=False,  # Disable SSL verification for self-signed certificates
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"NocoDB API error: {str(e)}")
    
    def create_record(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new record in the table.
        
        Args:
            data: Record data
            
        Returns:
            Created record with ID
        """
        return self._make_request("POST", "", json=data)
    
    def get_record(self, record_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a record by ID.
        
        Args:
            record_id: Record ID
            
        Returns:
            Record data or None if not found
        """
        try:
            return self._make_request("GET", f"/{record_id}")
        except Exception:
            return None
    
    def list_records(self, where: Optional[str] = None, limit: int = 25, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List records with optional filtering.
        
        Args:
            where: Filter condition (e.g., "(email,eq,test@example.com)")
            limit: Number of records to return
            offset: Number of records to skip
            
        Returns:
            List of records
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if where:
            params["where"] = where
        
        response = self._make_request("GET", "", params=params)
        return response.get("list", [])
    
    def update_record(self, record_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a record.
        
        Args:
            record_id: Record ID
            data: Updated data
            
        Returns:
            Updated record
        """
        return self._make_request("PATCH", f"/{record_id}", json=data)
    
    def delete_record(self, record_id: int) -> bool:
        """
        Delete a record.
        
        Args:
            record_id: Record ID
            
        Returns:
            True if successful
        """
        try:
            self._make_request("DELETE", f"/{record_id}")
            return True
        except Exception:
            return False
    
    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Find a candidate by email.
        
        Args:
            email: Email address
            
        Returns:
            Candidate record or None
        """
        # NocoDB where clause format: (field,operator,value)
        where = f"(email,eq,{email})"
        records = self.list_records(where=where, limit=1)
        return records[0] if records else None


# Global database client instance
db = NocoDBClient()


# Helper functions for common operations
def create_candidate(email: str, first_name: str, last_name: str, password: str) -> Dict[str, Any]:
    """
    Create a new candidate record.
    
    Args:
        email: Candidate email
        first_name: Candidate first name
        last_name: Candidate last name
        password: Plain text password (will be base64 encoded)
        
    Returns:
        Created candidate record
    """
    import base64
    
    # Encode password to base64
    password_encoded = base64.b64encode(password.encode()).decode()
    
    data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password_encoded,
        "created_at": None  # Auto-filled by NocoDB
    }
    return db.create_record(data)


def get_candidate_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Get candidate by email.
    
    Args:
        email: Candidate email
        
    Returns:
        Candidate record or None
    """
    return db.find_by_email(email)


def get_candidate_by_id(candidate_id: int) -> Optional[Dict[str, Any]]:
    """
    Get candidate by ID.
    
    Args:
        candidate_id: Candidate ID
        
    Returns:
        Candidate record or None
    """
    return db.get_record(candidate_id)


def update_candidate(candidate_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update candidate record.
    
    Args:
        candidate_id: Candidate ID
        data: Updated data
        
    Returns:
        Updated candidate record
    """
    return db.update_record(candidate_id, data)
