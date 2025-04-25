from sqlalchemy.orm import Session
import models, schemas

def get_user_by_srn(db: Session, srn: str):
    return db.query(models.User).filter(models.User.srn == srn).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, srn: str, password: str):
    user = get_user_by_srn(db, srn)
    if user and user.password == password:
        return user
    return None

def update_user(db: Session, srn: str, update_data: schemas.UserUpdate):
    user = get_user_by_srn(db, srn)
    if not user:
        return None
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(models.User).all()
