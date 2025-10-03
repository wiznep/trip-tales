from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import os
from pathlib import Path
from sqlalchemy.orm import Session

from app.api.v1.api import api_router
from app.core.config import settings
from app.database import SessionLocal  # ← FIXED
from app import crud, models, schemas
from app.api import deps

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Mount static files for serving videos and images
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Trip Tales API is running!",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "trip-tales-api"}

@app.post("/upload/")
async def upload_files(
    files: List[UploadFile] = File(...),
    trip_id: int = Form(None),
    db: Session = Depends(deps.get_db)
):
    """
    Upload media files (images/videos)
    Optional: Link to a trip_id if provided
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    saved_files = []
    
    for file in files:
        try:
            # Validate file type
            if not file.content_type:
                continue
            
            allowed_types = [
                "image/jpeg", "image/jpg", "image/png", "image/gif",
                "video/mp4", "video/quicktime", "video/x-msvideo"
            ]
            
            if file.content_type not in allowed_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type {file.content_type} not allowed"
                )
            
            # Save file
            file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
            
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # If trip_id provided, create MediaFile record
            if trip_id:
                file_type = "video" if file.content_type.startswith("video") else "image"
                
                media_in = schemas.MediaFileCreate(
                    filename=file.filename,
                    original_filename=file.filename,
                    file_path=file_path,
                    file_size=len(content),
                    mime_type=file.content_type,
                    file_type=file_type,
                    trip_id=trip_id
                )
                
                crud.media_file.create(db=db, obj_in=media_in)
            
            saved_files.append(file.filename)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error uploading file {file.filename}: {str(e)}"
            )
    
    return {
        "uploaded": saved_files,
        "count": len(saved_files)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)