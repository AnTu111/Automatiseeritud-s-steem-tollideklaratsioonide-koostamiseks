from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Настройки базы данных
DB_URL = "mysql+pymysql://root:@localhost/customs_declarations"

# Создание движка
engine = create_engine(DB_URL)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс моделей
Base = declarative_base()
