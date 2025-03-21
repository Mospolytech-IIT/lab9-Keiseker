from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Убираем connect_args для PostgreSQL, так как это не требуется для него
DATABASE_URL = "postgresql://postgres:8085@localhost:5432/db"

engine = create_engine(DATABASE_URL)  # Просто создаем engine без connect_args
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Получение сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
