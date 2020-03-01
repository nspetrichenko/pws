"""
Задание 1
Напишите модуль users.py, который регистрирует новых пользователей. 

Скрипт должен запрашивать следующие данные:
- имя
- фамилию
- пол
- адрес электронной почты
- дату рождения
- рост

Все данные о пользователях сохраните в таблице user 
нашей базы данных sochi_athletes.sqlite3.
"""
import uuid
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.String(36), primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_data():
    print("Пишу данные")
    user_id = str(uuid.uuid4())
    first_name = input("Имя: ")
    last_name = input("Фамилия: ")
    gender = input("Пол (Male/Female): ")
    email = input("email: ")    
    birthdate = input("Дата рождения (ГГГГ-ММ-ДД): ")
    height = input("Рост: ")
    user = User(
        id=user_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user

def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Данные сохранены в БД")


if __name__ == "__main__":
    main()
