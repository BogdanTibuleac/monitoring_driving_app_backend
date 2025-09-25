from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.services.emergency_service import EmergencyService
from app.core.dependencies import get_emergency_service
from app.data.schemas.models import EmergencyNumber, Emergency

router = APIRouter(prefix="/emergency", tags=["emergency"])


# -------------------------
# Global emergency numbers
# -------------------------
@router.get("/numbers", response_model=List[EmergencyNumber])
async def list_numbers(emergency_service: EmergencyService = Depends(get_emergency_service)):
    return await emergency_service.get_all_numbers()


@router.get("/numbers/{country_code}", response_model=EmergencyNumber)
async def get_number(country_code: str, emergency_service: EmergencyService = Depends(get_emergency_service)):
    number = await emergency_service.get_number_by_country(country_code)
    if not number:
        raise HTTPException(status_code=404, detail="Country code not found")
    return number


# -------------------------
# Driver emergency profile
# -------------------------
@router.post("/profile", response_model=Emergency, status_code=201)
async def create_or_update_profile(
    driver_id: int,
    auto_contact_enabled: bool,
    emergency_country_code: Optional[str] = None,
    share_location: Optional[bool] = None,
    share_medical_info: Optional[bool] = None,
    emergency_service: EmergencyService = Depends(get_emergency_service),
):
    try:
        return await emergency_service.create_or_update_profile(
            driver_id=driver_id,
            auto_contact_enabled=auto_contact_enabled,
            emergency_country_code=emergency_country_code,
            share_location=share_location,
            share_medical_info=share_medical_info,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create/update profile: {str(e)}")


@router.get("/profile/{driver_id}", response_model=Emergency)
async def get_profile(driver_id: int, emergency_service: EmergencyService = Depends(get_emergency_service)):
    profile = await emergency_service.get_profile(driver_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
