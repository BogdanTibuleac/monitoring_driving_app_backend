from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime
from app.data.schemas.models import FactSOS, Time, Location


class SOSService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_unresolved(self) -> List[FactSOS]:
        stmt = select(FactSOS).where(FactSOS.resolved == False)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, sos_id: int) -> Optional[FactSOS]:
        stmt = select(FactSOS).where(FactSOS.sos_id == sos_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_sos(
        self,
        driver_id: int,
        vehicle_id: int,
        latitude: float,
        longitude: float,
        severity: Optional[str] = None,
        anomaly_score: Optional[float] = None,
        signature_valid: Optional[bool] = None,
    ) -> FactSOS:
        ts = datetime.utcnow()

        # Ensure time entry
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

        # Create location entry
        loc = Location(latitude=latitude, longitude=longitude)
        self.session.add(loc)
        await self.session.commit()
        await self.session.refresh(loc)

        sos = FactSOS(
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            time_id=time_row.time_id,
            location_id=loc.location_id,
            severity=severity,
            signature_valid=signature_valid,
            anomaly_score=anomaly_score,
            resolved=False,
        )
        self.session.add(sos)
        await self.session.commit()
        await self.session.refresh(sos)
        return sos

    async def resolve_sos(self, sos_id: int) -> Optional[FactSOS]:
        stmt = select(FactSOS).where(FactSOS.sos_id == sos_id)
        result = await self.session.execute(stmt)
        sos = result.scalar_one_or_none()
        if not sos:
            return None
        sos.resolved = True
        self.session.add(sos)
        await self.session.commit()
        await self.session.refresh(sos)
        return sos
