from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm  # yangi import
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt, JWTError

from app.core.database import get_db
from app.core.config import settings
from app.modules.users.repository import UserRepository
from app.modules.auth.schemas import Token, TokenPayload
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(
    login_data: OAuth2PasswordRequestForm = Depends(),  # OAuth2PasswordRequestForm ga o'zgartirdik
    db: Session = Depends(get_db)
):
    # Foydalanuvchini bazadan qidiramiz (username orqali)
    user = UserRepository.get_by_username(db, login_data.username)
    
    # Agar username topilmasa, email orqali ham qidirib ko'ramiz
    if not user:
        user = UserRepository.get_by_email(db, login_data.username)

    if not user or not AuthService.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Foydalanuvchi nomi yoki parol xato"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Foydalanuvchi faol emas"
        )

    # Tokenlarni yaratamiz
    access_token = AuthService.create_access_token(subject=user.username, role=user.role)
    refresh_token = AuthService.create_refresh_token(subject=user.username, role=user.role)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token_str: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token yaroqsiz",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token_str, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        if username is None or token_type != "refresh":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = UserRepository.get_by_username(db, username)
    if not user or not user.is_active:
        raise credentials_exception

    new_access_token = AuthService.create_access_token(subject=user.username, role=user.role)
    new_refresh_token = AuthService.create_refresh_token(subject=user.username, role=user.role)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
