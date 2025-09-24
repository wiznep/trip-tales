import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
import aiofiles

router = APIRouter()

@router.post("/files/", response_model=List[schemas.MediaFile])
async def upload_files(
    *,
    db: Session = Depends(deps.get_db),
    trip_id: int = Form(...),
    files: List[UploadFile] = File(...),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Upload multiple files for a trip."""
    # Verify trip ownership
    trip = crud.trip.get(db=db, id=trip_id)
    if not trip or trip.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    uploaded_files = []
    
    for file in files:
        # Validate file type
        if file.content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file.content_type} not allowed"
            )
        
        # Validate file size
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes"
            )
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Determine file type
        file_type = "image" if file.content_type.startswith("image/") else "video"
        
        # Save to database
        media_file_in = schemas.MediaFileCreate(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type,
            file_type=file_type,
            trip_id=trip_id
        )
        
        media_file = crud.media_file.create_with_trip(db=db, obj_in=media_file_in)
        uploaded_files.append(media_file)
    
    return uploaded_files

@router.get("/trips/{trip_id}/files/", response_model=List[schemas.MediaFile])
def get_trip_files(
    *,
    db: Session = Depends(deps.get_db),
    trip_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Get all files for a trip."""
    trip = crud.trip.get(db=db, id=trip_id)
    if not trip or trip.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    files = crud.media_file.get_by_trip(db=db, trip_id=trip_id)
    return files

@router.delete("/files/{file_id}")
async def delete_file(
    *,
    db: Session = Depends(deps.get_db),
    file_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Delete a media file."""
    media_file = crud.media_file.get(db=db, id=file_id)
    if not media_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if user owns the trip
    trip = crud.trip.get(db=db, id=media_file.trip_id)
    if not trip or trip.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    # Delete file from filesystem
    try:
        os.remove(media_file.file_path)
    except FileNotFoundError:
        pass  # File already deleted from filesystem
    
    # Delete from database
    crud.media_file.remove(db=db, id=file_id)
    return {"message": "File deleted successfully"}