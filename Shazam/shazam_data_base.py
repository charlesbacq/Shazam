import peewee as pw
import shazamage as sh
import ast

db = pw.SqliteDatabase("song.db")


class Songs(pw.Model):
    title = pw.CharField()
    author = pw.CharField()
    finger_print = pw.CharField()
    path = pw.CharField()

    class Meta:
        database = db  # This model uses the "song.db" database.


def add_a_song(data_base_path: str, song_path: str, song_title: str, song_author: str):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    data_base.create_tables([Songs])
    song1 = Songs(title=song_title, author=song_author, finger_print=str(sh.musical_print_creation(song_path)),
                  path=song_path)
    song1.save()
    data_base.close()


def get_finger_print(data_base_path: str, song_title: str, song_author: str):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for song in Songs.select().where(Songs.title == song_title and Songs.author == song_author):
        return ast.literal_eval(song.finger_print)
    data_base.close()


def see_songs_in_data_base(data_base_path):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for song in Songs.select():
        print(song.title + "-" + song.author)
    data_base.close()


def delete_a_song_in_data_base(data_base_path: str, song_title: str, song_author: str):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for song in Songs.select().where(Songs.title == song_title and Songs.author == song_author):
        song.delete_instance()
    data_base.close()


def delete_all_songs_in_data_base(data_base_path: str):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for song in Songs.select():
        song.delete_instance()
    data_base.close()


def get_all_data_base(data_base_path: str):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    list_song = []
    for song in Songs.select():
        list_song.append([song.title, song.author, ast.literal_eval(song.finger_print)])
    return list_song


if __name__ == '__main__':
    pass
# utiliser pathlib pour faire un dossier avec le sons