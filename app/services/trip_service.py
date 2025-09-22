from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime
from app.data.schemas.models import FactTrip, Time


class TripService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_trips(self, limit: int = 100) -> List[FactTrip]:
        stmt = select(FactTrip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_trip_by_id(self, trip_id: int) -> Optional[FactTrip]:
        stmt = select(FactTrip).where(FactTrip.trip_id == trip_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_trip(
        self,
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
    ) -> FactTrip:
        """Insert trip and auto-manage time dimension entry."""
        ts = timestamp or datetime.utcnow()
        # Create or reuse time_id
        time_stmt = select(Time).where(
            Time.date == ts.date(),
            Time.year == ts.year,
            Time.month == ts.month,
            Time.day == ts.day,
            Time.hour == ts.hour,
            Time.weekday == ts.weekday()
        )
        time_result = await self.session.execute(time_stmt)
        time_row = time_result.scalar_one_or_none()

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

        trip = FactTrip(
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            time_id=time_row.time_id,
            distance_km=distance_km,
            avg_speed=avg_speed,
            harsh_events=harsh_events,
            eco_score=eco_score,
            safety_score=safety_score,
            trip_duration_sec=trip_duration_sec,
            max_speed=max_speed,
        )
        self.session.add(trip)
        await self.session.commit()
        await self.session.refresh(trip)
        return trip

    async def delete_trip(self, trip_id: int) -> bool:
        stmt = select(FactTrip).where(FactTrip.trip_id == trip_id)
        result = await self.session.execute(stmt)
        trip = result.scalar_one_or_none()
        if not trip:
            return False
        await self.session.delete(trip)
        await self.session.commit()
        return True
