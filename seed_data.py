import datetime
import json
import secrets
from app.database import SessionLocal, Base, engine
from app.models import (
    User, Household, HouseholdMember, Bill, Appliance, Budget, TariffConfig,
    UsageReading, Device, Recommendation, Notification
)
from app.auth import get_password_hash
from app.services.tariff_service import DEFAULT_DEMO_TARIFFS
from app.services.recommendations_service import RecommendationsService
from app.services.device_simulator import DeviceSimulator

def seed_database():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Clean existing demo data if any
        existing_owner = db.query(User).filter(User.email == "demo@bijlisave.in").first()
        if existing_owner:
            print("Existing demo user found. Cleaning up prior demo records...")
            # Delete households owned by demo
            hhs = db.query(Household).filter(Household.owner_user_id == existing_owner.id).all()
            for h in hhs:
                db.delete(h)
            db.delete(existing_owner)
            
            existing_member = db.query(User).filter(User.email == "family@bijlisave.in").first()
            if existing_member:
                db.delete(existing_member)
            db.commit()

        print("Creating demo users...")
        owner = User(
            name="Anand Sundaram",
            email="demo@bijlisave.in",
            password_hash=get_password_hash("Bijli@2026"),
            preferred_language="ta"  # Default Tamil for bilingual showcase
        )
        family_member = User(
            name="Kavitha Anand",
            email="family@bijlisave.in",
            password_hash=get_password_hash("Bijli@2026"),
            preferred_language="en"
        )
        db.add_all([owner, family_member])
        db.commit()
        db.refresh(owner)
        db.refresh(family_member)

        print("Creating demo household...")
        invite_code = "BIJLI888"
        household = Household(
            owner_user_id=owner.id,
            name="Sundaram Residence (Chennai)",
            state="Tamil Nadu",
            provider="TNEB / TANGEDCO",
            consumer_category="Domestic",
            invite_code=invite_code
        )
        db.add(household)
        db.commit()
        db.refresh(household)

        # Memberships
        m1 = HouseholdMember(household_id=household.id, user_id=owner.id, role="owner", status="active")
        m2 = HouseholdMember(household_id=household.id, user_id=family_member.id, role="member", status="active")
        db.add_all([m1, m2])
        db.commit()

        print("Inserting historical electricity bills (6 months)...")
        # Fictional seasonal bills (May - Oct 2026)
        sample_bills = [
            {
                "start": datetime.date(2026, 5, 1),
                "end": datetime.date(2026, 5, 31),
                "bill_date": datetime.date(2026, 6, 2),
                "due_date": datetime.date(2026, 6, 17),
                "units": 470.0,
                "amount": 2640.0,
                "source": "manual",
                "notes": "Peak summer AC consumption during high Chennai temperatures."
            },
            {
                "start": datetime.date(2026, 6, 1),
                "end": datetime.date(2026, 6, 30),
                "bill_date": datetime.date(2026, 7, 2),
                "due_date": datetime.date(2026, 7, 17),
                "units": 430.0,
                "amount": 2320.0,
                "source": "ocr-confirmed",
                "notes": "Summer bill verified from paper bill scan."
            },
            {
                "start": datetime.date(2026, 7, 1),
                "end": datetime.date(2026, 7, 31),
                "bill_date": datetime.date(2026, 8, 2),
                "due_date": datetime.date(2026, 8, 17),
                "units": 360.0,
                "amount": 1790.0,
                "source": "manual",
                "notes": "Monsoon onset; reduced afternoon AC usage."
            },
            {
                "start": datetime.date(2026, 8, 1),
                "end": datetime.date(2026, 8, 31),
                "bill_date": datetime.date(2026, 9, 2),
                "due_date": datetime.date(2026, 9, 17),
                "units": 320.0,
                "amount": 1490.0,
                "source": "manual",
                "notes": "Pleasant weather; fans used more than air conditioner."
            },
            {
                "start": datetime.date(2026, 9, 1),
                "end": datetime.date(2026, 9, 30),
                "bill_date": datetime.date(2026, 10, 2),
                "due_date": datetime.date(2026, 10, 17),
                "units": 295.0,
                "amount": 1300.0,
                "source": "manual",
                "notes": "Normal billing cycle."
            },
            {
                "start": datetime.date(2026, 10, 1),
                "end": datetime.date(2026, 10, 26),
                "bill_date": datetime.date(2026, 10, 27),
                "due_date": datetime.date(2026, 11, 10),
                "units": 275.0,
                "amount": 1150.0,
                "source": "manual",
                "notes": "Current billing cycle record."
            }
        ]

        for b in sample_bills:
            bill_obj = Bill(
                household_id=household.id,
                period_start=b["start"],
                period_end=b["end"],
                bill_date=b["bill_date"],
                due_date=b["due_date"],
                units_kwh=b["units"],
                amount_actual=b["amount"],
                fixed_charges=25.0,
                energy_charges=b["amount"] - 25.0,
                source=b["source"],
                notes=b["notes"]
            )
            db.add(bill_obj)
        db.commit()

        print("Adding sample household appliances...")
        appliances_data = [
            {"name": "Master Bed Split AC (1.5T Inverter)", "type": "ac", "watts": 1400.0, "qty": 1, "hrs": 6.0, "days": 30.0, "source": "sample estimate"},
            {"name": "Double Door Refrigerator (260L)", "type": "refrigerator", "watts": 180.0, "qty": 1, "hrs": 24.0, "days": 30.0, "source": "sample estimate"},
            {"name": "BLDC Ceiling Fans", "type": "fan", "watts": 35.0, "qty": 3, "hrs": 12.0, "days": 30.0, "source": "user entered"},
            {"name": "Living Room LED Tubelights", "type": "lighting", "watts": 20.0, "qty": 4, "hrs": 6.0, "days": 30.0, "source": "sample estimate"},
            {"name": "Smart LED TV (50 inch)", "type": "tv", "watts": 95.0, "qty": 1, "hrs": 4.0, "days": 30.0, "source": "user entered"},
            {"name": "Storage Geyser (15L)", "type": "geyser", "watts": 2000.0, "qty": 1, "hrs": 0.75, "days": 30.0, "source": "sample estimate"},
            {"name": "Front Load Washing Machine", "type": "washing_machine", "watts": 500.0, "qty": 1, "hrs": 1.0, "days": 20.0, "source": "sample estimate"}
        ]

        app_objects = []
        for app in appliances_data:
            a = Appliance(
                household_id=household.id,
                name=app["name"],
                appliance_type=app["type"],
                power_watts=app["watts"],
                quantity=app["qty"],
                hours_per_day=app["hrs"],
                days_per_month=app["days"],
                power_source=app["source"]
            )
            db.add(a)
            app_objects.append(a)
        db.commit()

        print("Setting up monthly budget & notifications...")
        budget = Budget(
            household_id=household.id,
            month="2026-10",
            amount=2000.0,
            thresholds_json="[75, 90, 100]"
        )
        db.add(budget)

        # Sample alert
        alert = Notification(
            household_id=household.id,
            user_id=owner.id,
            alert_key=f"budget_{household.id}_2026-10_demo",
            title="Welcome to BijliSave!",
            message="Your household has been setup with 6 months of demo bills, appliances, and simulated smart meter readings.",
            threshold=None,
            is_read=False
        )
        db.add(alert)
        db.commit()

        print("Seeding demo tariff configurations...")
        for state, config in DEFAULT_DEMO_TARIFFS.items():
            existing_t = db.query(TariffConfig).filter(TariffConfig.state == state).first()
            if not existing_t:
                tc = TariffConfig(
                    state=state,
                    provider=config["provider"],
                    consumer_category=config["consumer_category"],
                    effective_from=datetime.date(2026, 1, 1),
                    config_json=json.dumps(config["slabs"]),
                    source_label=config["source_label"],
                    is_demo=True
                )
                db.add(tc)
        db.commit()

        print("Generating savings recommendations...")
        bill_records = db.query(Bill).filter(Bill.household_id == household.id).all()
        RecommendationsService.generate_and_sync_recommendations(household, app_objects, bill_records, db)

        print("Seeding smart meter device and 24 hours of simulated hourly readings...")
        DeviceSimulator.seed_recent_simulated_readings(household.id, db, hours=24)

        print("\n=======================================================")
        print("SEEDING COMPLETE SUCCESSFULLY!")
        print("Demo Account Credentials:")
        print("Owner:  demo@bijlisave.in    Password:  Bijli@2026")
        print("Family: family@bijlisave.in  Password:  Bijli@2026")
        print("Household Invite Code: BIJLI888")
        print("=======================================================\n")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
