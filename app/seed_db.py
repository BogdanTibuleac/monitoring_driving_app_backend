import asyncio
from datetime import date, datetime
from sqlmodel import SQLModel
from app.core.database import get_db_provider
from app.data.schemas.models import (
    Driver, Vehicle, Location, Time, Badge,
    FactTrip, FactSOS, FactGamification, EmergencyNumber
)


async def seed():
    db_provider = get_db_provider()
    session_factory = db_provider.get_session_factory()

    async with session_factory() as session:
        # --- Drivers ---
        d1 = Driver(name="Alice Johnson", license_type="B", date_of_birth=date(1987, 4, 12))
        d2 = Driver(name="Michael Smith", license_type="C", date_of_birth=date(1979, 8, 23))
        d3 = Driver(name="Sofia Martinez", license_type="B", date_of_birth=date(1992, 1, 30))
        session.add_all([d1, d2, d3])
        await session.commit()
        await session.refresh(d1)
        await session.refresh(d2)
        await session.refresh(d3)

        # --- Vehicles ---
        v1 = Vehicle(make="Toyota", model="Corolla", year=2019, type="Sedan")
        v2 = Vehicle(make="Ford", model="Transit", year=2021, type="Van")
        v3 = Vehicle(make="Tesla", model="Model 3", year=2022, type="EV")
        session.add_all([v1, v2, v3])
        await session.commit()

        # --- Locations ---
        loc1 = Location(latitude=40.7128, longitude=-74.0060, city="New York", road_type="Highway")
        loc2 = Location(latitude=34.0522, longitude=-118.2437, city="Los Angeles", road_type="Urban")
        loc3 = Location(latitude=41.8781, longitude=-87.6298, city="Chicago", road_type="Suburban")
        session.add_all([loc1, loc2, loc3])
        await session.commit()

        # --- Time ---
        now = datetime.utcnow()
        t1 = Time(date=now.date(), year=now.year, month=now.month,
                  day=now.day, hour=now.hour, weekday=now.weekday())
        session.add(t1)
        await session.commit()

        # --- Badges ---
        b1 = Badge(badge_name="Eco Driver", description="Maintained >80 eco score", category="Eco")
        b2 = Badge(badge_name="Safe Driver", description="No incidents in 30 days", category="Safety")
        b3 = Badge(badge_name="Marathoner", description="Completed trip >500 km", category="Endurance")
        session.add_all([b1, b2, b3])
        await session.commit()

        # --- Trips ---
        trip1 = FactTrip(driver_id=d1.driver_id, vehicle_id=v1.vehicle_id, time_id=t1.time_id,
                         distance_km=120.5, avg_speed=75.3, harsh_events=1,
                         eco_score=82.0, safety_score=90.0, trip_duration_sec=5800, max_speed=110.0)
        trip2 = FactTrip(driver_id=d2.driver_id, vehicle_id=v2.vehicle_id, time_id=t1.time_id,
                         distance_km=450.2, avg_speed=68.0, harsh_events=4,
                         eco_score=70.0, safety_score=78.0, trip_duration_sec=20000, max_speed=125.0)
        session.add_all([trip1, trip2])
        await session.commit()

        # --- SOS event ---
        sos1 = FactSOS(driver_id=d3.driver_id, vehicle_id=v3.vehicle_id, time_id=t1.time_id,
                       location_id=loc2.location_id, severity="moderate",
                       signature_valid=True, anomaly_score=0.87, resolved=False)
        session.add(sos1)
        await session.commit()

        # --- Gamification ---
        g1 = FactGamification(driver_id=d1.driver_id, time_id=t1.time_id, badge_id=b1.badge_id,
                              score_change=20, streak_days=5)
        g2 = FactGamification(driver_id=d2.driver_id, time_id=t1.time_id, badge_id=b2.badge_id,
                              score_change=15, streak_days=3)
        g3 = FactGamification(driver_id=d3.driver_id, time_id=t1.time_id, badge_id=b3.badge_id,
                              score_change=30, streak_days=10)
        session.add_all([g1, g2, g3])
        await session.commit()

        # --- Emergency Numbers ---
        emergency_numbers = [
            ("AL", "Albania", "127"),
            ("AD", "Andorra", "112"),
            ("AT", "Austria", "144"),
            ("BY", "Belarus", "103"),
            ("BE", "Belgium", "100"),
            ("BA", "Bosnia and Herzegovina", "124"),
            ("BG", "Bulgaria", "112"),
            ("HR", "Croatia", "194"),
            ("CY", "Cyprus", "112"),
            ("CZ", "Czechia", "155"),
            ("DK", "Denmark", "112"),
            ("EE", "Estonia", "112"),
            ("FI", "Finland", "112"),
            ("FR", "France", "15"),
            ("DE", "Germany", "112"),
            ("GR", "Greece", "166"),
            ("HU", "Hungary", "104"),
            ("IS", "Iceland", "112"),
            ("IE", "Ireland", "112"),
            ("IT", "Italy", "118"),
            ("LV", "Latvia", "113"),
            ("LT", "Lithuania", "112"),
            ("LU", "Luxembourg", "112"),
            ("MT", "Malta", "112"),
            ("MD", "Moldova", "112"),
            ("MC", "Monaco", "15"),
            ("ME", "Montenegro", "124"),
            ("NL", "Netherlands", "112"),
            ("NO", "Norway", "113"),
            ("PL", "Poland", "999"),
            ("PT", "Portugal", "112"),
            ("RO", "Romania", "112"),
            ("RU", "Russia", "103"),
            ("RS", "Serbia", "194"),
            ("SK", "Slovakia", "155"),
            ("SI", "Slovenia", "112"),
            ("ES", "Spain", "061"),
            ("SE", "Sweden", "112"),
            ("CH", "Switzerland", "144"),
            ("TR", "Turkey", "112"),
            ("UA", "Ukraine", "103"),
            ("GB", "United Kingdom", "999"),
            ("US", "United States", "911"),
            ("CA", "Canada", "911"),
            ("MX", "Mexico", "911"),
            ("BR", "Brazil", "192"),
            ("AR", "Argentina", "107"),
            ("AU", "Australia", "000"),
            ("NZ", "New Zealand", "111"),
            ("JP", "Japan", "119"),
            ("CN", "China", "120"),
            ("IN", "India", "102"),
            ("ZA", "South Africa", "10177"),
            ("SA", "Saudi Arabia", "997"),
            ("AE", "United Arab Emirates", "998"),
            ("KR", "South Korea", "119"),
            ("SG", "Singapore", "995"),
            ("MY", "Malaysia", "999"),
            ("TH", "Thailand", "1669"),
            ("PH", "Philippines", "911"),
            ("VN", "Vietnam", "115"),
            ("IL", "Israel", "101"),
            ("HK", "Hong Kong", "999"),
            ("TW", "Taiwan", "119"),
        ]

        for code, name, num in emergency_numbers:
            session.add(EmergencyNumber(country_code=code, country_name=name, ambulance_number=num))

        await session.commit()

    print("✅ Seed data inserted successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
