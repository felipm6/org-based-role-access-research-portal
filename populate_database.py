"""
Script to populate the database with sample data
"""

from sqlalchemy.orm import Session
from src.connection import SessionLocal
from src.models.database import (
    Organization,
    User,
    Study,
    Session as StudySession,
    UserRole,
)
from datetime import datetime, timedelta
import bcrypt
import uuid


def hash_password(password: str) -> str:
    """Hash the password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_sample_data():
    """Create sample data for the database"""
    print("🔄 Creating sample data...")

    db: Session = SessionLocal()

    try:
        # Check if data already exists
        if db.query(Organization).first():
            print("ℹ️  Data already exists in the database")
            return

        # Create one simple organization
        org = Organization(id=str(uuid.uuid4()), name="Research University")

        db.add(org)
        db.flush()  # To get the ID

        # Create users - one for each role type with simple passwords
        # ADMIN user
        admin_user = User(
            id=str(uuid.uuid4()),
            client_id="admin",
            client_secret_hash=hash_password("admin1234"),
            email="admin@research.edu",
            name="Admin User",
            org_id=org.id,
            role=UserRole.ADMIN,
        )

        # STUDY_COORDINATOR user
        coordinator_user = User(
            id=str(uuid.uuid4()),
            client_id="study_coordinator",
            client_secret_hash=hash_password("study_coordinator1234"),
            email="coordinator@research.edu",
            name="Study Coordinator User",
            org_id=org.id,
            role=UserRole.STUDY_COORDINATOR,
        )

        # RESEARCH_ASSISTANT user
        assistant_user = User(
            id=str(uuid.uuid4()),
            client_id="research_assistant",
            client_secret_hash=hash_password("research_assistant1234"),
            email="assistant@research.edu",
            name="Research Assistant User",
            org_id=org.id,
            role=UserRole.RESEARCH_ASSISTANT,
        )

        # PARTICIPANT user
        participant_user = User(
            id=str(uuid.uuid4()),
            client_id="participant",
            client_secret_hash=hash_password("participant1234"),
            email="participant@research.edu",
            name="Participant User",
            org_id=org.id,
            role=UserRole.PARTICIPANT,
        )

        db.add_all([admin_user, coordinator_user, assistant_user, participant_user])

        # Commit all changes
        db.commit()

        print("✅ Sample data created successfully!")
        print("\n📊 Data created:")
        print(f"   🏢 Organizations: 1")
        print(f"   👥 Users: 4")

        print("\nSimple test credentials:")
        print("   ADMIN:")
        print(f"     - Client ID: admin")
        print(f"     - Password: admin1234")
        print("\n   STUDY_COORDINATOR:")
        print(f"     - Client ID: study_coordinator")
        print(f"     - Password: study_coordinator1234")
        print("\n   RESEARCH_ASSISTANT:")
        print(f"     - Client ID: research_assistant")
        print(f"     - Password: research_assistant1234")
        print("\n   PARTICIPANT:")
        print(f"     - Client ID: participant")
        print(f"     - Password: participant1234")

    except Exception as e:
        print(f"❌ Error creating data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()
