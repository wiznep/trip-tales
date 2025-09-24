from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.trip import Trip
from app.schemas.trip import TripCreate, TripUpdate

class CRUDTrip(CRUDBase[Trip, TripCreate, TripUpdate]):
    def get_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Trip]:
        return (
            db.query(self.model)
            .filter(Trip.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_with_owner(
        self, db: Session, *, obj_in: TripCreate, owner_id: int
    ) -> Trip:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

trip = CRUDTrip(Trip)