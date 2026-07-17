from fastapi import FastAPI
from app.api_router import api_router
from app.core.database import SessionLocal
from app.modules.users.service import UserService

app = FastAPI(
    title="Manufacturing Company API",
    description="Texnik qurilmalar, kompyuter qismlari va boshqa jihozlar ishlab chiqaruvchi firma uchun API",
    version="1.0.0"
)

# Barcha API endpointlarni ulash
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Manufacturing API ishlamoqda!"}

# Dastur ishga tushganda default foydalanuvchilarni yaratish (Seeder)
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        UserService.seed_users(db)
    finally:
        db.close()
