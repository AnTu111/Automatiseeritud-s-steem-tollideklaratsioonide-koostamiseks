from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal
from typing import Optional
from fastapi.responses import StreamingResponse
from lxml import etree
import io
from fastapi.staticfiles import StaticFiles

app = FastAPI(debug=True)

# Подключение папки static
app.mount("/static", StaticFiles(directory="static"), name="static")


# Подключаем Jinja2
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Главная страница
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Страница со странами
@app.get("/countries", response_class=HTMLResponse)
def country_list(request: Request, db: Session = Depends(get_db)):
    countries = crud.get_countries(db)
    return templates.TemplateResponse("countries.html", {"request": request, "countries": countries})

# Форма добавления страны
@app.post("/countries/add")
def add_country(name: str = Form(...), code: str = Form(...), db: Session = Depends(get_db)):
    crud.create_country(db, schemas.CountryCreate(name=name, code=code))
    return RedirectResponse(url="/countries", status_code=303)

# Страница редактирования страны
@app.get("/countries/edit/{country_id}", response_class=HTMLResponse)
def edit_country_page(request: Request, country_id: int, db: Session = Depends(get_db)):
    country = db.query(models.Country).filter(models.Country.id == country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return templates.TemplateResponse("update_country.html", {"request": request, "country": country})

# Обновление страны
@app.post("/countries/edit/{country_id}")
def update_country_post(country_id: int, name: str = Form(...), code: str = Form(...), db: Session = Depends(get_db)):
    print(f"Received country data to update: {country_id}, {name}, {code}")
    country = crud.update_country(db, country_id, name, code)
    if country:
        print(f"Country updated: {country}")
        return RedirectResponse(url="/countries", status_code=303)
    raise HTTPException(status_code=404, detail="Country not found")

# Удаление страны
@app.post("/countries/delete/{country_id}")
def delete_country_post(country_id: int, db: Session = Depends(get_db)):
    country = crud.delete_country(db, country_id)
    if country:
        return RedirectResponse(url="/countries", status_code=303)
    raise HTTPException(status_code=404, detail="Country not found")

# Страница с получателями
@app.get("/consignees", response_class=HTMLResponse)
def consignee_list(request: Request, db: Session = Depends(get_db)):
    consignees = crud.get_consignees(db)
    return templates.TemplateResponse("consignees.html", {"request": request, "consignees": consignees})

# Форма добавления получателя
@app.post("/consignees/add")
def add_consignee(name: str = Form(...), address: str = Form(...), db: Session = Depends(get_db)):
    consignee = schemas.ConsigneeCreate(name=name, address=address)
    crud.create_consignee(db, consignee)
    return RedirectResponse(url="/consignees", status_code=303)

# Страница редактирования получателя
@app.get("/consignees/edit/{consignee_id}", response_class=HTMLResponse)
def edit_consignee_page(request: Request, consignee_id: int, db: Session = Depends(get_db)):
    consignee = db.query(models.Consignee).filter(models.Consignee.id == consignee_id).first()
    if not consignee:
        raise HTTPException(status_code=404, detail="Consignee not found")
    return templates.TemplateResponse("update_consignee.html", {"request": request, "consignee": consignee})

# Обновление получателя
@app.post("/consignees/edit/{consignee_id}")
def update_consignee_post(consignee_id: int, name: str = Form(...), address: str = Form(...), identification_type: Optional[str] = None, identification_number: Optional[str] = None, db: Session = Depends(get_db)):
    consignee = crud.update_consignee(db, consignee_id, name, address, identification_type, identification_number)
    if consignee:
        return RedirectResponse(url="/consignees", status_code=303)
    raise HTTPException(status_code=404, detail="Consignee not found")

# Удаление получателя
@app.post("/consignees/delete/{consignee_id}")
def delete_consignee_post(consignee_id: int, db: Session = Depends(get_db)):
    consignee = crud.delete_consignee(db, consignee_id)
    if consignee:
        return RedirectResponse(url="/consignees", status_code=303)
    raise HTTPException(status_code=404, detail="Consignee not found")

@app.get("/incoterms", response_class=HTMLResponse)
def incoterm_list(request: Request, db: Session = Depends(get_db)):
    incoterms = crud.get_incoterms(db)
    return templates.TemplateResponse("incoterms.html", {"request": request, "incoterms": incoterms})

@app.post("/incoterms/add")
def add_incoterm(code: str = Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    crud.create_incoterm(db, schemas.IncotermCreate(code=code, description=description))
    return RedirectResponse(url="/incoterms", status_code=303)

@app.get("/incoterms/edit/{incoterm_id}", response_class=HTMLResponse)
def edit_incoterm_page(incoterm_id: int, request: Request, db: Session = Depends(get_db)):
    incoterm = db.query(models.Incoterm).filter(models.Incoterm.id == incoterm_id).first()
    return templates.TemplateResponse("update_incoterm.html", {"request": request, "incoterm": incoterm})

@app.post("/incoterms/edit/{incoterm_id}")
def edit_incoterm(incoterm_id: int, code: str = Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    crud.update_incoterm(db, incoterm_id, code, description)
    return RedirectResponse(url="/incoterms", status_code=303)

@app.post("/incoterms/delete/{incoterm_id}")
def delete_incoterm(incoterm_id: int, db: Session = Depends(get_db)):
    crud.delete_incoterm(db, incoterm_id)
    return RedirectResponse(url="/incoterms", status_code=303)

@app.get("/transport_modes", response_class=HTMLResponse)
def transport_modes(request: Request, db: Session = Depends(get_db)):
    modes = crud.get_transport_modes(db)
    return templates.TemplateResponse("transport_modes.html", {"request": request, "transport_modes": modes})

@app.post("/transport_modes/add")
def add_transport_mode(name: str = Form(...), db: Session = Depends(get_db)):
    crud.create_transport_mode(db, schemas.TransportModeCreate(name=name))
    return RedirectResponse(url="/transport_modes", status_code=303)

@app.get("/transport_modes/edit/{mode_id}", response_class=HTMLResponse)
def edit_transport_mode_page(mode_id: int, request: Request, db: Session = Depends(get_db)):
    mode = db.query(models.TransportMode).filter(models.TransportMode.id == mode_id).first()
    return templates.TemplateResponse("update_transport_mode.html", {"request": request, "transport_mode": mode})

@app.post("/transport_modes/edit/{mode_id}")
def edit_transport_mode(mode_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    crud.update_transport_mode(db, mode_id, name)
    return RedirectResponse(url="/transport_modes", status_code=303)

@app.post("/transport_modes/delete/{mode_id}")
def delete_transport_mode(mode_id: int, db: Session = Depends(get_db)):
    crud.delete_transport_mode(db, mode_id)
    return RedirectResponse(url="/transport_modes", status_code=303)

@app.get("/packages", response_class=HTMLResponse)
def package_list(request: Request, db: Session = Depends(get_db)):
    packages = crud.get_packages(db)
    return templates.TemplateResponse("packages.html", {"request": request, "packages": packages})

@app.post("/packages/add")
def add_package(type: str = Form(...), description: Optional[str] = Form(None), db: Session = Depends(get_db)):
    crud.create_package(db, schemas.PackageCreate(type=type, description=description))
    return RedirectResponse(url="/packages", status_code=303)

@app.get("/packages/edit/{package_id}", response_class=HTMLResponse)
def edit_package_page(package_id: int, request: Request, db: Session = Depends(get_db)):
    package = db.query(models.Package).filter(models.Package.id == package_id).first()
    return templates.TemplateResponse("update_package.html", {"request": request, "package": package})

@app.post("/packages/edit/{package_id}")
def edit_package(package_id: int, type: str = Form(...), description: Optional[str] = Form(None), db: Session = Depends(get_db)):
    crud.update_package(db, package_id, type, description)
    return RedirectResponse(url="/packages", status_code=303)

@app.post("/packages/delete/{package_id}")
def delete_package(package_id: int, db: Session = Depends(get_db)):
    crud.delete_package(db, package_id)
    return RedirectResponse(url="/packages", status_code=303)

@app.get("/harmonized_codes", response_class=HTMLResponse)
def harmonized_code_list(request: Request, db: Session = Depends(get_db)):
    codes = crud.get_harmonized_codes(db)
    return templates.TemplateResponse("harmonized_codes.html", {"request": request, "codes": codes})

@app.post("/harmonized_codes/add")
def add_harmonized_code(code: str = Form(...), description: Optional[str] = Form(None), db: Session = Depends(get_db)):
    crud.create_harmonized_code(db, schemas.HarmonizedCodeCreate(code=code, description=description))
    return RedirectResponse(url="/harmonized_codes", status_code=303)

@app.get("/harmonized_codes/edit/{code_id}", response_class=HTMLResponse)
def edit_harmonized_code_page(code_id: int, request: Request, db: Session = Depends(get_db)):
    code = db.query(models.HarmonizedCode).filter(models.HarmonizedCode.id == code_id).first()
    return templates.TemplateResponse("update_harmonized_code.html", {"request": request, "code": code})

@app.post("/harmonized_codes/edit/{code_id}")
def edit_harmonized_code(code_id: int, code: str = Form(...), description: Optional[str] = Form(None), db: Session = Depends(get_db)):
    crud.update_harmonized_code(db, code_id, code, description)
    return RedirectResponse(url="/harmonized_codes", status_code=303)

@app.post("/harmonized_codes/delete/{code_id}")
def delete_harmonized_code(code_id: int, db: Session = Depends(get_db)):
    crud.delete_harmonized_code(db, code_id)
    return RedirectResponse(url="/harmonized_codes", status_code=303)


@app.get("/customs_offices", response_class=HTMLResponse)
def customs_office_list(request: Request, db: Session = Depends(get_db)):
    offices = crud.get_customs_offices(db)
    return templates.TemplateResponse("customs_offices.html", {"request": request, "offices": offices})

@app.post("/customs_offices/add")
def add_customs_office(code: str = Form(...), location: str = Form(...), db: Session = Depends(get_db)):
    crud.create_customs_office(db, schemas.CustomsOfficeCreate(code=code, location=location))
    return RedirectResponse(url="/customs_offices", status_code=303)

@app.get("/customs_offices/edit/{office_id}", response_class=HTMLResponse)
def edit_customs_office_page(office_id: int, request: Request, db: Session = Depends(get_db)):
    office = db.query(models.CustomsOffice).filter(models.CustomsOffice.id == office_id).first()
    return templates.TemplateResponse("update_customs_office.html", {"request": request, "office": office})

@app.post("/customs_offices/edit/{office_id}")
def edit_customs_office(office_id: int, code: str = Form(...), location: str = Form(...), db: Session = Depends(get_db)):
    crud.update_customs_office(db, office_id, code, location)
    return RedirectResponse(url="/customs_offices", status_code=303)

@app.post("/customs_offices/delete/{office_id}")
def delete_customs_office(office_id: int, db: Session = Depends(get_db)):
    crud.delete_customs_office(db, office_id)
    return RedirectResponse(url="/customs_offices", status_code=303)

@app.get("/currencies", response_class=HTMLResponse)
def currency_list(request: Request, db: Session = Depends(get_db)):
    currencies = crud.get_currencies(db)
    return templates.TemplateResponse("currencies.html", {"request": request, "currencies": currencies})

@app.post("/currencies/add")
def add_currency(code: str = Form(...), name: str = Form(...), db: Session = Depends(get_db)):
    crud.create_currency(db, schemas.CurrencyCreate(code=code, name=name))
    return RedirectResponse(url="/currencies", status_code=303)

@app.get("/currencies/edit/{currency_id}", response_class=HTMLResponse)
def edit_currency_page(currency_id: int, request: Request, db: Session = Depends(get_db)):
    currency = db.query(models.Currency).filter(models.Currency.id == currency_id).first()
    return templates.TemplateResponse("update_currency.html", {"request": request, "currency": currency})

@app.post("/currencies/edit/{currency_id}")
def edit_currency(currency_id: int, code: str = Form(...), name: str = Form(...), db: Session = Depends(get_db)):
    crud.update_currency(db, currency_id, code, name)
    return RedirectResponse(url="/currencies", status_code=303)

@app.post("/currencies/delete/{currency_id}")
def delete_currency(currency_id: int, db: Session = Depends(get_db)):
    crud.delete_currency(db, currency_id)
    return RedirectResponse(url="/currencies", status_code=303)

@app.get("/documents", response_class=HTMLResponse)
def document_list(request: Request, db: Session = Depends(get_db)):
    documents = crud.get_documents(db)
    return templates.TemplateResponse("documents.html", {"request": request, "documents": documents})

@app.post("/documents/add")
def add_document(type: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    crud.create_document(db, schemas.DocumentCreate(type=type, description=description))
    return RedirectResponse(url="/documents", status_code=303)

@app.get("/documents/edit/{doc_id}", response_class=HTMLResponse)
def edit_document_page(doc_id: int, request: Request, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == doc_id).first()
    return templates.TemplateResponse("update_document.html", {"request": request, "document": document})

@app.post("/documents/edit/{doc_id}")
def edit_document(doc_id: int, type: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    crud.update_document(db, doc_id, type, description)
    return RedirectResponse(url="/documents", status_code=303)

@app.post("/documents/delete/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    crud.delete_document(db, doc_id)
    return RedirectResponse(url="/documents", status_code=303)

@app.get("/exporters", response_class=HTMLResponse)
def exporter_list(request: Request, db: Session = Depends(get_db)):
    exporters = crud.get_exporters(db)
    return templates.TemplateResponse("exporters.html", {"request": request, "exporters": exporters})

@app.post("/exporters/add")
def add_exporter(
    name: str = Form(...),
    identification_number: str = Form(...),
    street: str = Form(""),
    postcode: str = Form(""),
    city: str = Form(""),
    country_code: str = Form(""),
    db: Session = Depends(get_db)
):
    exporter = schemas.ExporterCreate(
        name=name,
        identification_number=identification_number,
        street=street,
        postcode=postcode,
        city=city,
        country_code=country_code
    )
    crud.create_exporter(db, exporter)
    return RedirectResponse(url="/exporters", status_code=303)

@app.get("/exporters/edit/{exporter_id}", response_class=HTMLResponse)
def edit_exporter_page(exporter_id: int, request: Request, db: Session = Depends(get_db)):
    exporter = db.query(models.Exporter).filter(models.Exporter.id == exporter_id).first()
    return templates.TemplateResponse("update_exporter.html", {"request": request, "exporter": exporter})

@app.post("/exporters/edit/{exporter_id}")
def edit_exporter(
    exporter_id: int,
    name: str = Form(...),
    identification_number: str = Form(...),
    street: str = Form(""),
    postcode: str = Form(""),
    city: str = Form(""),
    country_code: str = Form(""),
    db: Session = Depends(get_db)
):
    exporter_data = schemas.ExporterCreate(
        name=name,
        identification_number=identification_number,
        street=street,
        postcode=postcode,
        city=city,
        country_code=country_code
    )
    crud.update_exporter(db, exporter_id, exporter_data)
    return RedirectResponse(url="/exporters", status_code=303)

@app.post("/exporters/delete/{exporter_id}")
def delete_exporter(exporter_id: int, db: Session = Depends(get_db)):
    crud.delete_exporter(db, exporter_id)
    return RedirectResponse(url="/exporters", status_code=303)

@app.get("/declarations/new", response_class=HTMLResponse)
def new_declaration_form(request: Request, db: Session = Depends(get_db)):
    exporters = crud.get_exporters(db)
    countries = crud.get_countries(db)
    incoterms = crud.get_incoterms(db)
    currencies = crud.get_currencies(db)
    transport_modes = crud.get_transport_modes(db)
    customs_offices = crud.get_customs_offices(db)
    consignees = crud.get_consignees(db)
    return templates.TemplateResponse("new_declaration.html", {
        "request": request,
        "exporters": exporters,
        "countries": countries,
        "incoterms": incoterms,
        "currencies": currencies,
        "transport_modes": transport_modes,
        "customs_offices": customs_offices,
        "consignees": consignees
    })

@app.post("/declarations/add")
def add_declaration(
    request: Request,
    reference_number: str = Form(...),
    exporter_id: int = Form(...),
    consignee_id: int = Form(...),
    country_of_destination_id: int = Form(...),
    incoterm_id: int = Form(...),
    currency_id: int = Form(...),
    customs_office_id: int = Form(...),
    #transport_mode_id: int = Form(...),
    location: Optional[str] = Form(None),
    lrn: str = Form(...),
    total_amount_invoiced: float = Form(...),
    container_indicator: int = Form(...),
    inland_mode_id: int = Form(...),
    border_mode_id: int = Form(...),
    db: Session = Depends(get_db)  # ✅ db должен быть ЗДЕСЬ и только один раз
):
    # Получаем код валюты по ID
    invoice_currency = crud.get_currency_by_id(db, currency_id).code

    print("Received data:", {
        "reference_number": reference_number,
        "exporter_id": exporter_id,
        "consignee_id": consignee_id,
        "country_of_destination_id": country_of_destination_id,
        "incoterm_id": incoterm_id,
        "currency_id": currency_id,
        "customs_office_id": customs_office_id,
        #"transport_mode_id": transport_mode_id,
        "location": location,
        "lrn": lrn,
        "total_amount_invoiced": total_amount_invoiced,
        "invoice_currency": invoice_currency
    })

    declaration_data = schemas.DeclarationCreate(
        reference_number=reference_number,
        exporter_id=exporter_id,
        consignee_id=consignee_id,
        country_of_destination_id=country_of_destination_id,
        incoterm_id=incoterm_id,
        currency_id=currency_id,
        customs_office_id=customs_office_id,
        #transport_mode_id=transport_mode_id,
        container_indicator=container_indicator,
        inland_mode_id=inland_mode_id,
        border_mode_id=border_mode_id,
        location=location,
        lrn=lrn,
        total_amount_invoiced=total_amount_invoiced,
        invoice_currency=invoice_currency
    )

    declaration = crud.create_declaration(db, declaration_data)
    return RedirectResponse(url=f"/declarations/{declaration.id}", status_code=303)



@app.get("/declarations/{declaration_id}", response_class=HTMLResponse)
def view_declaration(declaration_id: int, request: Request, db: Session = Depends(get_db)):
    declaration = db.query(models.Declaration).get(declaration_id)
    if not declaration:
        raise HTTPException(status_code=404, detail="Declaration not found")

    documents = crud.get_documents(db)
    packages = db.query(models.Package).all()
    harmonized_codes = db.query(models.HarmonizedCode).all()

    return templates.TemplateResponse("declaration_detail.html", {
        "request": request,
        "declaration": declaration,
        "documents": documents,
        "packages": packages,
        "harmonized_codes": harmonized_codes
    })



@app.post("/declarations/{declaration_id}/add_document")
def add_supporting_document(
    declaration_id: int,
    document_id: int = Form(...),
    reference_number: str = Form(...),
    db: Session = Depends(get_db)
):
    from schemas import SupportingDocumentCreate

    doc_data = SupportingDocumentCreate(
        document_id=document_id,
        reference_number=reference_number
    )

    crud.add_supporting_document(db, doc_data, declaration_id)
    return RedirectResponse(url=f"/declarations/{declaration_id}", status_code=303)


@app.post("/declarations/{declaration_id}/generate_xml")
def generate_declaration_xml(declaration_id: int, db: Session = Depends(get_db)):
    from datetime import date
    from lxml import etree
    import io

    declaration = db.query(models.Declaration).get(declaration_id)
    if not declaration:
        raise HTTPException(status_code=404, detail="Declaration not found")

    goods_list = db.query(models.Goods).filter(models.Goods.declaration_id == declaration.id).all()
    supporting_docs = db.query(models.SupportingDocument).filter(models.SupportingDocument.declaration_id == declaration.id).all()

    root = etree.Element("AES515")

    # === ExportOperation ===
    export_op = etree.SubElement(root, "ExportOperation")
    etree.SubElement(export_op, "LRN").text = declaration.lrn
    etree.SubElement(export_op, "MRN").text = "24EE1210E0130048B0"
    etree.SubElement(export_op, "declarationType").text = "EX"
    etree.SubElement(export_op, "additionalDeclarationType").text = "A"
    etree.SubElement(export_op, "security").text = "2"
    etree.SubElement(export_op, "totalAmountInvoiced").text = str(declaration.total_amount_invoiced)
    etree.SubElement(export_op, "invoiceCurrency").text = declaration.invoice_currency
    etree.SubElement(export_op, "ndAgentNumber").text = "E2018/015"

    # === CustomsOfficeOfExport ===
    export_office = etree.SubElement(root, "CustomsOfficeOfExport")
    etree.SubElement(export_office, "referenceNumber").text = "EE1210EE"

    # === CustomsOfficeOfExitDeclared ===
    exit_office = etree.SubElement(root, "CustomsOfficeOfExitDeclared")
    etree.SubElement(exit_office, "referenceNumber").text = declaration.customs_office.code

    # === Exporter ===
    exporter = etree.SubElement(root, "Exporter")
    etree.SubElement(exporter, "identificationNumber").text = declaration.exporter.identification_number
    etree.SubElement(exporter, "name").text = declaration.exporter.name
    exporter_addr = etree.SubElement(exporter, "Address")
    etree.SubElement(exporter_addr, "streetAndNumber").text = declaration.exporter.street or ""
    etree.SubElement(exporter_addr, "postcode").text = declaration.exporter.postcode or ""
    etree.SubElement(exporter_addr, "city").text = declaration.exporter.city or ""
    etree.SubElement(exporter_addr, "country").text = declaration.exporter.country_code or "EE"

    # === Declarant ===
    declarant = etree.SubElement(root, "Declarant")
    etree.SubElement(declarant, "identificationNumber").text = "EE11436114"
    etree.SubElement(declarant, "name").text = "ALEKON CARGO OÜ"
    declarant_addr = etree.SubElement(declarant, "Address")
    etree.SubElement(declarant_addr, "streetAndNumber").text = "Saha-Loo põik 4"
    etree.SubElement(declarant_addr, "postcode").text = "74114"
    etree.SubElement(declarant_addr, "city").text = "Maardu"
    etree.SubElement(declarant_addr, "country").text = "EE"
    contact = etree.SubElement(declarant, "ContactPerson")
    etree.SubElement(contact, "phoneNumber").text = "6388989"
    etree.SubElement(contact, "eMailAddress").text = "ladu@alekon.ee"

    # === Representative ===
    representative = etree.SubElement(root, "Representative")
    etree.SubElement(representative, "identificationNumber").text = "EE11436114"
    etree.SubElement(representative, "status").text = "3"
    rep_contact = etree.SubElement(representative, "ContactPerson")
    etree.SubElement(rep_contact, "phoneNumber").text = "6388989"
    etree.SubElement(rep_contact, "eMailAddress").text = "ladu@alekon.ee"

    # === CurrencyExchange ===
    currency_exchange = etree.SubElement(root, "CurrencyExchange")
    etree.SubElement(currency_exchange, "internalCurrencyUnit").text = declaration.currency.code
    etree.SubElement(currency_exchange, "exchangeRate").text = "1"

    # === GoodsShipment ===
    shipment = etree.SubElement(root, "GoodsShipment")
    etree.SubElement(shipment, "natureOfTransaction").text = "11"
    etree.SubElement(shipment, "countryOfExport").text = "EE"
    etree.SubElement(shipment, "countryOfDestination").text = declaration.country_of_destination.code.upper()

    # === DeliveryTerms — должен идти до GoodsItem
    delivery = etree.SubElement(shipment, "DeliveryTerms")
    etree.SubElement(delivery, "incotermCode").text = declaration.incoterm.code
    etree.SubElement(delivery, "location").text = declaration.location or ""
    etree.SubElement(delivery, "country").text = declaration.country_of_destination.code

    # === Consignment
    consignment = etree.SubElement(shipment, "Consignment")
    etree.SubElement(consignment, "containerIndicator").text = str(declaration.container_indicator)
    etree.SubElement(consignment, "inlandModeOfTransport").text = declaration.inland_transport_mode.name[-1]
    etree.SubElement(consignment, "modeOfTransportAtTheBorder").text = declaration.border_transport_mode.name[-1]

    consignee = etree.SubElement(consignment, "Consignee")
    etree.SubElement(consignee, "name").text = declaration.consignee.name
    consignee_addr = etree.SubElement(consignee, "Address")
    addr_parts = (declaration.consignee.address or "").split(",")
    etree.SubElement(consignee_addr, "streetAndNumber").text = addr_parts[0] if len(addr_parts) > 0 else ""
    etree.SubElement(consignee_addr, "postcode").text = addr_parts[1] if len(addr_parts) > 1 else "-"
    etree.SubElement(consignee_addr, "city").text = addr_parts[2] if len(addr_parts) > 2 else ""
    etree.SubElement(consignee_addr, "country").text = declaration.country_of_destination.code

    location = etree.SubElement(consignment, "LocationOfGoods")
    etree.SubElement(location, "typeOfLocation").text = "D"
    etree.SubElement(location, "qualifierOfIdentification").text = "Z"
    location_addr = etree.SubElement(location, "Address")
    etree.SubElement(location_addr, "streetAndNumber").text = "Saha-Loo põik 4"
    etree.SubElement(location_addr, "postcode").text = "74114"
    etree.SubElement(location_addr, "city").text = "Maardu"
    etree.SubElement(location_addr, "country").text = "EE"

    # === GoodsItem (после DeliveryTerms)
    for idx, item in enumerate(goods_list, start=1):
        g = etree.SubElement(shipment, "GoodsItem")
        etree.SubElement(g, "declarationGoodsItemNumber").text = str(idx)
        etree.SubElement(g, "statisticalValue").text = "0"

        proc = etree.SubElement(g, "Procedure")
        etree.SubElement(proc, "requestedProcedure").text = "10"
        etree.SubElement(proc, "previousProcedure").text = "00"

        commodity = etree.SubElement(g, "Commodity")
        etree.SubElement(commodity, "descriptionOfGoods").text = item.harmonized_code.description or ""
        cc = etree.SubElement(commodity, "CommodityCode")
        etree.SubElement(cc, "harmonizedSystemSubHeadingCode").text = item.harmonized_code.code
        etree.SubElement(cc, "combinedNomenclatureCode").text = "00"

        gm = etree.SubElement(commodity, "GoodsMeasure")
        etree.SubElement(gm, "grossMass").text = str(item.gross_mass)
        etree.SubElement(gm, "netMass").text = str(item.net_mass)

        pkg = etree.SubElement(g, "Packaging")
        etree.SubElement(pkg, "sequenceNumber").text = "1"
        etree.SubElement(pkg, "typeOfPackages").text = item.package.type
        etree.SubElement(pkg, "numberOfPackages").text = str(item.number_of_packages)
        etree.SubElement(pkg, "shippingMarks").text = "-"

        for doc_idx, doc in enumerate(supporting_docs, start=1):
            sd = etree.SubElement(g, "SupportingDocument")
            etree.SubElement(sd, "sequenceNumber").text = str(doc_idx)
            etree.SubElement(sd, "type").text = doc.document.type
            etree.SubElement(sd, "referenceNumber").text = doc.reference_number
            etree.SubElement(sd, "validityDate").text = str(date.today())

        transport_doc = etree.SubElement(g, "TransportDocument")
        etree.SubElement(transport_doc, "sequenceNumber").text = "1"
        etree.SubElement(transport_doc, "type").text = "N730"
        etree.SubElement(transport_doc, "referenceNumber").text = "CMR"

    # === Output
    tree = etree.ElementTree(root)
    xml_bytes = io.BytesIO()
    tree.write(xml_bytes, xml_declaration=True, encoding="UTF-8", pretty_print=True)
    xml_bytes.seek(0)

    filename = f"declaration_{declaration.reference_number}.xml"
    return StreamingResponse(xml_bytes, media_type="application/xml", headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })



@app.post("/declarations/{declaration_id}/add_goods")
def add_goods(
    declaration_id: int,
    gross_mass: float = Form(...),
    net_mass: float = Form(...),
    number_of_packages: int = Form(...),
    harmonized_code_id: int = Form(...),
    package_id: int = Form(...),
    db: Session = Depends(get_db)
):
    harmonized_code = db.query(models.HarmonizedCode).get(harmonized_code_id)
    if not harmonized_code:
        raise HTTPException(status_code=404, detail="Harmonized code not found")

    goods_data = schemas.GoodsCreate(
        description=harmonized_code.description,
        gross_mass=gross_mass,
        net_mass=net_mass,
        number_of_packages=number_of_packages,
        harmonized_code_id=harmonized_code_id,
        package_id=package_id
    )
    crud.create_goods(db, goods_data, declaration_id)
    return RedirectResponse(url=f"/declarations/{declaration_id}", status_code=303)

@app.post("/goods/delete/{goods_id}")
def delete_goods(goods_id: int, db: Session = Depends(get_db)):
    goods = db.query(models.Goods).get(goods_id)
    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found")

    declaration_id = goods.declaration_id
    db.delete(goods)
    db.commit()
    return RedirectResponse(url=f"/declarations/{declaration_id}", status_code=303)

@app.post("/goods/update/{goods_id}")
def update_goods(
    goods_id: int,
    description: str = Form(...),
    gross_mass: float = Form(...),
    net_mass: float = Form(...),
    number_of_packages: int = Form(...),
    harmonized_code_id: int = Form(...),
    package_id: int = Form(...),
    db: Session = Depends(get_db)
):
    goods = db.query(models.Goods).filter(models.Goods.id == goods_id).first()
    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found")

    goods.description = description
    goods.gross_mass = gross_mass
    goods.net_mass = net_mass
    goods.number_of_packages = number_of_packages
    goods.harmonized_code_id = harmonized_code_id
    goods.package_id = package_id

    db.commit()

    return RedirectResponse(f"/declarations/{goods.eclaration_id}", status_code=303)


