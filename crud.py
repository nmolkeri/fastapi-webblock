from sqlalchemy.orm import Session
from models import WebBlockItem
from schemas import WebBlockItemCreate, WebBlockItemUpdate
from models import User
from passlib.context import CryptContext
import models  # ✅ Add this line
from models import WebBlockItem, User

def get_all_items(db: Session):
    return db.query(WebBlockItem).all()

def get_item(db: Session, item_id: str):
    return db.query(WebBlockItem).filter(WebBlockItem.id == item_id).first()

def create_item(db: Session, item: WebBlockItemCreate, user: User):
    db_item = WebBlockItem(**item.dict(), owner_id=user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: str, item: WebBlockItemUpdate):
    db_item = get_item(db, item_id)
    if db_item:
        db_item.name = item.name
        db_item.link = item.link
        db.commit()
        return db_item
    return None

def delete_item(db: Session, item_id: str):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()