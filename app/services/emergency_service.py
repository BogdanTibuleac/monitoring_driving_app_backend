from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.data.schemas.models import EmergencyNumber, Emergency


class EmergencyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # -------------------------
    # Global emergency numbers
    # -------------------------
    async def get_all_numbers(self, limit: int = 100) -> List[EmergencyNumber]:
        stmt = select(EmergencyNumber).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_number_by_country(self, country_code: str) -> Optional[EmergencyNumber]:
        stmt = select(EmergencyNumber).where(EmergencyNumber.country_code == country_code)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # -------------------------
    # Driver emergency profile
    # -------------------------
    async def create_or_update_profile(
        self,
        driver_id: int,
        auto_contact_enabled: bool,
        emergency_country_code: Optional[str] = None,
        share_location: Optional[bool] = None,
        share_medical_info: Optional[bool] = None,
    ) -> Emergency:
        stmt = select(Emergency).where(Emergency.driver_id == driver_id)
        result = await self.session.execute(stmt)
        profile = result.scalar_one_or_none()

        if not profile:
            profile = Emergency(
                driver_id=driver_id,
                auto_contact_enabled=auto_contact_enabled,
                emergency_country_code=emergency_country_code,
                share_location=share_location,
                share_medical_info=share_medical_info,
            )
            self.session.add(profile)
        else:
            profile.auto_contact_enabled = auto_contact_enabled
            profile.emergency_country_code = emergency_country_code
            profile.share_location = share_location
            profile.share_medical_info = share_medical_info
            self.session.add(profile)

        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def get_profile(self, driver_id: int) -> Optional[Emergency]:
        stmt = select(Emergency).where(Emergency.driver_id == driver_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
