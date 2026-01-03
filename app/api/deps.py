from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.deps import get_db
from app.db.crud_users import get_user_by_email
from app.models.user import User
from app.core.enums import UserRole

# Bearer token (Swagger mostrará un solo campo "Bearer <token>")
security = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """
    Extrae el JWT desde: Authorization: Bearer <token>
    y devuelve el usuario autenticado.
    """
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        email: str | None = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, email=email)
    if not user or not user.is_active:
        raise credentials_exception

    return user


def require_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Requiere rol ADMIN.
    """
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Requiere rol ADMIN")
    return user
