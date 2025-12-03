from models import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship 


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True)
    email = Column(String(220), unique = True, index = True)
    password = Column(String(255), nullable = False)
    role = Column(String(255), nullable = False)

    notes = relationship("Note", back_populates="author")
    encounters = relationship("Encounter", back_populates = "medical_stuff")
    patient = relationship("Patient", back_populates = "user",uselist = False)
