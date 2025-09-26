from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime
from datetime import date
from app.services.trip_service import TripService
from app.core.dependencies import get_trip_service
from app.data.schemas.models import FactTrip
from sqlmodel import SQLModel

router = APIRouter(prefix="/trips", tags=["trips"])


# -------------------------
# Schemas for dashbaord driver info, Trip with Locations for joining tables
# -------------------------
class TripSummary(SQLModel):
    total_trips: int
    avg_safety_score: float
    avg_eco_score: float

class TripWithLocations(SQLModel):
    trip_id: int
    driver_id: int
    vehicle_id: int
    distance_km: Optional[float]
    avg_speed: Optional[float]
    harsh_events: Optional[int]
    eco_score: Optional[float]
    safety_score: Optional[float]
    trip_duration_sec: Optional[int]
    max_speed: Optional[float]
    date:  Optional[date]
    origin_name: Optional[str]
    destination_name: Optional[str]

class WeeklyTrend(SQLModel):
    weekday: int
    avg_safety: Optional[float]
    avg_eco: Optional[float]
# -------------------------
# Routes
# -------------------------
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


@router.get("/driver/{driver_id}", response_model=List[TripWithLocations])
async def get_trips_for_driver(
    driver_id: int,
    trip_service: TripService = Depends(get_trip_service)
):
    return await trip_service.get_trips_by_driver(driver_id)


@router.get("/driver/{driver_id}/summary", response_model=TripSummary)
async def get_trips_summary_for_driver(
    driver_id: int,
    trip_service: TripService = Depends(get_trip_service)
):
    return await trip_service.get_trips_summary_by_driver(driver_id)

@router.get("/analytics/driver/{driver_id}/weekly", response_model=List[WeeklyTrend])
async def get_weekly_trends_for_driver(
    driver_id: int,
    trip_service: TripService = Depends(get_trip_service)
):
    return await trip_service.get_weekly_trends(driver_id)
