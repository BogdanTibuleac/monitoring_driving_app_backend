from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.services.vehicle_service import VehicleService
from app.core.dependencies import get_vehicle_service
from app.data.schemas.models import Vehicle

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=List[Vehicle])
async def list_vehicles(vehicle_service: VehicleService = Depends(get_vehicle_service)):
    try:
        return await vehicle_service.get_all_vehicles()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch vehicles: {str(e)}")


@router.get("/{vehicle_id}", response_model=Vehicle)
async def get_vehicle(vehicle_id: int, vehicle_service: VehicleService = Depends(get_vehicle_service)):
    vehicle = await vehicle_service.get_vehicle_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.post("/", response_model=Vehicle, status_code=201)
async def create_vehicle(
    make: str,
    model: str,
    year: int,
    type: Optional[str] = None,
    vehicle_service: VehicleService = Depends(get_vehicle_service),
):
    try:
        return await vehicle_service.create_vehicle(make, model, year, type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create vehicle: {str(e)}")


@router.patch("/{vehicle_id}", response_model=Vehicle)
async def update_vehicle(
    vehicle_id: int,
    updates: dict,
    vehicle_service: VehicleService = Depends(get_vehicle_service),
):
    vehicle = await vehicle_service.update_vehicle(vehicle_id, updates)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.delete("/{vehicle_id}", status_code=204)
async def delete_vehicle(vehicle_id: int, vehicle_service: VehicleService = Depends(get_vehicle_service)):
    success = await vehicle_service.delete_vehicle(vehicle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return None
