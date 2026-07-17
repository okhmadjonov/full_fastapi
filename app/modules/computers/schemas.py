from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ComputerBase(BaseModel):
    name: str
    brand: str
    model: Optional[str] = None
    serial_number: str
    price: float = 0.0
    quantity: int = 0
    status: str = "available"  # available, in_production, defect

class ComputerCreate(ComputerBase):
    pass

class ComputerUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    status: Optional[str] = None

class ComputerOut(ComputerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_id: int

    class Config:
        from_attributes = True
