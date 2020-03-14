"""
1. Веб-сервер принимает GET-запросы по адресу /albums/<artist> и выводит 
    на экран сообщение с количеством альбомов исполнителя artist 
    и списком названий этих альбомов.

2. Веб-сервер принимает POST-запросы по адресу /albums/ и сохраняет 
    переданные пользователем данные об альбоме. Данные передаются 
    в формате веб-формы. Если пользователь пытается передать данные 
    об альбоме, который уже есть в базе данных, обработчик запроса 
    отвечает HTTP-ошибкой 409 и выводит соответствующее сообщение.

http -f POST http://localhost:8080/albums artist="New Artist" 
    genre="Rock" album="Super"
Дополните список передаваемых параметров, если потребуется.

3. Набор полей в передаваемых данных полностью соответствует схеме 
    таблицы album базы данных.
4. В качестве исходной базы данных использовать файл albums.sqlite3.
5. До попытки сохранить переданные пользователем данные, нужно 
    провалидировать их. Проверить, например, что в поле "год выпуска" 
    передан действительно год.

Выложите код в репозиторий и приложите ссылку. Если считаете нужным, 
    оставьте комментарии о способах запуска и проверки кода. Если 
    в модулях есть сложные на ваш взгляд места, прокомментируйте их.
"""

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import json

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей 
        музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, 
        если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

"""
Поддержка GET-запроса
1. Веб-сервер принимает GET-запросы по адресу /albums/<artist> и выводит 
    на экран сообщение с количеством альбомов исполнителя artist 
    и списком названий этих альбомов.
"""

@route("/albums/<artist>")
def albums(artist):
    albums_list = find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        result = "Альбомов {} найдено: {}<br>".format(artist, 
            len(albums_list))
        album_names = [album.album for album in albums_list]
        result += "<h3>Список альбомов {}</h3>".format(artist)
        result += "<br>".join(album_names)
    return result


"""
Поддержка POST-запроса
2. Веб-сервер принимает POST-запросы по адресу /albums/ и сохраняет 
    переданные пользователем данные об альбоме. Данные передаются 
    в формате веб-формы. 

    Если пользователь пытается передать данные 
    об альбоме, который уже есть в базе данных, обработчик запроса 
    отвечает HTTP-ошибкой 409 и выводит соответствующее сообщение.

http -f POST http://localhost:8080/albums artist="New Artist" 
    genre="Rock" album="Super" year="1999"

3. Набор полей в передаваемых данных полностью соответствует схеме 
    таблицы album базы данных.
4. В качестве исходной базы данных использовать файл albums.sqlite3.
5. До попытки сохранить переданные пользователем данные, нужно 
    провалидировать их. Проверить, например, что в поле "год выпуска" 
    передан действительно год.
"""

class ExistedAlbum(Exception):
    pass

def save_user(user_data):
    """ сохраняет данные по новому альбому в sqlite
    """
    session = connect_db()
    
    existed_album = session.query(Album).filter(
        Album.album == user_data["album"], 
        Album.artist == user_data["artist"]
        ).first()
    if existed_album is not None:
        raise ExistedAlbum("Такой альбом уже есть в базе: {}".format(existed_album.id))

    new_album = Album(year=user_data["year"], artist=user_data["artist"], 
        genre=user_data["genre"], album=user_data["album"])

    session.add(new_album)
    session.commit()
    return


@route("/albums", method="POST")
def user():
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album = request.forms.get("album")
    year = request.forms.get("year")

    # проверка валидности данных и запись
    try:
        year = int(year)
        user_data = {
            "artist": artist,
            "genre": genre,
            "album": album,
            "year": year
        }
        save_user(user_data)

    except ValueError as err:
        result = HTTPError(400, "Некорректные данные в поле 'год'")
    except ExistedAlbum as err:
        result = HTTPError(409, str(err))
    else:
        result = "Альбом внесен в базу данных"

    return result
    

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)


