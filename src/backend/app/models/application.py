from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ApplicationStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class ApplicationBase(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None
    custom_resume: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class Application(ApplicationBase):
    id: int
    user_id: int
    status: ApplicationStatus = ApplicationStatus.PENDING
    submitted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    cover_letter: Optional[str] = None
    custom_resume: Optional[str] = None


class ApplicationWithJob(Application):
    job_title: str
    company: str
    job_location: str
