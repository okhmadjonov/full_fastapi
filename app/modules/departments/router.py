from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.modules.auth.service import get_current_user, RoleChecker
from app.modules.users.models import User
from app.modules.departments.schemas import DepartmentCreate, DepartmentUpdate, DepartmentOut, DepartmentDetailOut
from app.modules.departments.service import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departments"])

# 1. Hamma bo'limlarni olish (Barcha kirgan foydalanuvchilar ko'ra oladi)
@router.get("/", response_model=List[DepartmentOut])
def read_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.modules.departments.repository import DepartmentRepository
    return DepartmentRepository.get_all(db, skip=skip, limit=limit)

# 2. Bitta bo'limni barcha xodimlari va mahsulotlari (kompyuterlari) bilan birga olish
@router.get("/{department_id}", response_model=DepartmentDetailOut)
def read_department_detail(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DepartmentService.get_department(db, department_id)

# 3. Yangi bo'lim yaratish (Faqat director va deputy)
@router.post("/", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(
    department_in: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["director", "deputy"]))
):
    return DepartmentService.create_department(db, department_in)

# 4. Bo'lim ma'lumotlarini o'zgartirish (Faqat director va deputy)
@router.put("/{department_id}", response_model=DepartmentOut)
def update_department(
    department_id: int,
    department_in: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["director", "deputy"]))
):
    return DepartmentService.update_department(db, department_id, department_in)

# 5. Bo'limni o'chirish (Faqat eng katta rahbar - director)
@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["director"]))
):
    DepartmentService.delete_department(db, department_id)
    return None
