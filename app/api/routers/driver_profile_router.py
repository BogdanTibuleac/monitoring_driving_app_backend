from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.services.driver_profile_service import DriverProfileService
from app.core.dependencies import get_driver_profile_service
from app.data.schemas.models import Contact, Medical, Settings, Privacy, Notification

router = APIRouter(prefix="/drivers/{driver_id}/profile", tags=["driver_profile"])


# -------------------------
# Contacts
# -------------------------
@router.get("/contacts", response_model=List[Contact])
async def list_contacts(driver_id: int, service: DriverProfileService = Depends(get_driver_profile_service)):
    return await service.get_contacts(driver_id)


@router.post("/contacts", response_model=Contact, status_code=201)
async def add_contact(driver_id: int, contact: Contact, service: DriverProfileService = Depends(get_driver_profile_service)):
    contact.driver_id = driver_id
    return await service.add_contact(contact)


# -------------------------
# Medical
# -------------------------
@router.get("/medical", response_model=Medical)
async def get_medical(driver_id: int, service: DriverProfileService = Depends(get_driver_profile_service)):
    med = await service.get_medical(driver_id)
    if not med:
        raise HTTPException(status_code=404, detail="No medical record")
    return med


@router.patch("/medical", response_model=Medical, status_code=201)
async def upsert_medical(driver_id: int, data: dict, service: DriverProfileService = Depends(get_driver_profile_service)):
    return await service.upsert_medical(driver_id, data)


# -------------------------
# Settings
# -------------------------
@router.get("/settings", response_model=Settings)
async def get_settings(driver_id: int, service: DriverProfileService = Depends(get_driver_profile_service)):
    s = await service.get_settings(driver_id)
    if not s:
        raise HTTPException(status_code=404, detail="No settings record")
    return s


@router.post("/settings", response_model=Settings, status_code=201)
async def upsert_settings(driver_id: int, data: dict, service: DriverProfileService = Depends(get_driver_profile_service)):
    return await service.upsert_settings(driver_id, data)


# -------------------------
# Privacy
# -------------------------
@router.get("/privacy", response_model=Privacy)
async def get_privacy(driver_id: int, service: DriverProfileService = Depends(get_driver_profile_service)):
    p = await service.get_privacy(driver_id)
    if not p:
        raise HTTPException(status_code=404, detail="No privacy record")
    return p


@router.post("/privacy", response_model=Privacy, status_code=201)
async def upsert_privacy(driver_id: int, data: dict, service: DriverProfileService = Depends(get_driver_profile_service)):
    return await service.upsert_privacy(driver_id, data)


# -------------------------
# Notifications
# -------------------------
@router.get("/notifications", response_model=Notification)
async def get_notification(driver_id: int, service: DriverProfileService = Depends(get_driver_profile_service)):
    n = await service.get_notification(driver_id)
    if not n:
        raise HTTPException(status_code=404, detail="No notification record")
    return n


@router.post("/notifications", response_model=Notification, status_code=201)
async def upsert_notification(driver_id: int, data: dict, service: DriverProfileService = Depends(get_driver_profile_service)):
    return await service.upsert_notification(driver_id, data)
