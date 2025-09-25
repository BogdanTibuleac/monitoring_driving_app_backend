from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func
from typing import List, Dict
from app.data.schemas.models import FactTrip, FactSOS, FactGamification, Driver


class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # -------------------------
    # Trips analytics
    # -------------------------
    async def trips_summary(self) -> Dict:
        stmt = select(
            func.count(FactTrip.trip_id),
            func.avg(FactTrip.distance_km),
            func.avg(FactTrip.avg_speed),
            func.avg(FactTrip.eco_score),
            func.avg(FactTrip.safety_score),
        )
        result = await self.session.execute(stmt)
        total_trips, avg_distance, avg_speed, avg_eco, avg_safety = result.one()
        return {
            "total_trips": total_trips or 0,
            "avg_distance_km": float(avg_distance or 0),
            "avg_speed": float(avg_speed or 0),
            "avg_eco_score": float(avg_eco or 0),
            "avg_safety_score": float(avg_safety or 0),
        }

    # -------------------------
    # SOS analytics
    # -------------------------
    async def sos_summary(self) -> Dict:
        stmt = select(
            func.count(FactSOS.sos_id),
            func.count().filter(FactSOS.resolved == True),
            func.count().filter(FactSOS.resolved == False),
        )
        result = await self.session.execute(stmt)
        total, resolved, unresolved = result.one()
        return {
            "total_sos": total or 0,
            "resolved": resolved or 0,
            "unresolved": unresolved or 0,
        }

    # -------------------------
    # Gamification leaderboard
    # -------------------------
    async def gamification_leaderboard(self, limit: int = 5) -> List[Dict]:
        stmt = (
            select(
                FactGamification.driver_id,
                func.sum(FactGamification.score_change).label("score")
            )
            .group_by(FactGamification.driver_id)
            .order_by(func.sum(FactGamification.score_change).desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        leaderboard = []
        for driver_id, score in result.all():
            d_stmt = select(Driver).where(Driver.driver_id == driver_id)
            d_res = await self.session.execute(d_stmt)
            driver = d_res.scalar_one_or_none()
            leaderboard.append({
                "driver_id": driver_id,
                "name": driver.name if driver else f"Driver {driver_id}",
                "score": int(score or 0)
            })
        return leaderboard
