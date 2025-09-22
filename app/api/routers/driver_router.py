from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.services.driver_service import DriverService
from app.core.dependencies import get_driver_service
from app.data.schemas.models import Driver

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.get("/", response_model=List[Driver])
async def list_drivers(driver_service: DriverService = Depends(get_driver_service)):
    try:
        return await driver_service.get_all_drivers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch drivers: {str(e)}")


@router.get("/{driver_id}", response_model=Driver)
async def get_driver(driver_id: int, driver_service: DriverService = Depends(get_driver_service)):
    driver = await driver_service.get_driver_by_id(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.post("/", response_model=Driver, status_code=201)
async def create_driver(
    name: str,
    license_type: Optional[str] = None,
    driver_service: DriverService = Depends(get_driver_service),
):
    try:
        return await driver_service.create_driver(name, license_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create driver: {str(e)}")


@router.patch("/{driver_id}", response_model=Driver)
async def update_driver(
    driver_id: int,
    updates: dict,
    driver_service: DriverService = Depends(get_driver_service),
):
    driver = await driver_service.update_driver(driver_id, updates)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.delete("/{driver_id}", status_code=204)
async def delete_driver(driver_id: int, driver_service: DriverService = Depends(get_driver_service)):
    success = await driver_service.delete_driver(driver_id)
    if not success:
        raise HTTPException(status_code=404, detail="Driver not found")
    return None
