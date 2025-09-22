# api package
from fastapi import APIRouter
from app.api.routers.driver_router import router as driver_router
from app.api.routers.vehicle_router import router as vehicle_router
# Add others as you build them:
from app.api.routers.trip_router import router as trip_router
from app.api.routers.sos_router import router as sos_router
from app.api.routers.gamification_router import router as gamification_router

api_router = APIRouter()
api_router.include_router(driver_router)
api_router.include_router(vehicle_router)
api_router.include_router(trip_router)
api_router.include_router(sos_router)
api_router.include_router(gamification_router)
