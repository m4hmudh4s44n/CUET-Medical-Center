from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas
from .auth import hash_password, verify_password
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from starlette.middleware.sessions import SessionMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="our-secret-key")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        return RedirectResponse(url="/signup.html?error=exists", status_code=303)
    
    new_user = models.User(
        full_name=full_name,
        email=email,
        phone=phone,
        password=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login.html", status_code=303)


@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and verify_password(password, user.password):
        request.session["user_email"] = user.email
        return RedirectResponse(url="/index.html", status_code=303)

    # return RedirectResponse(url="/login.html?error=invalid", status_code=303)
    return {"error": "Invalid email or password"}



@app.get("/ambulances", response_model=list[schemas.AmbulanceOut])
def get_ambulances(db: Session = Depends(get_db)):
    return db.query(models.Ambulance).all()


@app.post("/ambulances/", response_model=schemas.AmbulanceOut)   
def create_ambulance(
    number: str = Form(...),
    driver: str = Form(...),
    phone: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    db_ambulance = models.Ambulance(
        number=number,
        driver=driver,
        phone=phone,
        status=status
    )
    db.add(db_ambulance)
    db.commit()
    db.refresh(db_ambulance)
    return RedirectResponse(url="/admin_panel.html", status_code=303)


    
@app.delete("/ambulances/{ambulance_id}")
def delete_ambulance(ambulance_id: int, db: Session = Depends(get_db)):
    db_ambulance = db.query(models.Ambulance).filter(models.Ambulance.id == ambulance_id).first()
    if not db_ambulance:
        raise HTTPException(status_code=404, detail="Ambulance not found")
    db.delete(db_ambulance)
    db.commit()
    return {"ok": True}


@app.post("/ambulances/{ambulance_id}/", response_model=schemas.AmbulanceOut)
def update_ambulance(
    ambulance_id: int,
    number: str = Form(...),
    driver: str = Form(...),
    phone: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    db_ambulance = db.query(models.Ambulance).filter(models.Ambulance.id == ambulance_id).first()
    if not db_ambulance:
        raise HTTPException(status_code=404, detail="Ambulance not found")
    
    db_ambulance.number = number
    db_ambulance.driver = driver
    db_ambulance.phone = phone
    db_ambulance.status = status
    db.commit()
    db.refresh(db_ambulance)
    
    return RedirectResponse(url="/admin_panel.html", status_code=303)

@app.get("/medicines", response_model=list[schemas.MedicineOut])
def get_medicines(db: Session = Depends(get_db)):
    return db.query(models.Medicine).all()


@app.post("/medicines/", response_model=schemas.MedicineOut)
def create_medicine(
    name: str = Form(...),
    company: str = Form(...),
    type: str = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    db_medicine = models.Medicine(
        name=name,
        company=company,
        type=type,
        quantity=quantity
    )
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return RedirectResponse(url="/admin_panel.html", status_code=303)


@app.get("/doctors", response_model=list[schemas.DoctorOut])
def get_doctors(db: Session = Depends(get_db)):
    return db.query(models.Doctor).all()

@app.post("/doctors/", response_model=schemas.DoctorOut)
def create_doctor(
    name: str = Form(...),
    specialty: str = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db)
):
    db_doctor = models.Doctor(
        name=name,
        specialty=specialty,
        phone=phone
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return RedirectResponse(url="/admin_panel.html", status_code=303)

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(db_doctor)
    db.commit()
    return {"ok": True}


@app.get("/experiments", response_model=list[schemas.ExperimentOut])
def get_experiments(db: Session = Depends(get_db)):
    return db.query(models.Experiment).all()

@app.post("/experiments/", response_model=schemas.ExperimentOut)
def create_experiment(
    ex_id: str = Form(...),
    name: str = Form(...),
    lead: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    db_experiment = models.Experiment(
        ex_id=ex_id,
        name=name,
        lead=lead,
        status=status
    )
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return RedirectResponse(url="/admin_panel.html", status_code=303)

@app.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, db: Session = Depends(get_db)):
    db_experiment = db.query(models.Experiment).filter(models.Experiment.id == experiment_id).first()
    if not db_experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    db.delete(db_experiment)
    db.commit()
    return {"ok": True}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")