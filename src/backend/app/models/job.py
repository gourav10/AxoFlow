from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from enum import Enum


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class JobStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"


class JobBase(BaseModel):
    title: str
    company: str
    location: str
    job_type: JobType
    description: str
    requirements: list[str]
    salary_range: Optional[str] = None
    url: HttpUrl


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    status: JobStatus = JobStatus.ACTIVE
    created_at: datetime
    posted_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobSearch(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    company: Optional[str] = None
