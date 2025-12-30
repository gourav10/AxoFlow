# AxoFlow Backend - FastAPI Service

## Overview

This is the backend API service for AxoFlow, a Job Copilot application that automates job applications.

## Features

- **Authentication**: User registration, login, and session management
- **Job Management**: Browse, search, and filter job listings
- **Applications**: Submit and track job applications
- **User Profiles**: Manage user information and resumes

## Tech Stack

- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and settings
- **Uvicorn**: ASGI server

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Navigate to backend directory
cd src/backend

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Or run directly
python -m app.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication (`/api/auth`)
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user

### Jobs (`/api/jobs`)
- `GET /api/jobs` - List jobs (with pagination)
- `GET /api/jobs/{job_id}` - Get job details
- `POST /api/jobs/search` - Search jobs
- `POST /api/jobs` - Create job posting

### Applications (`/api/applications`)
- `GET /api/applications` - List user applications
- `POST /api/applications` - Submit application
- `GET /api/applications/{app_id}` - Get application status
- `PUT /api/applications/{app_id}` - Update application

### Users (`/api/users`)
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update profile
- `POST /api/users/resume` - Upload resume

## Current Status

**Note**: This is a placeholder implementation with in-memory data storage. All endpoints return mock data and do not persist to a database.

### Next Steps for Production

1. **Database Integration**: Add PostgreSQL/MySQL with SQLAlchemy ORM
2. **Authentication**: Implement JWT tokens with proper password hashing
3. **File Storage**: Integrate S3 or similar for resume uploads
4. **Job Scraping**: Add job board integration (LinkedIn, Indeed, etc.)
5. **AI Integration**: Connect to LLM for application automation
6. **Testing**: Add unit and integration tests
7. **Deployment**: Containerize with Docker

## Development

### Project Structure

```
src/backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings and configuration
│   ├── models/              # Pydantic models
│   │   ├── user.py
│   │   ├── job.py
│   │   └── application.py
│   ├── routers/             # API endpoints
│   │   ├── auth.py
│   │   ├── jobs.py
│   │   └── users.py
│   └── utils/               # Utility functions
└── requirements.txt
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./axoflow.db
```

## License

See main project LICENSE file.
