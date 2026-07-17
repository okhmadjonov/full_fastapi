from sqlalchemy.orm import Session
from app.modules.departments.models import Department
from app.modules.departments.schemas import DepartmentCreate, DepartmentUpdate

class DepartmentRepository:
    @staticmethod
    def get_by_id(db: Session, department_id: int) -> Department:
        return db.query(Department).filter(Department.id == department_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Department:
        return db.query(Department).filter(Department.name == name).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Department).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, department_in: DepartmentCreate) -> Department:
        db_dept = Department(
            name=department_in.name,
            description=department_in.description
        )
        db.add(db_dept)
        db.commit()
        db.refresh(db_dept)
        return db_dept

    @staticmethod
    def update(db: Session, db_dept: Department, department_in: DepartmentUpdate) -> Department:
        update_data = department_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_dept, key, value)
        db.commit()
        db.refresh(db_dept)
        return db_dept

    @staticmethod
    def delete(db: Session, db_dept: Department) -> None:
        db.delete(db_dept)
        db.commit()
