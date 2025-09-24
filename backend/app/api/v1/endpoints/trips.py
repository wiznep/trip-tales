from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Trip])
def read_trips(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Retrieve trips for current user."""
    trips = crud.trip.get_by_owner(db=db, owner_id=current_user.id, skip=skip, limit=limit)
    return trips
    # """Retrieve all trips (no auth)."""
    # trips = crud.trip.get_multi(db=db, skip=skip, limit=limit)  # Get all trips
    # return trips

@router.post("/", response_model=schemas.Trip)
def create_trip(
    *,
    db: Session = Depends(deps.get_db),
    trip_in: schemas.TripCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Create new trip."""
    trip = crud.trip.create_with_owner(db=db, obj_in=trip_in, owner_id=current_user.id)
    return trip

@router.get("/{trip_id}", response_model=schemas.Trip)
def read_trip(
    *,
    db: Session = Depends(deps.get_db),
    trip_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get trip by ID."""
    trip = crud.trip.get(db=db, id=trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return trip

@router.put("/{trip_id}", response_model=schemas.Trip)
def update_trip(
    *,
    db: Session = Depends(deps.get_db),
    trip_id: int,
    trip_in: schemas.TripUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Update a trip."""
    trip = crud.trip.get(db=db, id=trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    trip = crud.trip.update(db=db, db_obj=trip, obj_in=trip_in)
    return trip

@router.delete("/{trip_id}")
def delete_trip(
    *,
    db: Session = Depends(deps.get_db),
    trip_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Delete a trip."""
    trip = crud.trip.get(db=db, id=trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    trip = crud.trip.remove(db=db, id=trip_id)
    return {"message": "Trip deleted successfully"}