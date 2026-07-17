from fastapi import APIRouter
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.computers.router import router as computers_router
from app.modules.departments.router import router as departments_router  # yangi import

api_router = APIRouter()

# Routerlarni birlashtiramiz
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(computers_router)
api_router.include_router(departments_router)  # yangi router
