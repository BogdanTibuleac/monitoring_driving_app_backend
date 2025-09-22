from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.services.sos_service import SOSService
from app.core.dependencies import get_sos_service
from app.data.schemas.models import FactSOS

router = APIRouter(prefix="/sos", tags=["sos"])


@router.get("/unresolved", response_model=List[FactSOS])
async def list_unresolved(sos_service: SOSService = Depends(get_sos_service)):
    return await sos_service.get_all_unresolved()


@router.get("/{sos_id}", response_model=FactSOS)
async def get_sos(sos_id: int, sos_service: SOSService = Depends(get_sos_service)):
    sos = await sos_service.get_by_id(sos_id)
    if not sos:
        raise HTTPException(status_code=404, detail="SOS not found")
    return sos


@router.post("/", response_model=FactSOS, status_code=201)
async def create_sos(
    driver_id: int,
    vehicle_id: int,
    latitude: float,
    longitude: float,
    severity: Optional[str] = None,
    anomaly_score: Optional[float] = None,
    signature_valid: Optional[bool] = None,
    sos_service: SOSService = Depends(get_sos_service),
):
    try:
        return await sos_service.create_sos(
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            latitude=latitude,
            longitude=longitude,
            severity=severity,
            anomaly_score=anomaly_score,
            signature_valid=signature_valid,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create SOS: {str(e)}")


@router.post("/{sos_id}/resolve", response_model=FactSOS)
async def resolve_sos(sos_id: int, sos_service: SOSService = Depends(get_sos_service)):
    sos = await sos_service.resolve_sos(sos_id)
    if not sos:
        raise HTTPException(status_code=404, detail="SOS not found")
    return sos
