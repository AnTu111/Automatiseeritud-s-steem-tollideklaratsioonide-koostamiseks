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
