from fastapi import APIRouter, HTTPException, status, UploadFile, File
from app.models.user import UserProfile, UserProfileUpdate
from app.models.application import Application, ApplicationCreate, ApplicationUpdate, ApplicationWithJob, ApplicationStatus
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api", tags=["users", "applications"])

# Placeholder data stores (in-memory)
profiles_db = {
    1: {
        "id": 1,
        "email": "demo@axoflow.com",
        "full_name": "Demo User",
        "phone": "+1-555-0123",
        "current_company": "TechCorp",
        "current_title": "Software Engineer",
        "years_of_experience": 5,
        "skills": ["Python", "FastAPI", "React", "AWS"],
        "resume_url": None
    }
}

applications_db = {}
next_app_id = 1


# User Profile Endpoints
@router.get("/users/profile", response_model=UserProfile)
async def get_user_profile():
    """
    Get current user's profile (placeholder implementation).
    
    In production, this would:
    - Get user ID from JWT token
    - Query database for profile
    """
    # Return demo profile
    if 1 in profiles_db:
        return UserProfile(**profiles_db[1])
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Profile not found"
    )


@router.put("/users/profile", response_model=UserProfile)
async def update_user_profile(profile_update: UserProfileUpdate):
    """
    Update current user's profile (placeholder implementation).
    
    In production, this would:
    - Get user ID from JWT token
    - Update database
    - Return updated profile
    """
    if 1 not in profiles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update profile with provided fields
    profile = profiles_db[1]
    update_data = profile_update.model_dump(exclude_unset=True)
    profile.update(update_data)
    
    return UserProfile(**profile)


@router.post("/users/resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload user's resume (placeholder implementation).
    
    In production, this would:
    - Validate file type (PDF, DOCX)
    - Upload to cloud storage (S3, etc.)
    - Update user profile with resume URL
    - Extract text for AI processing
    """
    # Placeholder: just return file info
    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "content_type": file.content_type,
        "resume_url": f"/uploads/resumes/{file.filename}"
    }


# Application Endpoints
@router.get("/applications", response_model=List[ApplicationWithJob])
async def list_applications():
    """
    List current user's applications (placeholder implementation).
    
    In production, this would:
    - Get user ID from JWT token
    - Query database with joins
    - Return applications with job details
    """
    # Return placeholder applications with job info
    results = []
    for app in applications_db.values():
        # Mock job data
        app_with_job = {
            **app,
            "job_title": "Software Engineer",
            "company": "TechCorp",
            "job_location": "San Francisco, CA"
        }
        results.append(ApplicationWithJob(**app_with_job))
    
    return results


@router.post("/applications", response_model=Application, status_code=status.HTTP_201_CREATED)
async def create_application(application: ApplicationCreate):
    """
    Submit a new job application (placeholder implementation).
    
    In production, this would:
    - Get user ID from JWT token
    - Validate job exists
    - Check for duplicate applications
    - Store in database
    - Trigger automation workflow
    """
    global next_app_id
    
    app_id = next_app_id
    next_app_id += 1
    
    now = datetime.now()
    app_data = {
        "id": app_id,
        "user_id": 1,  # Placeholder user ID
        **application.model_dump(),
        "status": ApplicationStatus.PENDING,
        "submitted_at": None,
        "created_at": now,
        "updated_at": now
    }
    
    applications_db[app_id] = app_data
    
    return Application(**app_data)


@router.get("/applications/{app_id}", response_model=Application)
async def get_application(app_id: int):
    """
    Get application status by ID (placeholder implementation).
    
    In production, this would:
    - Verify user owns this application
    - Query database
    - Return application details
    """
    if app_id not in applications_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    return Application(**applications_db[app_id])


@router.put("/applications/{app_id}", response_model=Application)
async def update_application(app_id: int, update: ApplicationUpdate):
    """
    Update application (placeholder implementation).
    
    In production, this would:
    - Verify user owns this application
    - Update database
    - Log status changes
    - Send notifications
    """
    if app_id not in applications_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    app = applications_db[app_id]
    update_data = update.model_dump(exclude_unset=True)
    app.update(update_data)
    app["updated_at"] = datetime.now()
    
    if update.status == ApplicationStatus.SUBMITTED and not app.get("submitted_at"):
        app["submitted_at"] = datetime.now()
    
    return Application(**app)
