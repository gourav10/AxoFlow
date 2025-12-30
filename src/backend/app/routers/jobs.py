from fastapi import APIRouter, HTTPException, status
from app.models.job import Job, JobCreate, JobSearch, JobType, JobStatus
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

# Placeholder data store (in-memory)
jobs_db = {
    1: {
        "id": 1,
        "title": "Senior Software Engineer",
        "company": "TechCorp",
        "location": "San Francisco, CA",
        "job_type": JobType.FULL_TIME,
        "description": "We are looking for a senior software engineer...",
        "requirements": ["5+ years Python", "FastAPI experience", "AWS knowledge"],
        "salary_range": "$150k - $200k",
        "url": "https://example.com/jobs/1",
        "status": JobStatus.ACTIVE,
        "created_at": datetime.now(),
        "posted_date": datetime.now()
    },
    2: {
        "id": 2,
        "title": "Frontend Developer",
        "company": "StartupXYZ",
        "location": "Remote",
        "job_type": JobType.FULL_TIME,
        "description": "Join our team to build amazing user experiences...",
        "requirements": ["React", "TypeScript", "Tailwind CSS"],
        "salary_range": "$120k - $160k",
        "url": "https://example.com/jobs/2",
        "status": JobStatus.ACTIVE,
        "created_at": datetime.now(),
        "posted_date": datetime.now()
    },
    3: {
        "id": 3,
        "title": "DevOps Engineer",
        "company": "CloudSolutions Inc",
        "location": "New York, NY",
        "job_type": JobType.CONTRACT,
        "description": "Looking for an experienced DevOps engineer...",
        "requirements": ["Kubernetes", "Docker", "CI/CD", "Terraform"],
        "salary_range": "$140k - $180k",
        "url": "https://example.com/jobs/3",
        "status": JobStatus.ACTIVE,
        "created_at": datetime.now(),
        "posted_date": datetime.now()
    }
}
next_job_id = 4


@router.get("", response_model=List[Job])
async def list_jobs(skip: int = 0, limit: int = 10):
    """
    List all available jobs (placeholder implementation).
    
    In production, this would:
    - Query database with pagination
    - Filter by active status
    - Sort by relevance/date
    """
    jobs = list(jobs_db.values())[skip:skip + limit]
    return [Job(**job) for job in jobs]


@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: int):
    """
    Get job details by ID (placeholder implementation).
    
    In production, this would:
    - Query database for specific job
    - Include related data (company info, etc.)
    """
    if job_id not in jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return Job(**jobs_db[job_id])


@router.post("/search", response_model=List[Job])
async def search_jobs(search: JobSearch):
    """
    Search for jobs based on criteria (placeholder implementation).
    
    In production, this would:
    - Use full-text search (Elasticsearch, etc.)
    - Apply filters and sorting
    - Return ranked results
    """
    results = []
    
    for job in jobs_db.values():
        # Simple placeholder filtering
        if search.query and search.query.lower() not in job["title"].lower():
            continue
        if search.location and search.location.lower() not in job["location"].lower():
            continue
        if search.job_type and job["job_type"] != search.job_type:
            continue
        if search.company and search.company.lower() not in job["company"].lower():
            continue
        
        results.append(Job(**job))
    
    return results


@router.post("", response_model=Job, status_code=status.HTTP_201_CREATED)
async def create_job(job: JobCreate):
    """
    Create a new job posting (placeholder implementation).
    
    In production, this would:
    - Validate user permissions (admin/recruiter only)
    - Store in database
    - Send notifications
    """
    global next_job_id
    
    job_id = next_job_id
    next_job_id += 1
    
    job_data = {
        "id": job_id,
        **job.model_dump(),
        "status": JobStatus.ACTIVE,
        "created_at": datetime.now(),
        "posted_date": datetime.now()
    }
    
    jobs_db[job_id] = job_data
    
    return Job(**job_data)
