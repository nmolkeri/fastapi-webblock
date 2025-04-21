from pydantic import BaseModel

class WebBlockItemBase(BaseModel):
    name: str
    link: str

class WebBlockItemCreate(WebBlockItemBase):
    pass

class WebBlockItemUpdate(WebBlockItemBase):
    pass

class WebBlockItemResponse(WebBlockItemBase):
    id: str

    model_config = {
        "from_attributes": True
    }

class User(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str

    model_config = {
        "from_attributes": True
    }