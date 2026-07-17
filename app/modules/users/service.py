from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserUpdate
from app.modules.users.models import User
from app.modules.auth.service import AuthService

class UserService:
    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
        return user

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        if UserRepository.get_by_username(db, user_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ushbu foydalanuvchi nomi band"
            )
        if UserRepository.get_by_email(db, user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ushbu email manzili band"
            )
        return UserRepository.create(db, user_in)

    @staticmethod
    def update_user(db: Session, user_id: int, user_in: UserUpdate) -> User:
        db_user = UserService.get_user(db, user_id)
        return UserRepository.update(db, db_user, user_in)

    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        db_user = UserService.get_user(db, user_id)
        UserRepository.delete(db, db_user)

    @staticmethod
    def seed_users(db: Session):
        director_exists = db.query(User).filter(User.role == "director").first()
        if not director_exists:
            # 1. Director yaratish
            UserRepository.create(db, UserCreate(
                username="director_admin",
                email="director@company.com",
                password="DirectorPassword123!",
                role="director"
            ))
            
            # 2. Deputy (O'rinbosar) yaratish
            UserRepository.create(db, UserCreate(
                username="deputy_admin",
                email="deputy@company.com",
                password="DeputyPassword123!",
                role="deputy"
            ))

            # 3. Manager (Bo'lim boshlig'i) yaratish
            UserRepository.create(db, UserCreate(
                username="manager_user",
                email="manager@company.com",
                password="ManagerPassword123!",
                role="manager"
            ))

            # 4. Operator yaratish
            UserRepository.create(db, UserCreate(
                username="operator_user",
                email="operator@company.com",
                password="OperatorPassword123!",
                role="operator"
            ))

            # 5. Worker (Ishchi) yaratish
            UserRepository.create(db, UserCreate(
                username="worker_user",
                email="worker@company.com",
                password="WorkerPassword123!",
                role="worker"
            ))
            print("Default foydalanuvchilar (seed) muvaffaqiyatli yaratildi!")
