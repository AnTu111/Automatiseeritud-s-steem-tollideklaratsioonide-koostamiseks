from sqlalchemy.orm import Session
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

