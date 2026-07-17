from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.modules.auth.service import get_current_user, RoleChecker
from app.modules.users.models import User
from app.modules.computers.schemas import ComputerCreate, ComputerUpdate, ComputerOut
from app.modules.computers.service import ComputerService

router = APIRouter(prefix="/computers", tags=["Computers"])

# 1. Hamma kompyuterlarni olish (Barcha rollar ko'ra oladi)
@router.get("/", response_model=List[ComputerOut])
def read_computers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.modules.computers.repository import ComputerRepository
    return ComputerRepository.get_all(db, skip=skip, limit=limit)

# 2. Bitta kompyuterni ID orqali olish (Barcha rollar ko'ra oladi)
@router.get("/{computer_id}", response_model=ComputerOut)
def read_computer(
    computer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ComputerService.get_computer(db, computer_id)

# 3. Yangi kompyuter yaratish (Faqat director, deputy, manager)
@router.post("/", response_model=ComputerOut, status_code=status.HTTP_201_CREATED)
def create_computer(
    computer_in: ComputerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["director", "deputy", "manager"]))
):
    return ComputerService.create_computer(db, computer_in, created_by_id=current_user.id)

# 4. Kompyuter ma'lumotlarini o'zgartirish (Director, deputy, manager, operator)
@router.put("/{computer_id}", response_model=ComputerOut)
def update_computer(
    computer_id: int,
    computer_in: ComputerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["director", "deputy", "manager", "operator"]))
):
    return ComputerService.update_computer(db, computer_id, computer_in)

# 5. Kompyuterni o'chirish (Faqat director, deputy)
@router.delete("/{computer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_computer(
    computer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["director", "deputy"]))
):
    ComputerService.delete_computer(db, computer_id)
    return None
