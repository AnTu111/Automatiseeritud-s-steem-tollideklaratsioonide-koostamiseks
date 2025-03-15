print(" Запуск database.py...")
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

print("Загружаем .env файл...")
load_dotenv()

print("Получаем DATABASE_URL...")
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL: {DATABASE_URL}")

print("Создаём движок SQLAlchemy...")
engine = create_engine(DATABASE_URL)

print("Проверяем подключение к базе...")
try:
    with engine.connect() as connection:
        print("Успешное подключение к базе данных!")
except Exception as e:
    print(f"Ошибка подключения: {e}")

print("Настраиваем сессию...")
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

print("Определяем базовый класс для моделей...")
Base = declarative_base()

print("`database.py` выполнен успешно!")

