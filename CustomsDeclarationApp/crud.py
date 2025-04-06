from sqlalchemy.orm import Session
from typing import Optional  # Добавьте этот импорт
import models, schemas

def get_countries(db: Session):
    return db.query(models.Country).all()

def create_country(db: Session, country: schemas.CountryCreate):
    db_country = models.Country(name=country.name, code=country.code)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def get_consignees(db: Session):
    return db.query(models.Consignee).all()

def create_consignee(db: Session, consignee: schemas.ConsigneeCreate):
    db_consignee = models.Consignee(
        name=consignee.name, 
        address=consignee.address, 
        identification_type=consignee.identification_type, 
        identification_number=consignee.identification_number
    )
    db.add(db_consignee)
    db.commit()
    db.refresh(db_consignee)
    return db_consignee

def update_country(db: Session, country_id: int, name: str, code: str):
    db_country = db.query(models.Country).filter(models.Country.id == country_id).first()
    if db_country:
        print(f"Updating country {country_id} with name: {name} and code: {code}")
        db_country.name = name
        db_country.code = code
        db.commit()
        db.refresh(db_country)
        return db_country
    else:
        print(f"Country {country_id} not found")
    return None

def delete_country(db: Session, country_id: int):
    db_country = db.query(models.Country).filter(models.Country.id == country_id).first()
    if db_country:
        db.delete(db_country)
        db.commit()
    return db_country

def update_consignee(db: Session, consignee_id: int, name: str, address: str, identification_type: Optional[str], identification_number: Optional[str]):
    db_consignee = db.query(models.Consignee).filter(models.Consignee.id == consignee_id).first()
    if db_consignee:
        db_consignee.name = name
        db_consignee.address = address
        db_consignee.identification_type = identification_type
        db_consignee.identification_number = identification_number
        db.commit()
        db.refresh(db_consignee)
    return db_consignee

def delete_consignee(db: Session, consignee_id: int):
    db_consignee = db.query(models.Consignee).filter(models.Consignee.id == consignee_id).first()
    if db_consignee:
        db.delete(db_consignee)
        db.commit()
    return db_consignee

def get_incoterms(db: Session):
    return db.query(models.Incoterm).all()

def create_incoterm(db: Session, incoterm: schemas.IncotermCreate):
    db_incoterm = models.Incoterm(**incoterm.model_dump())
    db.add(db_incoterm)
    db.commit()
    db.refresh(db_incoterm)
    return db_incoterm

def update_incoterm(db: Session, incoterm_id: int, code: str, description: Optional[str]):
    db_incoterm = db.query(models.Incoterm).filter(models.Incoterm.id == incoterm_id).first()
    if db_incoterm:
        db_incoterm.code = code
        db_incoterm.description = description
        db.commit()
        db.refresh(db_incoterm)
    return db_incoterm

def delete_incoterm(db: Session, incoterm_id: int):
    db_incoterm = db.query(models.Incoterm).filter(models.Incoterm.id == incoterm_id).first()
    if db_incoterm:
        db.delete(db_incoterm)
        db.commit()
    return db_incoterm

def get_transport_modes(db: Session):
    return db.query(models.TransportMode).all()

def create_transport_mode(db: Session, transport_mode: schemas.TransportModeCreate):
    db_mode = models.TransportMode(name=transport_mode.name)
    db.add(db_mode)
    db.commit()
    db.refresh(db_mode)
    return db_mode

def update_transport_mode(db: Session, mode_id: int, name: str):
    db_mode = db.query(models.TransportMode).filter(models.TransportMode.id == mode_id).first()
    if db_mode:
        db_mode.name = name
        db.commit()
        db.refresh(db_mode)
    return db_mode

def delete_transport_mode(db: Session, mode_id: int):
    db_mode = db.query(models.TransportMode).filter(models.TransportMode.id == mode_id).first()
    if db_mode:
        db.delete(db_mode)
        db.commit()
    return db_mode

def get_packages(db: Session):
    return db.query(models.Package).all()

def create_package(db: Session, package: schemas.PackageCreate):
    db_package = models.Package(**package.model_dump())
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package

def update_package(db: Session, package_id: int, type: str, description: Optional[str]):
    db_package = db.query(models.Package).filter(models.Package.id == package_id).first()
    if db_package:
        db_package.type = type
        db_package.description = description
        db.commit()
        db.refresh(db_package)
    return db_package

def delete_package(db: Session, package_id: int):
    db_package = db.query(models.Package).filter(models.Package.id == package_id).first()
    if db_package:
        db.delete(db_package)
        db.commit()
    return db_package

def get_harmonized_codes(db: Session):
    return db.query(models.HarmonizedCode).all()

def create_harmonized_code(db: Session, code: schemas.HarmonizedCodeCreate):
    db_code = models.HarmonizedCode(**code.model_dump())
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code

def update_harmonized_code(db: Session, code_id: int, code: str, description: Optional[str]):
    db_code = db.query(models.HarmonizedCode).filter(models.HarmonizedCode.id == code_id).first()
    if db_code:
        db_code.code = code
        db_code.description = description
        db.commit()
        db.refresh(db_code)
    return db_code

def delete_harmonized_code(db: Session, code_id: int):
    db_code = db.query(models.HarmonizedCode).filter(models.HarmonizedCode.id == code_id).first()
    if db_code:
        db.delete(db_code)
        db.commit()
    return db_code


def get_customs_offices(db: Session):
    return db.query(models.CustomsOffice).all()

def create_customs_office(db: Session, office: schemas.CustomsOfficeCreate):
    db_office = models.CustomsOffice(**office.model_dump())
    db.add(db_office)
    db.commit()
    db.refresh(db_office)
    return db_office

def update_customs_office(db: Session, office_id: int, code: str, location: str):
    db_office = db.query(models.CustomsOffice).filter(models.CustomsOffice.id == office_id).first()
    if db_office:
        db_office.code = code
        db_office.location = location
        db.commit()
        db.refresh(db_office)
    return db_office

def delete_customs_office(db: Session, office_id: int):
    db_office = db.query(models.CustomsOffice).filter(models.CustomsOffice.id == office_id).first()
    if db_office:
        db.delete(db_office)
        db.commit()
    return db_office

def get_currencies(db: Session):
    return db.query(models.Currency).all()

def create_currency(db: Session, currency: schemas.CurrencyCreate):
    db_currency = models.Currency(**currency.model_dump())
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency

def update_currency(db: Session, currency_id: int, code: str, name: str):
    db_currency = db.query(models.Currency).filter(models.Currency.id == currency_id).first()
    if db_currency:
        db_currency.code = code
        db_currency.name = name
        db.commit()
        db.refresh(db_currency)
    return db_currency

def delete_currency(db: Session, currency_id: int):
    db_currency = db.query(models.Currency).filter(models.Currency.id == currency_id).first()
    if db_currency:
        db.delete(db_currency)
        db.commit()
    return db_currency


def get_documents(db: Session):
    return db.query(models.Document).all()

def create_document(db: Session, document: schemas.DocumentCreate):
    db_doc = models.Document(**document.model_dump())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def update_document(db: Session, doc_id: int, type: str, description: str):
    db_doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if db_doc:
        db_doc.type = type
        db_doc.description = description
        db.commit()
        db.refresh(db_doc)
    return db_doc

def delete_document(db: Session, doc_id: int):
    db_doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if db_doc:
        db.delete(db_doc)
        db.commit()
    return db_doc

def get_exporters(db: Session):
    return db.query(models.Exporter).all()

def create_exporter(db: Session, exporter: schemas.ExporterCreate):
    db_exporter = models.Exporter(**exporter.model_dump())
    db.add(db_exporter)
    db.commit()
    db.refresh(db_exporter)
    return db_exporter

def update_exporter(db: Session, exporter_id: int, exporter_data: schemas.ExporterCreate):
    db_exporter = db.query(models.Exporter).filter(models.Exporter.id == exporter_id).first()
    if db_exporter:
        for field, value in exporter_data.model_dump().items():
            setattr(db_exporter, field, value)
        db.commit()
        db.refresh(db_exporter)
    return db_exporter

def delete_exporter(db: Session, exporter_id: int):
    db_exporter = db.query(models.Exporter).filter(models.Exporter.id == exporter_id).first()
    if db_exporter:
        db.delete(db_exporter)
        db.commit()
    return db_exporter

def create_declaration(db: Session, declaration: schemas.DeclarationCreate):
    db_decl = models.Declaration(**declaration.model_dump())
    db.add(db_decl)
    db.commit()
    db.refresh(db_decl)
    return db_decl
