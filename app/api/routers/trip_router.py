from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime
from app.services.trip_service import TripService
from app.core.dependencies import get_trip_service
from app.data.schemas.models import FactTrip

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("/", response_model=List[FactTrip])
async def list_trips(trip_service: TripService = Depends(get_trip_service)):
    try:
        return await trip_service.get_all_trips()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch trips: {str(e)}")


@router.get("/{trip_id}", response_model=FactTrip)
async def get_trip(trip_id: int, trip_service: TripService = Depends(get_trip_service)):
    trip = await trip_service.get_trip_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.post("/", response_model=FactTrip, status_code=201)
async def create_trip(
    driver_id: int,
    vehicle_id: int,
    distance_km: float,
    avg_speed: float,
    harsh_events: int,
    eco_score: float,
    safety_score: float,
    trip_duration_sec: int,
    max_speed: float,
    timestamp: Optional[datetime] = None,
    trip_service: TripService = Depends(get_trip_service),
):
    try:
        return await trip_service.create_trip(
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            distance_km=distance_km,
            avg_speed=avg_speed,
            harsh_events=harsh_events,
            eco_score=eco_score,
            safety_score=safety_score,
            trip_duration_sec=trip_duration_sec,
            max_speed=max_speed,
            timestamp=timestamp,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create trip: {str(e)}")


@router.delete("/{trip_id}", status_code=204)
async def delete_trip(trip_id: int, trip_service: TripService = Depends(get_trip_service)):
    success = await trip_service.delete_trip(trip_id)
    if not success:
        raise HTTPException(status_code=404, detail="Trip not found")
    return None
