# pip install fastapi uvicorn sqlalchemy databases bcrypt


from pydantic import BaseModel

class UserCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class AmbulanceBase(BaseModel):
    number: str
    driver: str
    phone: str
    status: str


class AmbulanceCreate(AmbulanceBase):
    pass

class AmbulanceOut(AmbulanceBase):
    id: int
    class Config:
        orm_mode = True

class MedicineBase(BaseModel):
    name: str
    company: str
    type: str
    quantity: int

class MedicineCreate(MedicineBase):
    pass

class MedicineOut(MedicineBase):
    id: int
    class Config:
        orm_mode = True

class DoctorBase(BaseModel):
    name: str
    specialty: str
    phone: str

class DoctorCreate(DoctorBase):
    pass

class DoctorOut(DoctorBase):
    id: int
    class Config:
        orm_mode = True

class ExperimentBase(BaseModel):
    ex_id: str
    name: str
    lead: str
    status: str

class ExperimentCreate(ExperimentBase):
    pass

class ExperimentOut(ExperimentBase):
    id: int
    class Config:
        orm_mode = True