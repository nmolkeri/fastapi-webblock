from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import WebBlockItemCreate, WebBlockItemUpdate, WebBlockItemResponse, UserCreate, UserResponse
from models import User
from database import SessionLocal, init_db
from auth import authenticate_user, create_access_token, get_current_user, oauth2_scheme
import crud
from database import get_db
from datetime import timedelta

app = FastAPI()

# Run DB init
init_db()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "FastAPI is working!"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db, user.username, user.password)

@app.get("/items", response_model=list[WebBlockItemResponse])
def read_items(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_all_items(db)

@app.post("/items", response_model=WebBlockItemResponse)
def create_item(item: WebBlockItemCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_item = crud.create_item(db, item, user)
    return db_item

@app.put("/items/{item_id}", response_model=WebBlockItemResponse)
def update_item(item_id: str, item: WebBlockItemUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), user=Depends(get_current_user)):
    updated = crud.update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@app.delete("/items/{item_id}")
def delete_item(item_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), user=Depends(get_current_user)):
    success = crud.delete_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"deleted": True}