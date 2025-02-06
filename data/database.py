# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_bas
# from sqlalchemy.orm import sessionmaker
# import os
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL is not set in the .env file")

# # Create the database engine
# engine = create_engine(DATABASE_URL)

# # Create a session factory
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for all ORM models
# Base = declarative_base()

# # Import models to register them with the database
# from data.models import *

# # Create all tables in the database
# def initialize_database():
#     Base.metadata.create_all(bind=engine)

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import declarative_base
# from dotenv import load_dotenv
# import os
# import sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from .models import *

# load_dotenv()

# # Database configuration
# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL is not set in the environment variables")

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Helper function to get a database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Database initialization function
# def initialize_database():
#     """
#     Create all tables in the database based on the models.
#     """
#     Base.metadata.create_all(bind=engine)
#     print("Database initialized successfully.")


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables")

engine = create_engine(DATABASE_URL)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    raise SystemExit(f"Database connection failed: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Helper function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database initialization function
def initialize_database():
    """
    Create all tables in the database based on the models.
    """
    from data.models import MoodLog
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")