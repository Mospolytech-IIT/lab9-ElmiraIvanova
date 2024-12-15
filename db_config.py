from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db_models import Base

DATABASE_URL = "postgresql://elmira:1230984576@localhost:5432/my_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц в базе данных
if __name__ == "__main__":
    # Создаем все таблицы, определённые в моделях
    Base.metadata.create_all(engine)
    print("Таблицы Users и Posts успешно созданы.")