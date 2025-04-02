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

class IncotermBase(BaseModel):
    code: str
    description: Optional[str] = None

class IncotermCreate(IncotermBase):
    pass

class Incoterm(IncotermBase):
    id: int

    class Config:
        from_attributes = True

class TransportModeBase(BaseModel):
    name: str

class TransportModeCreate(TransportModeBase):
    pass

class TransportMode(TransportModeBase):
    id: int

    class Config:
        from_attributes = True

class PackageBase(BaseModel):
    type: str
    description: Optional[str] = None

class PackageCreate(PackageBase):
    pass

class Package(PackageBase):
    id: int

    class Config:
        from_attributes = True

class HarmonizedCodeBase(BaseModel):
    code: str
    description: Optional[str] = None

class HarmonizedCodeCreate(HarmonizedCodeBase):
    pass

class HarmonizedCode(HarmonizedCodeBase):
    id: int

    class Config:
        from_attributes = True
