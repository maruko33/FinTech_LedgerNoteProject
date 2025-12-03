from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship 
from models import Base

class Visit(Base):
    __tablename__ = 'visit'
    id = Column(Integer, primary_key = True, index = True)
    date = Column(Date, nullable = False)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    patient = relationship("Patient", back_populates = 'visits', uselist = False)


