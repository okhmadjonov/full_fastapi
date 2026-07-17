from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class DepartmentOut(DepartmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Agar bo'lim haqidagi to'liq ma'lumotni unga tegishli bo'lgan xodimlar va 
# kompyuterlar ro'yxati bilan birga olmoqchi bo'lsak, quyidagi sxemadan foydalanamiz:
from app.modules.users.schemas import UserOut
from app.modules.computers.schemas import ComputerOut

class DepartmentDetailOut(DepartmentOut):
    users: List[UserOut] = []
    computers: List[ComputerOut] = []

    class Config:
        from_attributes = True
