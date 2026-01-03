from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id.asc()).all()

def create_user(db: Session, email: str, hashed_password: str, role: str = "USER", is_active: bool = True) -> User:
    user = User(email=email, hashed_password=hashed_password, role=role, is_active=is_active)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def set_user_active(db: Session, user: User, is_active: bool) -> User:
    user.is_active = is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def set_user_role(db: Session, user: User, role: str) -> User:
    user.role = role
    db.add(user)
    db.commit()
    db.refresh(user)
    return user