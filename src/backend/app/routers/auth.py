from fastapi import APIRouter, HTTPException, status
from app.models.user import UserCreate, UserLogin, User
from app.database import create_candidate, get_candidate_by_email, get_candidate_by_id
from app.utils.auth import verify_password
from datetime import datetime

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """
    Register a new user.
    
    Creates a new candidate record in NocoDB with base64-encoded password.
    """
    # Check if user already exists
    existing_user = get_candidate_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Split full_name into first_name and last_name
    name_parts = user.full_name.strip().split(maxsplit=1)
    first_name = name_parts[0] if len(name_parts) > 0 else ""
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    
    # Create candidate in NocoDB with password
    try:
        candidate = create_candidate(
            email=user.email,
            first_name=first_name,
            last_name=last_name,
            password=user.password
        )
        
        # Return user data (without password)
        return User(
            id=candidate.get("Id"),
            email=candidate.get("email"),
            full_name=f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}".strip(),
            created_at=candidate.get("created_at") or datetime.now(),
            is_active=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.post("/login")
async def login(credentials: UserLogin):
    """
    Login user.
    
    Authenticates user by verifying password against base64-encoded version in database.
    """
    # Find user by email
    candidate = get_candidate_by_email(credentials.email)
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    stored_password = candidate.get("password", "")
    if not verify_password(credentials.password, stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Return token and user info
    user = User(
        id=candidate.get("Id"),
        email=candidate.get("email"),
        full_name=f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}".strip(),
        created_at=candidate.get("created_at") or datetime.now(),
        is_active=True
    )
    
    return {
        "access_token": f"mock_token_{candidate.get('Id')}",
        "token_type": "bearer",
        "user": user
    }


@router.post("/logout")
async def logout():
    """
    Logout user.
    
    In production, this would invalidate the JWT token.
    """
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=User)
async def get_current_user():
    """
    Get current authenticated user.
    
    In production, this would verify JWT token and return user from database.
    For now, returns a demo user.
    """
    # TODO: Get user ID from JWT token
    # For now, return demo user
    demo_email = "demo@axoflow.com"
    candidate = get_candidate_by_email(demo_email)
    
    if not candidate:
        # Create demo user if doesn't exist
        try:
            candidate = create_candidate(
                email=demo_email,
                first_name="Demo",
                last_name="User",
                password="demo123"
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get current user"
            )
    
    return User(
        id=candidate.get("Id"),
        email=candidate.get("email"),
        full_name=f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}".strip(),
        created_at=candidate.get("created_at") or datetime.now(),
        is_active=True
    )

