from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MediaFileBase(BaseModel):
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    file_type: str

class MediaFileCreate(MediaFileBase):
    file_path: str
    trip_id: int

class MediaFileUpdate(BaseModel):
    filename: Optional[str] = None

class MediaFileInDBBase(MediaFileBase):
    id: int
    file_path: str
    trip_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

class MediaFile(MediaFileInDBBase):
    pass