from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int
    
class PostUpdate(BaseModel):
    title: str
    content: str