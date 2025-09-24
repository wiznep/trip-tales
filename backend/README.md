# Trip Tales Backend API

A FastAPI backend for the Trip Tales Pro application, providing RESTful APIs for user management, trip creation, media upload, and AI-powered video generation.

## Features

- 🔐 **User Authentication** - JWT-based authentication system
- 📸 **Media Upload** - Support for images and videos with file validation
- 🗺️ **Trip Management** - CRUD operations for travel trips
- 🤖 **AI Integration** - Video generation from uploaded media and prompts
- 📊 **Database** - MySQL integration with SQLAlchemy ORM
- 📚 **API Documentation** - Automatic OpenAPI/Swagger documentation
- 🚀 **Async Support** - Built with FastAPI for high performance

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── users.py      # User authentication endpoints
│   │       │   ├── trips.py      # Trip CRUD endpoints
│   │       │   ├── upload.py     # File upload endpoints
│   │       │   └── ai.py         # AI video generation endpoints
│   │       └── api.py            # API router configuration
│   ├── core/
│   │   ├── config.py             # Application settings
│   │   └── security.py           # Authentication utilities
│   ├── crud/
│   │   ├── user.py               # User database operations
│   │   ├── trip.py               # Trip database operations
│   │   └── media.py              # Media file database operations
│   ├── models/
│   │   ├── user.py               # User SQLAlchemy model
│   │   ├── trip.py               # Trip SQLAlchemy model
│   │   └── media.py              # Media file SQLAlchemy model
│   ├── schemas/
│   │   ├── user.py               # User Pydantic schemas
│   │   ├── trip.py               # Trip Pydantic schemas
│   │   └── media.py              # Media file Pydantic schemas
│   └── database.py               # Database configuration
├── uploads/                      # Media file storage
├── main.py                       # FastAPI application entry point
├── create_tables.py              # Database table creation script
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
└── README.md                     # This file
```

## Setup Instructions

### Prerequisites

- Python 3.13.7
- MySQL 8.0+
- pip (Python package manager)

### Manual Setup

1. **Clone and navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create environment file**
   ```bash
   copy .env.example .env
   ```

3. **Modify .env file**
   Update `.env` file with your database credentials:
   ```env
   DATABASE_URL=mysql+pymysql://your_user:your_password@localhost:3306/trip_tales_db
   SECRET_KEY=your-super-secret-key-change-in-production
   ```

4. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

5. **Activate virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **Unix/Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```

6. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

7. **Create uploads directory**
   ```bash
   mkdir uploads
   ```

8. **Create MySQL database**
   ```sql
   CREATE DATABASE trip_tales_db;
   ```

9. **Initialize database tables**
   ```bash
   python create_tables.py
   ```

10. **Start the development server**
    ```bash
    uvicorn main:app --reload
    ```

## API Documentation

Once the server is running, you can access:

- **Interactive API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative Documentation (ReDoc):** http://localhost:8000/redoc
- **OpenAPI JSON Schema:** http://localhost:8000/api/v1/openapi.json


