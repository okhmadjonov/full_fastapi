from sqlalchemy.orm import Session
from app.modules.computers.models import Computer
from app.modules.computers.schemas import ComputerCreate, ComputerUpdate

class ComputerRepository:
    @staticmethod
    def get_by_id(db: Session, computer_id: int) -> Computer:
        return db.query(Computer).filter(Computer.id == computer_id).first()

    @staticmethod
    def get_by_serial_number(db: Session, serial_number: str) -> Computer:
        return db.query(Computer).filter(Computer.serial_number == serial_number).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Computer).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, computer_in: ComputerCreate, created_by_id: int) -> Computer:
        db_computer = Computer(
            name=computer_in.name,
            brand=computer_in.brand,
            model=computer_in.model,
            serial_number=computer_in.serial_number,
            price=computer_in.price,
            quantity=computer_in.quantity,
            status=computer_in.status,
            created_by_id=created_by_id
        )
        db.add(db_computer)
        db.commit()
        db.refresh(db_computer)
        return db_computer

    @staticmethod
    def update(db: Session, db_computer: Computer, computer_in: ComputerUpdate) -> Computer:
        update_data = computer_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_computer, key, value)
        db.commit()
        db.refresh(db_computer)
        return db_computer

    @staticmethod
    def delete(db: Session, db_computer: Computer) -> None:
        db.delete(db_computer)
        db.commit()
