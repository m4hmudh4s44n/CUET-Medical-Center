# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True)
#     full_name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     phone_number = Column(String)
#     hashed_password = Column(String)


from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)

class Ambulance(Base):
    __tablename__ = "ambulances"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)
    driver = Column(String)
    phone = Column(String)
    status = Column(String)

class Medicine(Base):
    __tablename__ = "medicines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    company = Column(String)
    type = Column(String)
    quantity = Column(Integer)

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialty = Column(String)
    phone = Column(String)

class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    ex_id = Column(String) 
    name = Column(String)
    lead = Column(String)
    status = Column(String)