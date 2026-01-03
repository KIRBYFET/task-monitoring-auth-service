from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.deps import get_db
from app.db.crud_users import (
    list_users,
    get_user_by_id,
    create_user,
    set_user_active,
    set_user_role,
    get_user_by_email,
)
from app.schemas.user import UserOut, UserCreate, UserUpdateRole
from app.core.security import hash_password

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut], dependencies=[Depends(require_admin)])
def admin_list_users(db: Session = Depends(get_db)):
    return list_users(db)


@router.post("/users", response_model=UserOut, dependencies=[Depends(require_admin)])
def admin_create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if len(payload.password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="La contraseña supera 72 bytes (bcrypt).")

    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=409, detail="Email ya registrado")

    user = create_user(
        db,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        is_active=payload.is_active,
    )
    return user


@router.patch("/users/{user_id}/activate", response_model=UserOut, dependencies=[Depends(require_admin)])
def admin_activate_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return set_user_active(db, user, True)


@router.patch("/users/{user_id}/deactivate", response_model=UserOut, dependencies=[Depends(require_admin)])
def admin_deactivate_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return set_user_active(db, user, False)


@router.patch("/users/{user_id}/role", response_model=UserOut, dependencies=[Depends(require_admin)])
def admin_update_role(user_id: int, payload: UserUpdateRole, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if payload.role not in ("ADMIN", "USER"):
        raise HTTPException(status_code=400, detail="Rol inválido (ADMIN | USER)")

    return set_user_role(db, user, payload.role)
