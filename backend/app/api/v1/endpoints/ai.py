from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from pydantic import BaseModel

router = APIRouter()

class VideoGenerationRequest(BaseModel):
    trip_id: int
    prompt: str
    style: str = "cinematic"

class VideoGenerationResponse(BaseModel):
    message: str
    trip_id: int
    status: str

@router.post("/generate-video/", response_model=VideoGenerationResponse)
async def generate_video(
    *,
    db: Session = Depends(deps.get_db),
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Generate video from trip media and prompt."""
    # Verify trip ownership
    trip = crud.trip.get(db=db, id=request.trip_id)
    if not trip or trip.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Get trip media files
    media_files = crud.media_file.get_by_trip(db=db, trip_id=request.trip_id)
    if not media_files:
        raise HTTPException(status_code=400, detail="No media files found for this trip")
    
    # Update trip with prompt and style
    trip_update = schemas.TripUpdate(
        prompt=request.prompt,
        style=request.style,
        status="processing"
    )
    crud.trip.update(db=db, db_obj=trip, obj_in=trip_update)
    
    # Add background task for video generation
    background_tasks.add_task(
        process_video_generation,
        db,
        request.trip_id,
        request.prompt,
        request.style,
        media_files
    )
    
    return VideoGenerationResponse(
        message="Video generation started",
        trip_id=request.trip_id,
        status="processing"
    )

async def process_video_generation(
    db: Session,
    trip_id: int,
    prompt: str,
    style: str,
    media_files: List[models.MediaFile]
):
    """Background task to process video generation."""
    try:
        # TODO: Implement actual AI video generation logic here
        # For now, simulate processing time and return a placeholder
        import asyncio
        await asyncio.sleep(10)  # Simulate processing time
        
        # Update trip with generated video URL (placeholder)
        video_url = f"/api/v1/videos/{trip_id}/generated.mp4"
        trip_update = schemas.TripUpdate(
            generated_video_url=video_url,
            status="completed"
        )
        
        trip = crud.trip.get(db=db, id=trip_id)
        crud.trip.update(db=db, db_obj=trip, obj_in=trip_update)
        
    except Exception as e:
        # Update trip status to failed
        trip_update = schemas.TripUpdate(status="failed")
        trip = crud.trip.get(db=db, id=trip_id)
        crud.trip.update(db=db, db_obj=trip, obj_in=trip_update)

@router.get("/status/{trip_id}")
def get_generation_status(
    *,
    db: Session = Depends(deps.get_db),
    trip_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Get video generation status for a trip."""
    trip = crud.trip.get(db=db, id=trip_id)
    if not trip or trip.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    return {
        "trip_id": trip_id,
        "status": trip.status,
        "generated_video_url": trip.generated_video_url
    }