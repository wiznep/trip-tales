from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .media import MediaFile

class TripBase(BaseModel):
    title: str
    description: Optional[str] = None
    destination: Optional[str] = None
    prompt: Optional[str] = None
    style: Optional[str] = None

class TripCreate(TripBase):
    pass

class TripUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    destination: Optional[str] = None
    prompt: Optional[str] = None
    style: Optional[str] = None
    status: Optional[str] = None
    generated_video_url: Optional[str] = None

class TripInDBBase(TripBase):
    id: int
    status: str
    generated_video_url: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Trip(TripInDBBase):
    media_files: List[MediaFile] = []

class TripInDB(TripInDBBase):
    pass