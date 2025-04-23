from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), nullable=False)

class Consignee(Base):
    __tablename__ = "consignees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    identification_type = Column(String(100), nullable=True)
    identification_number = Column(String(100), nullable=True)

class Incoterm(Base):
    __tablename__ = "incoterms"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), nullable=False)
    description = Column(String(255), nullable=True)

class TransportMode(Base):
    __tablename__ = "transport_modes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)

class HarmonizedCode(Base):
    __tablename__ = "harmonized_codes"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), nullable=False)
    description = Column(String(255), nullable=True)

class CustomsOffice(Base):
    __tablename__ = "customs_offices"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), nullable=False)
    location = Column(String(255), nullable=False)

class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False)

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=False)

    supporting_documents = relationship("SupportingDocument", back_populates="document")

class Exporter(Base):
    __tablename__ = "exporters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    identification_number = Column(String(100), nullable=False)
    street = Column(String(255), nullable=True)
    postcode = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    country_code = Column(String(10), nullable=True)

class Declaration(Base):
    __tablename__ = "declarations"
    id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String(100), nullable=False)
    exporter_id = Column(Integer, ForeignKey("exporters.id"))
    consignee_id = Column(Integer, ForeignKey("consignees.id"))
    country_of_destination_id = Column(Integer, ForeignKey("countries.id"))
    incoterm_id = Column(Integer, ForeignKey("incoterms.id"))
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    customs_office_id = Column(Integer, ForeignKey("customs_offices.id"))
    # transport_mode_id = Column(Integer, ForeignKey("transport_modes.id"))
    location = Column(String(255), nullable=True)
    lrn = Column(String(100), nullable=True)
    total_amount_invoiced = Column(Integer, nullable=True)
    invoice_currency = Column(String(10), nullable=True)

    # ✅ новые поля
    container_indicator = Column(Integer, nullable=False, default=0)
    inland_transport_mode_id = Column(Integer, ForeignKey("transport_modes.id"))
    border_transport_mode_id = Column(Integer, ForeignKey("transport_modes.id"))

    exporter = relationship("Exporter")
    consignee = relationship("Consignee")
    country_of_destination = relationship("Country")
    incoterm = relationship("Incoterm")
    currency = relationship("Currency")
    customs_office = relationship("CustomsOffice")
    inland_transport_mode = relationship("TransportMode", foreign_keys=[inland_transport_mode_id])
    border_transport_mode = relationship("TransportMode", foreign_keys=[border_transport_mode_id])

    # transport_mode = relationship("TransportMode", foreign_keys=[transport_mode_id])

    # ✅ новые связи

    # 💾 связи
    supporting_documents = relationship("SupportingDocument", back_populates="declaration", cascade="all, delete-orphan")
    goods = relationship("Goods", back_populates="declaration", cascade="all, delete-orphan")

class SupportingDocument(Base):
    __tablename__ = "supporting_documents"
    id = Column(Integer, primary_key=True, index=True)
    declaration_id = Column(Integer, ForeignKey("declarations.id"))
    document_id = Column(Integer, ForeignKey("documents.id"))
    reference_number = Column(String(100))

    declaration = relationship("Declaration", back_populates="supporting_documents")
    document = relationship("Document", back_populates="supporting_documents")

class Goods(Base):
    __tablename__ = "goods"
    id = Column(Integer, primary_key=True, index=True)
    declaration_id = Column(Integer, ForeignKey("declarations.id"))
    harmonized_code_id = Column(Integer, ForeignKey("harmonized_codes.id"))
    package_id = Column(Integer, ForeignKey("packages.id"))
    description = Column(String(255), nullable=True)
    gross_mass = Column(Integer, nullable=True)
    net_mass = Column(Integer, nullable=True)
    number_of_packages = Column(Integer, nullable=True)
    statistical_value = Column(Integer, default=0)

    declaration = relationship("Declaration", back_populates="goods")
    harmonized_code = relationship("HarmonizedCode")
    package = relationship("Package")

# Добавим связь в Declaration:
Declaration.goods = relationship("Goods", back_populates="declaration", cascade="all, delete-orphan")

