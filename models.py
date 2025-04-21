from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    items = relationship("WebBlockItem", back_populates="owner")

class WebBlockItem(Base):
    __tablename__ = "webblockitems"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    link = Column(String)
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")