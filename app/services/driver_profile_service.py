from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.data.schemas.models import (
    Contact, Medical, Settings, Privacy, Notification
)


class DriverProfileService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # -------------------------
    # Contacts
    # -------------------------
    async def add_contact(self, contact: Contact) -> Contact:
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact

    async def get_contacts(self, driver_id: int) -> List[Contact]:
        stmt = select(Contact).where(Contact.driver_id == driver_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # -------------------------
    # Medical info
    # -------------------------
    async def upsert_medical(self, driver_id: int, data: dict) -> Medical:
        stmt = select(Medical).where(Medical.driver_id == driver_id)
        result = await self.session.execute(stmt)
        med = result.scalar_one_or_none()

        if not med:
            med = Medical(driver_id=driver_id, **data)
            self.session.add(med)
        else:
            for k, v in data.items():
                setattr(med, k, v)
            self.session.add(med)

        await self.session.commit()
        await self.session.refresh(med)
        return med

    async def get_medical(self, driver_id: int) -> Optional[Medical]:
        stmt = select(Medical).where(Medical.driver_id == driver_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # -------------------------
    # Settings
    # -------------------------
    async def upsert_settings(self, driver_id: int, data: dict) -> Settings:
        stmt = select(Settings).where(Settings.driver_id == driver_id)
        result = await self.session.execute(stmt)
        settings = result.scalar_one_or_none()

        if not settings:
            settings = Settings(driver_id=driver_id, **data)
            self.session.add(settings)
        else:
            for k, v in data.items():
                setattr(settings, k, v)
            self.session.add(settings)

        await self.session.commit()
        await self.session.refresh(settings)
        return settings

    async def get_settings(self, driver_id: int) -> Optional[Settings]:
        stmt = select(Settings).where(Settings.driver_id == driver_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # -------------------------
    # Privacy
    # -------------------------
    async def upsert_privacy(self, driver_id: int, data: dict) -> Privacy:
        stmt = select(Privacy).where(Privacy.driver_id == driver_id)
        result = await self.session.execute(stmt)
        privacy = result.scalar_one_or_none()

        if not privacy:
            privacy = Privacy(driver_id=driver_id, **data)
            self.session.add(privacy)
        else:
            for k, v in data.items():
                setattr(privacy, k, v)
            self.session.add(privacy)

        await self.session.commit()
        await self.session.refresh(privacy)
        return privacy

    async def get_privacy(self, driver_id: int) -> Optional[Privacy]:
        stmt = select(Privacy).where(Privacy.driver_id == driver_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # -------------------------
    # Notifications
    # -------------------------
    async def upsert_notification(self, driver_id: int, data: dict) -> Notification:
        stmt = select(Notification).where(Notification.driver_id == driver_id)
        result = await self.session.execute(stmt)
        notif = result.scalar_one_or_none()

        if not notif:
            notif = Notification(driver_id=driver_id, **data)
            self.session.add(notif)
        else:
            for k, v in data.items():
                setattr(notif, k, v)
            self.session.add(notif)

        await self.session.commit()
        await self.session.refresh(notif)
        return notif

    async def get_notification(self, driver_id: int) -> Optional[Notification]:
        stmt = select(Notification).where(Notification.driver_id == driver_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
