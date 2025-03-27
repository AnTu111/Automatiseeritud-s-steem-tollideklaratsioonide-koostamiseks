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
