from functools import lru_cache
from app.core.database import get_db_provider
from app.data.repositories.template_repository import TemplateRepository
from app.services.cache_service import CacheService
from app.services.template_service import TemplateService
from app.services.driver_service import DriverService
from app.services.vehicle_service import VehicleService
from app.services.trip_service import TripService
from app.services.sos_service import SOSService
from app.services.gamification_service import GamificationService


# --------------------------------------------------------------------
# Cached / singleton-style dependencies
# --------------------------------------------------------------------

@lru_cache()
def get_database_provider():
    """Return the global DatabaseProvider singleton."""
    return get_db_provider()


@lru_cache()
def get_template_repository() -> TemplateRepository:
    """Template repository (singleton)."""
    db_provider = get_database_provider()
    return TemplateRepository(db_provider)


@lru_cache()
def get_cache_service() -> CacheService:
    """Cache service (singleton)."""
    return CacheService()


@lru_cache()
def get_template_service() -> TemplateService:
    """Template service (singleton)."""
    repository = get_template_repository()
    cache_service = get_cache_service()
    return TemplateService(repository, cache_service)


# --------------------------------------------------------------------
# Request-scoped, DB-session–bound services
# --------------------------------------------------------------------

async def get_driver_service():
    """
    Provide DriverService with a per-request DB session.
    The service is responsible for commits/rollbacks.
    """
    db_provider = get_database_provider()
    session_factory = db_provider.get_session_factory()
    async with session_factory() as session:
        yield DriverService(session)


async def get_vehicle_service():
    """
    Provide VehicleService with a per-request DB session.
    The service is responsible for commits/rollbacks.
    """
    db_provider = get_database_provider()
    session_factory = db_provider.get_session_factory()
    async with session_factory() as session:
        yield VehicleService(session)


async def get_trip_service():
    db_provider = get_db_provider()
    session_factory = db_provider.get_session_factory()
    async with session_factory() as session:
        yield TripService(session)


async def get_sos_service():
    db_provider = get_db_provider()
    session_factory = db_provider.get_session_factory()
    async with session_factory() as session:
        yield SOSService(session)


async def get_gamification_service():
    db_provider = get_db_provider()
    session_factory = db_provider.get_session_factory()
    async with session_factory() as session:
        yield GamificationService(session)
