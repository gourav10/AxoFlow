from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    current_company: Optional[str] = None
    current_title: Optional[str] = None
    years_of_experience: Optional[int] = None
    skills: Optional[list[str]] = []
    resume_url: Optional[str] = None

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    current_company: Optional[str] = None
    current_title: Optional[str] = None
    years_of_experience: Optional[int] = None
    skills: Optional[list[str]] = None
