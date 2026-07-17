from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.modules.auth.service import get_current_user, RoleChecker
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserUpdate, UserOut
from app.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

# 1. Hamma foydalanuvchilarni olish (Faqat rahbarlar ko'ra oladi)
@router.get("/", response_model=List[UserOut])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["director", "deputy", "manager"]))
):
    from app.modules.users.repository import UserRepository
    return UserRepository.get_all(db, skip=skip, limit=limit)

# 2. O'zining profilini ko'rish (Hamma kira oladi)
@router.get("/me", response_model=UserOut)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

# 3. Yangi user qo'shish (Faqat director va deputy)
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["director", "deputy"]))
):
    return UserService.create_user(db, user_in)

# 4. User ma'lumotlarini o'zgartirish (Faqat director va deputy)
@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["director", "deputy"]))
):
    return UserService.update_user(db, user_id, user_in)

# 5. Userni o'chirish (Faqat director)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["director"]))
):
    UserService.delete_user(db, user_id)
    return None
