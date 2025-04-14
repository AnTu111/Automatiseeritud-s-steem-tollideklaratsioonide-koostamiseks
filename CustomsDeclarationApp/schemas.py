from pydantic import BaseModel
from typing import Optional, List

# --- Country ---
class CountryBase(BaseModel):
    name: str
    code: str

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    id: int

    class Config:
        from_attributes = True

# --- Consignee ---
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

# --- Incoterm ---
class IncotermBase(BaseModel):
    code: str
    description: Optional[str] = None

class IncotermCreate(IncotermBase):
    pass

class Incoterm(IncotermBase):
    id: int

    class Config:
        from_attributes = True

# --- TransportMode ---
class TransportModeBase(BaseModel):
    name: str

class TransportModeCreate(TransportModeBase):
    pass

class TransportMode(TransportModeBase):
    id: int

    class Config:
        from_attributes = True

# --- Package ---
class PackageBase(BaseModel):
    type: str
    description: Optional[str] = None

class PackageCreate(PackageBase):
    pass

class Package(PackageBase):
    id: int

    class Config:
        from_attributes = True

# --- HarmonizedCode ---
class HarmonizedCodeBase(BaseModel):
    code: str
    description: Optional[str] = None

class HarmonizedCodeCreate(HarmonizedCodeBase):
    pass

class HarmonizedCode(HarmonizedCodeBase):
    id: int

    class Config:
        from_attributes = True

# --- CustomsOffice ---
class CustomsOfficeBase(BaseModel):
    code: str
    location: str

class CustomsOfficeCreate(CustomsOfficeBase):
    pass

class CustomsOffice(CustomsOfficeBase):
    id: int

    class Config:
        from_attributes = True

# --- Currency ---
class CurrencyBase(BaseModel):
    code: str
    name: str

class CurrencyCreate(CurrencyBase):
    pass

class Currency(CurrencyBase):
    id: int

    class Config:
        from_attributes = True

# --- Document (Справочник SupportingDocument) ---
class DocumentBase(BaseModel):
    type: str
    description: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int

    class Config:
        from_attributes = True

# --- Exporter ---
class ExporterBase(BaseModel):
    name: str
    identification_number: str
    street: Optional[str] = None
    postcode: Optional[str] = None
    city: Optional[str] = None
    country_code: Optional[str] = None

class ExporterCreate(ExporterBase):
    pass

class Exporter(ExporterBase):
    id: int

    class Config:
        from_attributes = True

# --- Supporting Document (связка: декларация + документ + номер) ---
class SupportingDocumentBase(BaseModel):
    document_id: int
    reference_number: str

class SupportingDocumentCreate(SupportingDocumentBase):
    pass

class SupportingDocument(SupportingDocumentBase):
    id: int

    class Config:
        from_attributes = True

# --- Declaration ---
class DeclarationBase(BaseModel):
    reference_number: str
    exporter_id: int
    consignee_id: int
    country_of_destination_id: int
    incoterm_id: int
    currency_id: int
    customs_office_id: int
    transport_mode_id: int
    location: Optional[str] = None
    lrn: Optional[str] = None
    total_amount_invoiced: Optional[float] = None
    invoice_currency: Optional[str] = None

class DeclarationCreate(DeclarationBase):
    supporting_documents: Optional[List[SupportingDocumentCreate]] = []

class Declaration(DeclarationBase):
    id: int

    class Config:
        from_attributes = True
