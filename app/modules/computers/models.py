from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Computer(Base):
    __tablename__ = "computers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=True)
    serial_number = Column(String, unique=True, index=True, nullable=False)
    price = Column(Float, default=0.0)
    quantity = Column(Integer, default=0)
    status = Column(String, default="available")  # available, in_production, defect
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Qaysi user yaratganini bog'lash
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", backref="computers")

    # Qaysi bo'limda ishlab chiqarilgani (Foreign Key)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    # Aloqa (Relationship)
    department = relationship("Department", back_populates="computers")
