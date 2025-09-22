from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func
from datetime import datetime, timedelta
from app.data.schemas.models import FactGamification, Badge, Driver, Time


class GamificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_badges(self, limit: int = 100) -> List[Badge]:
        stmt = select(Badge).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_event(
        self,
        driver_id: int,
        score_change: int,
        streak_days: Optional[int] = None,
        badge_id: Optional[int] = None,
        timestamp: Optional[datetime] = None,
    ) -> FactGamification:
        ts = timestamp or datetime.utcnow()

        # ensure time row exists
        stmt = select(Time).where(
            Time.date == ts.date(),
            Time.year == ts.year,
            Time.month == ts.month,
            Time.day == ts.day,
            Time.hour == ts.hour,
            Time.weekday == ts.weekday()
        )
        res = await self.session.execute(stmt)
        time_row = res.scalar_one_or_none()

        if not time_row:
            time_row = Time(
                date=ts.date(),
                year=ts.year,
                month=ts.month,
                day=ts.day,
                hour=ts.hour,
                weekday=ts.weekday()
            )
            self.session.add(time_row)
            await self.session.commit()
            await self.session.refresh(time_row)

        event = FactGamification(
            driver_id=driver_id,
            time_id=time_row.time_id,
            badge_id=badge_id,
            score_change=score_change,
            streak_days=streak_days,
        )
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_leaderboard(self, days: int = 7, limit: int = 10):
        cutoff = datetime.utcnow().date() - timedelta(days=days)

        sub_time_ids = select(Time.time_id).where(Time.date >= cutoff)

        stmt = (
            select(
                FactGamification.driver_id,
                func.sum(FactGamification.score_change).label("total_score")
            )
            .where(FactGamification.time_id.in_(sub_time_ids))
            .group_by(FactGamification.driver_id)
            .order_by(func.sum(FactGamification.score_change).desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        rows = result.all()

        leaderboard = []
        for driver_id, total_score in rows:
            d_stmt = select(Driver).where(Driver.driver_id == driver_id)
            d_res = await self.session.execute(d_stmt)
            driver = d_res.scalar_one_or_none()
            leaderboard.append({
                "driver_id": driver_id,
                "name": driver.name if driver else f"Driver {driver_id}",
                "total_score": int(total_score or 0)
            })
        return leaderboard
