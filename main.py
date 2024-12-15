from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db_config import SessionLocal, engine
from db_models import Base, User, Post
from models import PostCreate, PostUpdate, UserCreate

# Инициализация приложения и базы данных
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    """Получение списка всех пользователей"""
    users = db.query(User).all()
    return [{"id": user.id, "username": user.username, "email": user.email} for user in users]


@app.post("/users/create")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создание нового пользователя"""
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

@app.put("/users/update/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """Обновление информации о пользователе"""
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_user.username = user.username
    existing_user.email = user.email
    existing_user.password = user.password
    db.commit()
    db.refresh(existing_user)
    return {"id": existing_user.id, "username": existing_user.username, "email": existing_user.email}

@app.delete("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удаление пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} deleted"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    """Получение списка всех постов"""
    posts = db.query(Post).all()
    return posts

@app.post("/posts/create")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """Создание нового поста"""
    new_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"id": new_post.id, "title": new_post.title, "content": new_post.content, "user_id": new_post.user_id}

@app.put("/posts/update/{post_id}")
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    """Обновление информации о посте"""
    existing_post = db.query(Post).filter(Post.id == post_id).first()
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    existing_post.title = post.title
    existing_post.content = post.content
    db.commit()
    db.refresh(existing_post)
    return {"id": existing_post.id, "title": existing_post.title, "content": existing_post.content, "user_id": existing_post.user_id}

@app.delete("/posts/delete/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Удаление поста"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": f"Post with ID {post_id} deleted"}
