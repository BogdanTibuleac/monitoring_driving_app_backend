
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.data.schemas.models import Vehicle


class VehicleService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_vehicles(self, limit: int = 100) -> List[Vehicle]:
        stmt = select(Vehicle).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        stmt = select(Vehicle).where(Vehicle.vehicle_id == vehicle_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_vehicle(self, make: str, model: str, year: int, type: Optional[str] = None) -> Vehicle:
        vehicle = Vehicle(make=make, model=model, year=year, type=type)
        self.session.add(vehicle)
        await self.session.commit()
        await self.session.refresh(vehicle)
        return vehicle

    async def update_vehicle(self, vehicle_id: int, updates: dict) -> Optional[Vehicle]:
        stmt = select(Vehicle).where(Vehicle.vehicle_id == vehicle_id)
        result = await self.session.execute(stmt)
        vehicle = result.scalar_one_or_none()
        if not vehicle:
            return None
        for k, v in updates.items():
            setattr(vehicle, k, v)
        self.session.add(vehicle)
        await self.session.commit()
        await self.session.refresh(vehicle)
        return vehicle

    async def delete_vehicle(self, vehicle_id: int) -> bool:
        stmt = select(Vehicle).where(Vehicle.vehicle_id == vehicle_id)
        result = await self.session.execute(stmt)
        vehicle = result.scalar_one_or_none()
        if not vehicle:
            return False
        await self.session.delete(vehicle)
        await self.session.commit()
        return True
