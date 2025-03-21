from sqlalchemy import Column, Integer, String, Float, Date, CheckConstraint, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CustomsDeclaration(Base):
    __tablename__ = "customs_declaration"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(255), nullable=False, index=True)
    gross_mass = Column(Float, nullable=False)
    statistical_value = Column(Float, nullable=False)
    description_of_goods = Column(String(500), nullable=False)
    net_mass = Column(Float, nullable=False)
    sequence_number = Column(Integer, nullable=False)
    reference_number = Column(String(50), nullable=False)
    validity_date = Column(Date, nullable=False)
    country = Column(String(100), nullable=False)

    __table_args__ = (
        CheckConstraint("statistical_value >= 0", name="check_statistical_value"),
        CheckConstraint("net_mass >= 0", name="check_net_mass"),
    )

# 🔥 Подключаем MySQL, а не SQLite!
engine = create_engine("mysql+pymysql://root@localhost/customs_declarations")

Base.metadata.create_all(engine)  # Создаем таблицы
print("✅ Таблица успешно создана в MySQL!")
