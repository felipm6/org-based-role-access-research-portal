from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.database import Base
from src.constants import SQLITE_URL
import os


def create_database():
    print("Creating SQLite database...")

    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)

    print("✅ Database created successfully!")
    print(f"📍 Connection URL: {SQLITE_URL}")
    print(f"📍 File location: {os.path.abspath('research_portal.db')}")

    return engine


def get_database_session():
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


if __name__ == "__main__":
    create_database()
