from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.services.gamification_service import GamificationService
from app.core.dependencies import get_gamification_service
from app.data.schemas.models import Badge, FactGamification

router = APIRouter(prefix="/gamification", tags=["gamification"])


@router.get("/badges", response_model=List[Badge])
async def list_badges(gamification_service: GamificationService = Depends(get_gamification_service)):
    return await gamification_service.get_badges()


@router.post("/events", response_model=FactGamification, status_code=201)
async def add_event(
    driver_id: int,
    score_change: int,
    streak_days: Optional[int] = None,
    badge_id: Optional[int] = None,
    timestamp: Optional[datetime] = None,
    gamification_service: GamificationService = Depends(get_gamification_service),
):
    try:
        return await gamification_service.add_event(
            driver_id=driver_id,
            score_change=score_change,
            streak_days=streak_days,
            badge_id=badge_id,
            timestamp=timestamp,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log gamification event: {str(e)}")


@router.get("/leaderboard")
async def leaderboard(
    days: int = Query(7, ge=1, le=90),
    limit: int = Query(10, ge=1, le=100),
    gamification_service: GamificationService = Depends(get_gamification_service),
):
    try:
        return await gamification_service.get_leaderboard(days=days, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch leaderboard: {str(e)}")
