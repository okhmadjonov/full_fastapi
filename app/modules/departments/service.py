from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.departments.repository import DepartmentRepository
from app.modules.departments.schemas import DepartmentCreate, DepartmentUpdate
from app.modules.departments.models import Department

class DepartmentService:
    @staticmethod
    def get_department(db: Session, department_id: int) -> Department:
        dept = DepartmentRepository.get_by_id(db, department_id)
        if not dept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bo'lim topilmadi"
            )
        return dept

    @staticmethod
    def create_department(db: Session, department_in: DepartmentCreate) -> Department:
        # Bo'lim nomi takrorlanmasligini tekshiramiz
        existing = DepartmentRepository.get_by_name(db, department_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ushbu nomli bo'lim allaqachon mavjud"
            )
        return DepartmentRepository.create(db, department_in)

    @staticmethod
    def update_department(db: Session, department_id: int, department_in: DepartmentUpdate) -> Department:
        db_dept = DepartmentService.get_department(db, department_id)
        
        # Agar nom yangilanyotgan bo'lsa va u boshqasida bo'lsa, xatolik beramiz
        if department_in.name and department_in.name != db_dept.name:
            existing = DepartmentRepository.get_by_name(db, department_in.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ushbu nomli bo'lim allaqachon mavjud"
                )
        
        return DepartmentRepository.update(db, db_dept, department_in)

    @staticmethod
    def delete_department(db: Session, department_id: int) -> None:
        db_dept = DepartmentService.get_department(db, department_id)
        DepartmentRepository.delete(db, db_dept)
