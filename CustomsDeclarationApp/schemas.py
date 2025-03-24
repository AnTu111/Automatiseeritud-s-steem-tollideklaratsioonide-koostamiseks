from pydantic import BaseModel
from typing import Optional

class CountryBase(BaseModel):
    name: str
    code: str

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    id: int

    class Config:
        from_attributes = True

class ConsigneeBase(BaseModel):
    name: str
    address: str
    identification_type: Optional[str] = None
    identification_number: Optional[str] = None

class ConsigneeCreate(ConsigneeBase):
    pass

class Consignee(ConsigneeBase):
    id: int

    class Config:
        from_attributes = True
