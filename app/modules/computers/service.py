from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.computers.repository import ComputerRepository
from app.modules.computers.schemas import ComputerCreate, ComputerUpdate
from app.modules.computers.models import Computer

class ComputerService:
    @staticmethod
    def get_computer(db: Session, computer_id: int) -> Computer:
        computer = ComputerRepository.get_by_id(db, computer_id)
        if not computer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kompyuter topilmadi"
            )
        return computer

    @staticmethod
    def create_computer(db: Session, computer_in: ComputerCreate, created_by_id: int) -> Computer:
        # Serial number takrorlanmasligini tekshiramiz
        existing = ComputerRepository.get_by_serial_number(db, computer_in.serial_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ushbu seriya raqamiga ega kompyuter allaqachon kiritilgan"
            )
        return ComputerRepository.create(db, computer_in, created_by_id)

    @staticmethod
    def update_computer(db: Session, computer_id: int, computer_in: ComputerUpdate) -> Computer:
        db_computer = ComputerService.get_computer(db, computer_id)
        
        # Agar seriya raqami yangilanyotgan bo'lsa va u boshqasida bo'lsa, xatolik beramiz
        if computer_in.serial_number and computer_in.serial_number != db_computer.serial_number:
            existing = ComputerRepository.get_by_serial_number(db, computer_in.serial_number)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ushbu seriya raqami band"
                )
        
        return ComputerRepository.update(db, db_computer, computer_in)

    @staticmethod
    def delete_computer(db: Session, computer_id: int) -> None:
        db_computer = ComputerService.get_computer(db, computer_id)
        ComputerRepository.delete(db, db_computer)
