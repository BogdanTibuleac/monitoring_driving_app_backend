from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.analytics_service import AnalyticsService
from app.core.dependencies import get_analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/trips")
async def trips_summary(service: AnalyticsService = Depends(get_analytics_service)):
    try:
        return await service.trips_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch trips analytics: {str(e)}")


@router.get("/sos")
async def sos_summary(service: AnalyticsService = Depends(get_analytics_service)):
    try:
        return await service.sos_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch SOS analytics: {str(e)}")


@router.get("/leaderboard")
async def leaderboard(limit: int = Query(5, ge=1, le=50),
                      service: AnalyticsService = Depends(get_analytics_service)):
    try:
        return await service.gamification_leaderboard(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch leaderboard: {str(e)}")
