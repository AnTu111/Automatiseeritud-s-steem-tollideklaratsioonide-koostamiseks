from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal

app = FastAPI()

# ���������� Jinja2
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ������� ��������
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# �������� �� ��������
@app.get("/countries", response_class=HTMLResponse)
def country_list(request: Request, db: Session = Depends(get_db)):
    countries = crud.get_countries(db)
    return templates.TemplateResponse("countries.html", {"request": request, "countries": countries})

# ����� ���������� ������
@app.post("/countries/add")
def add_country(name: str = Form(...), code: str = Form(...), db: Session = Depends(get_db)):
    crud.create_country(db, schemas.CountryCreate(name=name, code=code))
    return RedirectResponse(url="/countries", status_code=303)

# �������� � ������������
@app.get("/consignees", response_class=HTMLResponse)
def consignee_list(request: Request, db: Session = Depends(get_db)):
    consignees = crud.get_consignees(db)
    return templates.TemplateResponse("consignees.html", {"request": request, "consignees": consignees})

# ����� ���������� ����������
@app.post("/consignees/add")
def add_consignee(name: str = Form(...), address: str = Form(...), db: Session = Depends(get_db)):
    consignee = schemas.ConsigneeCreate(name=name, address=address)
    crud.create_consignee(db, consignee)
    return RedirectResponse(url="/consignees", status_code=303)
