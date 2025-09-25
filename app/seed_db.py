import asyncio
from datetime import date, datetime, timedelta
from sqlmodel import select
from app.core.database import get_db_provider
from app.data.schemas.models import (
    Driver, Vehicle, Location, Time, Badge,
    FactTrip, FactSOS, FactGamification, FactSecurity,
    EmergencyNumber, Emergency,
    Contact, Medical, Settings, Privacy, Notification
)


async def seed():
    db_provider = get_db_provider()
    session_factory = db_provider.get_session_factory()

    async with session_factory() as session:
        # -------------------------
        # Drivers
        # -------------------------
        drivers = [
            Driver(name="Alice Johnson", license_type="B", date_of_birth=date(1987, 4, 12)),
            Driver(name="Michael Smith", license_type="C", date_of_birth=date(1979, 8, 23)),
            Driver(name="Sofia Martinez", license_type="B", date_of_birth=date(1992, 1, 30)),
        ]
        session.add_all(drivers)
        await session.commit()
        for d in drivers:
            await session.refresh(d)

        # -------------------------
        # Contacts, Medical, Settings, Privacy, Notifications
        # -------------------------
        contacts = [
            Contact(driver_id=drivers[0].driver_id, name="Jane Johnson", relationship="Spouse",
                    phone="+1-555-1234", email="jane.johnson@example.com", is_primary=True),
            Contact(driver_id=drivers[1].driver_id, name="Robert Smith", relationship="Brother",
                    phone="+1-555-5678", email="robert.smith@example.com", is_primary=False),
            Contact(driver_id=drivers[2].driver_id, name="Maria Martinez", relationship="Mother",
                    phone="+34-600-123-456", email="maria.martinez@example.com", is_primary=True),
        ]
        session.add_all(contacts)

        medicals = [
            Medical(driver_id=drivers[0].driver_id, blood_type="O+", insurance="BlueCross",
                    allergies="Peanuts", medications="Ibuprofen", conditions="Asthma",
                    instructions="Carry inhaler"),
            Medical(driver_id=drivers[1].driver_id, blood_type="A-", insurance="United Health",
                    allergies=None, medications="Atorvastatin", conditions="High cholesterol",
                    instructions=None),
            Medical(driver_id=drivers[2].driver_id, blood_type="B+", insurance="AXA",
                    allergies="Penicillin", medications=None, conditions=None,
                    instructions="Alert doctor for antibiotic use"),
        ]
        session.add_all(medicals)

        settings = [
            Settings(driver_id=drivers[0].driver_id, detection_sensitivity=5, auto_sos_delay=10,
                     accelerometer_enabled=True, gyroscope_enabled=True, gps_enabled=True, microphone_enabled=False),
            Settings(driver_id=drivers[1].driver_id, detection_sensitivity=7, auto_sos_delay=5,
                     accelerometer_enabled=True, gyroscope_enabled=True, gps_enabled=True, microphone_enabled=True),
            Settings(driver_id=drivers[2].driver_id, detection_sensitivity=4, auto_sos_delay=15,
                     accelerometer_enabled=False, gyroscope_enabled=True, gps_enabled=True, microphone_enabled=True),
        ]
        session.add_all(settings)

        privacies = [
            Privacy(driver_id=drivers[0].driver_id, data_sharing_mode="opt-in", location_accuracy="high", local_caching=True),
            Privacy(driver_id=drivers[1].driver_id, data_sharing_mode="opt-out", location_accuracy="medium", local_caching=False),
            Privacy(driver_id=drivers[2].driver_id, data_sharing_mode="opt-in", location_accuracy="low", local_caching=True),
        ]
        session.add_all(privacies)

        notifications = [
            Notification(driver_id=drivers[0].driver_id, push_enabled=True, sound_enabled=True, vibration_enabled=True, volume=80),
            Notification(driver_id=drivers[1].driver_id, push_enabled=False, sound_enabled=True, vibration_enabled=False, volume=60),
            Notification(driver_id=drivers[2].driver_id, push_enabled=True, sound_enabled=False, vibration_enabled=True, volume=90),
        ]
        session.add_all(notifications)

        await session.commit()

        # -------------------------
        # Vehicles
        # -------------------------
        vehicles = [
            Vehicle(make="Toyota", model="Corolla", year=2019, type="Sedan"),
            Vehicle(make="Ford", model="Transit", year=2021, type="Van"),
            Vehicle(make="Tesla", model="Model 3", year=2022, type="EV"),
        ]
        session.add_all(vehicles)
        await session.commit()
        for v in vehicles:
            await session.refresh(v)

        # -------------------------
        # Locations
        # -------------------------
        locations = [
            Location(latitude=40.7128, longitude=-74.0060, city="New York", road_type="Highway"),
            Location(latitude=34.0522, longitude=-118.2437, city="Los Angeles", road_type="Urban"),
            Location(latitude=41.8781, longitude=-87.6298, city="Chicago", road_type="Suburban"),
        ]
        session.add_all(locations)
        await session.commit()
        for loc in locations:
            await session.refresh(loc)

        # -------------------------
        # Time entries
        # -------------------------
        now = datetime.utcnow()
        times = [
            Time(date_value=now.date(), year=now.year, month=now.month, day=now.day,
                 hour=now.hour, weekday=now.weekday()),
            Time(date_value=(now - timedelta(days=1)).date(), year=(now - timedelta(days=1)).year,
                 month=(now - timedelta(days=1)).month, day=(now - timedelta(days=1)).day,
                 hour=(now - timedelta(days=1)).hour, weekday=(now - timedelta(days=1)).weekday())
        ]
        session.add_all(times)
        await session.commit()
        for t in times:
            await session.refresh(t)

        # -------------------------
        # Badges
        # -------------------------
        badges = [
            Badge(badge_name="Eco Driver", description="Maintained >80 eco score", category="Eco"),
            Badge(badge_name="Safe Driver", description="No incidents in 30 days", category="Safety"),
            Badge(badge_name="Marathoner", description="Completed trip >500 km", category="Endurance"),
        ]
        session.add_all(badges)
        await session.commit()
        for b in badges:
            await session.refresh(b)

        # -------------------------
        # Emergency numbers
        # -------------------------
        emergency_numbers = [
            ("US", "United States", "911"),
            ("DE", "Germany", "112"),
            ("FR", "France", "15"),
            ("IN", "India", "102"),
        ]
        for code, name, num in emergency_numbers:
            exists = await session.execute(
                select(EmergencyNumber).where(EmergencyNumber.country_code == code)
            )
            if not exists.scalar_one_or_none():
                session.add(EmergencyNumber(country_code=code, country_name=name, ambulance_number=num))
        await session.commit()

        # -------------------------
        # Emergency profiles
        # -------------------------
        emergencies = [
            Emergency(driver_id=drivers[0].driver_id, auto_contact_enabled=True,
                      emergency_country_code="US", share_location=True, share_medical_info=True),
            Emergency(driver_id=drivers[1].driver_id, auto_contact_enabled=False,
                      emergency_country_code="DE", share_location=False, share_medical_info=True),
            Emergency(driver_id=drivers[2].driver_id, auto_contact_enabled=True,
                      emergency_country_code="FR", share_location=True, share_medical_info=False),
        ]
        session.add_all(emergencies)
        await session.commit()

        # -------------------------
        # Trips
        # -------------------------
        trip1 = FactTrip(driver_id=drivers[0].driver_id, vehicle_id=vehicles[0].vehicle_id,
                         time_id=times[0].time_id, distance_km=120.5, avg_speed=75.3,
                         harsh_events=1, eco_score=82.0, safety_score=90.0,
                         trip_duration_sec=5800, max_speed=110.0)
        trip2 = FactTrip(driver_id=drivers[1].driver_id, vehicle_id=vehicles[1].vehicle_id,
                         time_id=times[1].time_id, distance_km=450.2, avg_speed=68.0,
                         harsh_events=4, eco_score=70.0, safety_score=78.0,
                         trip_duration_sec=20000, max_speed=125.0)
        session.add_all([trip1, trip2])
        await session.commit()
        await session.refresh(trip1)
        await session.refresh(trip2)

        # -------------------------
        # SOS events
        # -------------------------
        sos1 = FactSOS(driver_id=drivers[2].driver_id, vehicle_id=vehicles[2].vehicle_id,
                       time_id=times[0].time_id, location_id=locations[1].location_id,
                       severity="moderate", signature_valid=True, anomaly_score=0.87, resolved=False)
        session.add(sos1)
        await session.commit()
        await session.refresh(sos1)

        # -------------------------
        # Gamification
        # -------------------------
        g1 = FactGamification(driver_id=drivers[0].driver_id, time_id=times[0].time_id,
                              badge_id=badges[0].badge_id, score_change=20, streak_days=5)
        g2 = FactGamification(driver_id=drivers[1].driver_id, time_id=times[1].time_id,
                              badge_id=badges[1].badge_id, score_change=15, streak_days=3)
        g3 = FactGamification(driver_id=drivers[2].driver_id, time_id=times[0].time_id,
                              badge_id=badges[2].badge_id, score_change=30, streak_days=10)
        session.add_all([g1, g2, g3])
        await session.commit()

        # -------------------------
        # Security log
        # -------------------------
        s1 = FactSecurity(time_id=times[0].time_id, event_type="Trip", ref_id=trip1.trip_id,
                          signature_status=True, hash_value="abc123hash")
        s2 = FactSecurity(time_id=times[1].time_id, event_type="Trip", ref_id=trip2.trip_id,
                          signature_status=True, hash_value="def456hash")
        s3 = FactSecurity(time_id=times[0].time_id, event_type="SOS", ref_id=sos1.sos_id,
                          signature_status=False, hash_value="ghi789hash")
        session.add_all([s1, s2, s3])
        await session.commit()

    print("✅ Seed data inserted successfully for all tables!")


if __name__ == "__main__":
    asyncio.run(seed())
