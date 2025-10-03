import os
import asyncio
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils.video_processor import VideoProcessor
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate-video/", response_model=schemas.Trip)
async def generate_video(
    *,
    db: Session = Depends(deps.get_db),
    trip_id: int,
    prompt: str = None,
    style: str = "cinematic",
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate AI video from trip media files
    """
    # Get trip
    trip = crud.trip.get(db=db, id=trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Verify ownership
    if trip.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this trip")
    
    # Get media files
    media_files = crud.media_file.get_by_trip(db=db, trip_id=trip_id)
    if not media_files:
        raise HTTPException(
            status_code=400,
            detail="No media files found for this trip"
        )
    
    # Update trip status
    trip_update = schemas.TripUpdate(
        status="processing",
        prompt=prompt,
        style=style
    )
    trip = crud.trip.update(db=db, db_obj=trip, obj_in=trip_update)
    
    # Start background video generation
    background_tasks.add_task(
        process_video_generation,
        db=db,
        trip_id=trip_id,
        media_files=media_files,
        title=trip.title or "My Travel Story",
        style=style
    )
    
    return trip


def process_video_generation(
    db: Session,
    trip_id: int,
    media_files: list,
    title: str,
    style: str
):
    """
    Background task to process video generation using OpenCV
    """
    try:
        logger.info(f"Starting video generation for trip {trip_id}")
        
        # Prepare output path
        output_filename = f"trip_{trip_id}_{style}.mp4"
        output_path = os.path.join(settings.UPLOAD_DIR, output_filename)
        
        # Prepare media files list
        media_list = []
        for media in media_files:
            media_list.append({
                'path': media.file_path,
                'type': media.file_type,
                'filename': media.filename
            })
        
        # Sort by creation time (if available) or by filename
        media_list.sort(key=lambda x: x['filename'])
        
        # Create video processor with style
        processor = VideoProcessor(
            output_path=output_path,
            fps=settings.VIDEO_FPS,
            resolution=settings.VIDEO_RESOLUTION,
            codec=settings.VIDEO_CODEC,
            style=style  # Pass style parameter
        )
        
        # Generate video
        success = processor.create_video_from_media(
            media_files=media_list,
            title=title,
            add_intro=True,
            add_outro=True
        )
        
        if success:
            # Update trip with generated video URL
            video_url = f"/uploads/{output_filename}"
            trip_update = schemas.TripUpdate(
                generated_video_url=video_url,
                status="completed"
            )
            
            # Get fresh trip object
            trip = crud.trip.get(db=db, id=trip_id)
            crud.trip.update(db=db, db_obj=trip, obj_in=trip_update)
            
            logger.info(f"Video generation completed for trip {trip_id}")
        else:
            raise Exception("Video generation failed")
        
    except Exception as e:
        logger.error(f"Error generating video for trip {trip_id}: {str(e)}")
        
        # Update trip status to failed
        trip = crud.trip.get(db=db, id=trip_id)
        trip_update = schemas.TripUpdate(status="failed")
        crud.trip.update(db=db, db_obj=trip, obj_in=trip_update)


@router.get("/status/{trip_id}")
async def get_generation_status(
    *,
    db: Session = Depends(deps.get_db),
    trip_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get video generation status
    """
    trip = crud.trip.get(db=db, id=trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    if trip.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return {
        "status": trip.status,
        "video_url": trip.generated_video_url,
        "title": trip.title
    }


@router.get("/video/{trip_id}")
async def get_video(
    *,
    db: Session = Depends(deps.get_db),
    trip_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get generated video details
    """
    trip = crud.trip.get(db=db, id=trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    if trip.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if not trip.generated_video_url:
        raise HTTPException(status_code=404, detail="Video not generated yet")
    
    return {
        "video_url": trip.generated_video_url,
        "status": trip.status,
        "title": trip.title,
        "style": trip.style
    }