#models.py
from __future__ import annotations
from typing import Optional
from datetime import date, datetime, timezone
from sqlmodel import SQLModel, Field
from datetime import date as dt_date, datetime


# Helpers
def utcnow() -> datetime:
    return datetime.now(timezone.utc)


##########################################################
# Dimension Tables
##########################################################

class Driver(SQLModel, table=True):
    __tablename__ = "dim_driver"
    driver_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    license_type: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=20)
    phone: Optional[str] = Field(default=None, max_length=20)

    date_of_birth: Optional[date] = None


class Contact(SQLModel, table=True):
    __tablename__ = "dim_contact"
    contact_id: Optional[int] = Field(default=None, primary_key=True)
    driver_id: int = Field(foreign_key="dim_driver.driver_id", nullable=False)
    name: str = Field(max_length=100, nullable=False)
    relationship: Optional[str] = Field(default=None, max_length=50)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)
    is_primary: Optional[bool] = Field(default=False)


class Medical(SQLModel, table=True):
    __tablename__ = "dim_medical"
    medical_id: Optional[int] = Field(default=None, primary_key=True)
    driver_id: int = Field(foreign_key="dim_driver.driver_id", nullable=False)
    blood_type: Optional[str] = Field(default=None, max_length=5)
    insurance: Optional[str] = Field(default=None, max_length=100)
    allergies: Optional[str] = None
    medications: Optional[str] = None
    conditions: Optional[str] = None
    instructions: Optional[str] = None


class Vehicle(SQLModel, table=True):
    __tablename__ = "dim_vehicle"
    vehicle_id: Optional[int] = Field(default=None, primary_key=True)
    make: str = Field(max_length=50, nullable=False)
    model: str = Field(max_length=50, nullable=False)
    year: int
    type: Optional[str] = Field(default=None, max_length=20)


class Time(SQLModel, table=True):
    __tablename__ = "dim_time"
    time_id: Optional[int] = Field(default=None, primary_key=True)
    date_value: dt_date = Field(default_factory=lambda: datetime.now().date())
    year: int
    month: int
    day: int
    hour: int
    weekday: int

class Location(SQLModel, table=True):
    __tablename__ = "dim_location"
    location_id: Optional[int] = Field(default=None, primary_key=True)
    latitude: float
    longitude: float
    city: Optional[str] = Field(default=None, max_length=50)
    road_type: Optional[str] = Field(default=None, max_length=30)


class Badge(SQLModel, table=True):
    __tablename__ = "dim_badge"
    badge_id: Optional[int] = Field(default=None, primary_key=True)
    badge_name: str = Field(max_length=50, nullable=False)
    description: Optional[str] = None
    category: Optional[str] = Field(default=None, max_length=20)


class Settings(SQLModel, table=True):
    __tablename__ = "dim_settings"
    settings_id: Optional[int] = Field(default=None, primary_key=True)
    driver_id: int = Field(foreign_key="dim_driver.driver_id", nullable=False)
    detection_sensitivity: Optional[int] = None
    auto_sos_delay: Optional[int] = None
    accelerometer_enabled: Optional[bool] = None
    gyroscope_enabled: Optional[bool] = None
    gps_enabled: Optional[bool] = None
    microphone_enabled: Optional[bool] = None


class Notification(SQLModel, table=True):
    __tablename__ = "dim_notification"
    notification_id: Optional[int] = Field(default=None, primary_key=True)
    driver_id: int = Field(foreign_key="dim_driver.driver_id", nullable=False)
    push_enabled: Optional[bool] = None
    sound_enabled: Optional[bool] = None
    vibration_enabled: Optional[bool] = None
    volume: Optional[int] = None


class Privacy(SQLModel, table=True):
    __tablename__ = "dim_privacy"
    privacy_id: Optional[int] = Field(default=None, primary_key=True)
    driver_id: int = Field(foreign_key="dim_driver.driver_id", nullable=False)
    data_sharing_mode: Optional[str] = Field(default=None, max_length=50)
    location_accuracy: Optional[str] = Field(default=None, max_length=50)
    local_caching: Optional[bool] = None


class EmergencyNumber(SQLModel, table=True):
    """
    Global ambulance numbers by country/region
    """
    __tablename__ = "dim_emergency_number"
    country_code: str = Field(primary_key=True, max_length=5)  # e.g. "US", "DE"
    country_name: str = Field(max_length=100, nullable=False)
    ambulance_number: str = Field(max_length=10, nullable=False)
    notes: Optional[str] = None


class Emergency(SQLModel, table=True):
    __tablename__ = "dim_emergency"
    emergency_id: Optional[int] = Field(default=None, primary_key=True)
    driver_id: int = Field(foreign_key="dim_driver.driver_id", nullable=False)
    auto_contact_enabled: Optional[bool] = None
    emergency_country_code: Optional[str] = Field(
        default=None, foreign_key="dim_emergency_number.country_code"
    )
    share_location: Optional[bool] = None
    share_medical_info: Optional[bool] = None


##########################################################
# Fact Tables
##########################################################

class FactSOS(SQLModel, table=True):
    __tablename__ = "fact_sos"
    sos_id: Optional[int] = Field(default=None, primary_key=True)
    driver_id: int = Field(foreign_key="dim_driver.driver_id", nullable=False)
    vehicle_id: int = Field(foreign_key="dim_vehicle.vehicle_id", nullable=False)
    time_id: int = Field(foreign_key="dim_time.time_id", nullable=False)
    location_id: int = Field(foreign_key="dim_location.location_id", nullable=False)

    severity: Optional[str] = Field(default=None, max_length=10)
    signature_valid: Optional[bool] = None
    anomaly_score: Optional[float] = None
    resolved: Optional[bool] = None


class FactTrip(SQLModel, table=True):
    __tablename__ = "fact_trip"
    trip_id: Optional[int] = Field(default=None, primary_key=True)
    driver_id: int = Field(foreign_key="dim_driver.driver_id", nullable=False)
    vehicle_id: int = Field(foreign_key="dim_vehicle.vehicle_id", nullable=False)
    time_id: int = Field(foreign_key="dim_time.time_id", nullable=False)

    distance_km: Optional[float] = None
    avg_speed: Optional[float] = None
    harsh_events: Optional[int] = None
    eco_score: Optional[float] = None
    safety_score: Optional[float] = None
    trip_duration_sec: Optional[int] = None
    max_speed: Optional[float] = None


class FactGamification(SQLModel, table=True):
    __tablename__ = "fact_gamification"
    gamelog_id: Optional[int] = Field(default=None, primary_key=True)
    driver_id: int = Field(foreign_key="dim_driver.driver_id", nullable=False)
    time_id: int = Field(foreign_key="dim_time.time_id", nullable=False)
    badge_id: Optional[int] = Field(default=None, foreign_key="dim_badge.badge_id")

    score_change: Optional[int] = None
    streak_days: Optional[int] = None


class FactSecurity(SQLModel, table=True):
    __tablename__ = "fact_security"
    sec_id: Optional[int] = Field(default=None, primary_key=True)
    time_id: int = Field(foreign_key="dim_time.time_id", nullable=False)

    event_type: str = Field(max_length=50, nullable=False)  # "SOS", "Trip", "Gamification"
    ref_id: int = Field(nullable=False)                     # references fact IDs
    signature_status: Optional[bool] = None
    hash_value: Optional[str] = None
