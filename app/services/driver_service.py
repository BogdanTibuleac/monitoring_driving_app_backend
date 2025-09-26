from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.data.schemas.models import Driver
from datetime import date


class DriverService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_drivers(self, limit: int = 100) -> List[Driver]:
        stmt = select(Driver).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_driver_by_id(self, driver_id: int) -> Optional[Driver]:
        stmt = select(Driver).where(Driver.driver_id == driver_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_driver(
        self,
        name: str,
        license_type: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        date_of_birth: Optional[str] = None,  # can be str or date
    ) -> Driver:
        # convert to date if passed as string
        dob = None
        if date_of_birth:
            if isinstance(date_of_birth, str):
                dob = date.fromisoformat(date_of_birth)
            else:
                dob = date_of_birth

        driver = Driver(
            name=name,
            license_type=license_type,
            email=email,
            phone=phone,
            date_of_birth=dob,
        )
        self.session.add(driver)
        await self.session.commit()
        await self.session.refresh(driver)
        return driver

    async def update_driver(self, driver_id: int, updates: dict) -> Optional[Driver]:
        stmt = select(Driver).where(Driver.driver_id == driver_id)
        result = await self.session.execute(stmt)
        driver = result.scalar_one_or_none()
        if not driver:
            return None

        for k, v in updates.items():
            if hasattr(driver, k):
                # convert date_of_birth if it's a string
                if k == "date_of_birth" and isinstance(v, str):
                    try:
                        v = date.fromisoformat(v)
                    except ValueError:
                        continue  # skip invalid dates
                setattr(driver, k, v)

        self.session.add(driver)
        await self.session.commit()
        await self.session.refresh(driver)
        return driver

    async def delete_driver(self, driver_id: int) -> bool:
        stmt = select(Driver).where(Driver.driver_id == driver_id)
        result = await self.session.execute(stmt)
        driver = result.scalar_one_or_none()
        if not driver:
            return False
        await self.session.delete(driver)
        await self.session.commit()
        return True
