import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Берём адрес базы из переменной окружения (в Docker мы её зададим)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:pass@db:5432/habits")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()