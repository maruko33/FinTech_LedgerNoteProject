from models import Base
from sqlalchemy import Integer, String, Column, Text, ForeignKey, Date
from sqlalchemy.orm import relationship 

class Note(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key = True, index = True)
    date = Column(Date, nullable = False)
    
    encounter_id = Column(Integer, ForeignKey("encounter.id"))
    encounter = relationship("Encounter",back_populates = 'notes')

    author_id = Column(Integer,ForeignKey("users.id"))
    author= relationship("User", back_populates = "notes")