from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.media import MediaFile
from app.schemas.media import MediaFileCreate, MediaFileUpdate

class CRUDMediaFile(CRUDBase[MediaFile, MediaFileCreate, MediaFileUpdate]):
    def get_by_trip(
        self, db: Session, *, trip_id: int
    ) -> List[MediaFile]:
        return db.query(self.model).filter(MediaFile.trip_id == trip_id).all()
    
    def create_with_trip(
        self, db: Session, *, obj_in: MediaFileCreate
    ) -> MediaFile:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

media_file = CRUDMediaFile(MediaFile)