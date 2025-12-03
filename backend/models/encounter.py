from sqlalchemy import Column, Integer, String, ForeignKey, Date,DateTime
from sqlalchemy.orm import relationship 
from models import Base
from datetime import datetime


class Encounter(Base):
    __tablename__ = 'encounter'
    id = Column(Integer, primary_key = True, index = True)
    start_time = Column(DateTime,default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)
    
    medical_stuff_id = Column(Integer,ForeignKey("users.id"))
    medical_stuff = relationship("User", back_populates= 'encounters')#where user.role == doctor
   
    notes = relationship("Note", back_populates = 'encounter')