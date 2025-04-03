from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, CheckConstraint, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)



class Incoterm(Base):
    __tablename__ = "incoterms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text)



class TransportMode(Base):
    __tablename__ = "transport_modes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)


#  (Consignees)
class Consignee(Base):
    __tablename__ = "consignees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    identification_type = Column(String(100))
    identification_number = Column(String(100), unique=True)



class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(255), unique=True, nullable=False)
    description = Column(Text)



class HarmonizedCode(Base):
    __tablename__ = "harmonized_codes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), unique=True, nullable=False)
    description = Column(Text)



class Declaration(Base):
    __tablename__ = "declarations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference_number = Column(String(100), unique=True, nullable=False)
    agent_number = Column(String(100))
    invoice_currency = Column(String(50))
    location = Column(String(255))
    transport_document = Column(String(255))
    validity_date = Column(String(50))  # Можно сделать Date, если нужно

    country_of_destination_id = Column(Integer, ForeignKey("countries.id"))
    incoterm_id = Column(Integer, ForeignKey("incoterms.id"))

    country_of_destination = relationship("Country")
    incoterm = relationship("Incoterm")


#  (Goods)
class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    declaration_id = Column(Integer, ForeignKey("declarations.id"), nullable=False)
    description = Column(String(500), nullable=False)
    gross_mass = Column(Float)
    net_mass = Column(Float)
    number_of_packages = Column(Integer)
    statistical_value = Column(Float)

    harmonized_code_id = Column(Integer, ForeignKey("harmonized_codes.id"))
    package_id = Column(Integer, ForeignKey("packages.id"))

    declaration = relationship("Declaration")
    harmonized_code = relationship("HarmonizedCode")
    package = relationship("Package")

    __table_args__ = (
        CheckConstraint("gross_mass >= 0", name="check_gross_mass"),
        CheckConstraint("net_mass >= 0", name="check_net_mass"),
        CheckConstraint("statistical_value >= 0", name="check_statistical_value"),
    )

class CustomsOffice(Base):
    __tablename__ = "customs_offices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    location = Column(String(255), nullable=False)

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=False)





# Подключаемся к MySQL
engine = create_engine("mysql+pymysql://root@localhost/customs_declarations")

# Создаем таблицы
Base.metadata.create_all(engine)

print("✅ All tables have been successfully created!")
