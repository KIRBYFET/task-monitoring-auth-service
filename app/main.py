from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.models.base import Base

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.admin import router as admin_router

from app.db.crud_users import get_user_by_email, create_user
from app.core.security import hash_password


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0"
)

# Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)


# Health
@app.get("/health")
def health():
    return {"status": "ok"}


# Startup: crear tablas + seed admin
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        admin_email = "admin@example.com"
        admin_password = "admin123"

        existing = get_user_by_email(db, admin_email)
        if not existing:
            create_user(
                db=db,
                email=admin_email,
                hashed_password=hash_password(admin_password),
                role="ADMIN",
            )
    finally:
        db.close()