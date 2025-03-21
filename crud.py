from sqlalchemy.orm import Session
from models import User, Post

# Добавление нового пользователя
def create_user(db: Session, username: str, email: str, password: str):
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Получение всех пользователей
def get_users(db: Session):
    return db.query(User).all()

# Получение конкретного пользователя
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Добавление поста
def create_post(db: Session, title: str, content: str, user_id: int):
    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# Получение всех постов
def get_posts(db: Session):
    return db.query(Post).all()

# Получение постов конкретного пользователя
def get_posts_by_user(db: Session, user_id: int):
    return db.query(Post).filter(Post.user_id == user_id).all()

# Обновление email пользователя
def update_user_email(db: Session, user_id: int, new_email: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        db.commit()
    return user

# Обновление контента поста
def update_post_content(db: Session, post_id: int, new_content: str):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        db.commit()
    return post

# Удаление поста
def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
    return post

# Удаление пользователя и всех его постов
def delete_user_and_posts(db: Session, user_id: int):
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    for post in posts:
        db.delete(post)
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
