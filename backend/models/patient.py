from models import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship 


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key = True, unique = True, index = True)
    name = Column(String(255), index = True)
    date_of_birth = Column(Date, nullable = False)
    sex = Column(String(1))
    contact_info = Column(String(255))

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates='patient',uselist = False)

    visits = relationship("Visit", back_populates = 'patient')



