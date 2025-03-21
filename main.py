from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
import crud, models
from pydantic import BaseModel

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Схемы Pydantic для валидации входных данных
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserEmailUpdate(BaseModel):
    new_email: str

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

class PostContentUpdate(BaseModel):
    new_content: str

# Получение всех пользователей
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

# Получение конкретного пользователя
@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Добавление нового пользователя
@app.post("/users/")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.username, user.email, user.password)

# Получение всех постов
@app.get("/posts/")
def read_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

# Получение постов конкретного пользователя
@app.get("/posts/{user_id}")
def read_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_posts_by_user(db, user_id)

# Добавление нового поста
@app.post("/posts/")
def add_post(post: PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post.title, post.content, post.user_id)

# Обновление email пользователя
@app.put("/users/{user_id}/email")
def update_user_email(user_id: int, email_update: UserEmailUpdate, db: Session = Depends(get_db)):
    return crud.update_user_email(db, user_id, email_update.new_email)

# Обновление контента поста
@app.put("/posts/{post_id}/content")
def update_post_content(post_id: int, content_update: PostContentUpdate, db: Session = Depends(get_db)):
    return crud.update_post_content(db, post_id, content_update.new_content)

# Удаление поста
@app.delete("/posts/{post_id}")
def remove_post(post_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(db, post_id)

# Удаление пользователя и всех его постов
@app.delete("/users/{user_id}")
def remove_user_and_posts(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user_and_posts(db, user_id)

# Запуск FastAPI-сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
