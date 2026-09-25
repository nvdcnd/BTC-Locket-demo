from sqlmodel import SQLModel, create_engine, Session
import dotenv
import os

dotenv.load_dotenv()  # Load environment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Default to SQLite if not set
DB_ECHO = os.getenv("DB_ECHO", "false").lower() in {"1", "true", "yes", "on"}

# Không log mặc định ở production: SQL echo làm tốn I/O và có thể ghi metadata/caption vào log.
# pool_pre_ping giúp phát hiện connection đã bị provider/proxy đóng trước khi query.
engine = create_engine(
    DATABASE_URL,
    echo=DB_ECHO,
    pool_pre_ping=True,
)

def create_db_and_tables():
    import database.models as models
    SQLModel.metadata.create_all(engine)  # Create tables if they don't exist