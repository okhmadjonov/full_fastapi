from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey  # ForeignKey qo'shildi
from sqlalchemy.orm import relationship  # relationship qo'shildi
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="worker", nullable=False)  # director, deputy, manager, operator, worker
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Department bilan bog'lash (Foreign Key)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    # Aloqa (Relationship)
    department = relationship("Department", back_populates="users")
