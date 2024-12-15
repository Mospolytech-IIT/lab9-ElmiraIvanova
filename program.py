from db_config import SessionLocal
from db_models import User, Post
from sqlalchemy.exc import SQLAlchemyError

def add_users():
    """Добавление пользователей"""
    session = SessionLocal()
    try:
        users = [
            User(username="elmira", email="elmira@mail.com", password="12345Elmira."),
            User(username="kate", email="kate@mail.com", password="12345Kate."),
            User(username="alyona", email="alyona@email.com", password="12345Alyona."),
        ]
        session.add_all(users)  
        session.commit()
        print("Пользователи успешно добавлены добавлены")
    except SQLAlchemyError as e:
        session.rollback()
        print(e)
    finally:
        session.close()


def add_posts():
    """Добавление постов"""
    session = SessionLocal()
    try:
        user1 = session.query(User).filter_by(username="elmira").first()
        user2 = session.query(User).filter_by(username="kate").first()
        user3 = session.query(User).filter_by(username="alyona").first()

        posts = [
            Post(title="Пост 1", content=f"Это пост пользователя {user1.username}", user_id=user1.id),
            Post(title="Пост 2", content=f"Это пост пользователя {user2.username}", user_id=user2.id),
            Post(title="Пост 3", content=f"Это пост пользователя {user3.username}", user_id=user3.id),
        ]
        session.add_all(posts)
        session.commit()
        print("Посты добавлены")
    except SQLAlchemyError as e:
        session.rollback()
        print(e)
    finally:
        session.close()

def get_users():
    """Извлечение пользователей"""
    session = SessionLocal()
    try:
        users = session.query(User).all()
        for user in users:
            print(f"ID: {user.id}, username: {user.username}, email: {user.email}")
    finally:
        session.close()

def get_posts():
    """Изавлечение постов, с информацией о пользователях"""
    session = SessionLocal()
    try:
        posts = session.query(Post).all()
        for post in posts:
            print(f"Post ID: {post.id}, Title: {post.title}, Content: {post.content}, Author: {post.user.username}")
    finally:
        session.close()

def get_posts_by_user(username: str):
    """Извлечение постов определенного пользователя"""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            print("Пользователь не найден.")
            return
        posts = session.query(Post).filter_by(user_id=user.id).all()
        for post in posts:
            print(f"Post ID: {post.id}, Title: {post.title}, Content: {post.content}")
    finally:
        session.close()

def update_email(username: str, new_email: str):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user:
            user.email = new_email
            session.commit()
            print(f"Email пользователя '{username}' обновлён на '{new_email}'.")
        else:
            print(f"Пользователь с именем '{username}' не найден.")
    except SQLAlchemyError as e:
        session.rollback()
        print(e)
    finally:
        session.close()
    
def update_content(post_id: int, new_content: str):
    session = SessionLocal()
    try:
        post = session.query(Post).filter_by(id=post_id).first()
        if post:
            post.content = new_content
            session.commit()
            print(f"Содержимое поста {post_id} успешно обновлено.")
        else:
            print(f"Пост не найден.")
    except SQLAlchemyError as e:
        session.rollback()
        print(e)
    finally:
        session.close()

def delete_post(post_id: int):
    session = SessionLocal()
    try:
        post = session.query(Post).filter_by(id=post_id).first()
        if post:
            session.delete(post)
            session.commit()
            print(f"Пост с ID {post_id} успешно удалён.")
        else:
            print(f"Пост с ID {post_id} не найден.")
    except SQLAlchemyError as e:
        session.rollback()
        print(e)
    finally:
        session.close()

def delete_user_with_posts(username: str):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user:
            session.query(Post).filter_by(user_id=user.id).delete()
            session.delete(user)
            session.commit()
            print(f"Пользователь '{username}' и его посты удалены.")
        else:
            print(f"Пользователь с именем '{username}' не найден.")
    except SQLAlchemyError as e:
        session.rollback()
        print(e)
    finally:
        session.close()

if __name__ == "__main__":
  # add_users()
  # add_posts()
  # get_users()
  # username = input("Введите имя пользователя: ")
  # get_posts_by_user(username)

    update_email("elmira", "new_elmira@mail.com")
    update_content(1, "Обновлённое содержимое поста.")
    delete_post(2)
    delete_user_with_posts("alyona")