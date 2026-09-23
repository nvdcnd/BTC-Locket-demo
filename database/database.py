from sqlmodel import SQLModel, create_engine, Session
import dotenv
import os

dotenv.load_dotenv()  # Load environment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Default to SQLite if not set

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    import database.models as models
    SQLModel.metadata.create_all(engine)  # Create tables if they don't exist