import peewee as pw
import shazamage as sh
import ast
import pathlib as path

db_song_path = "Shazamage/song.db"
db_song = pw.SqliteDatabase(db_song_path)


class Songs(pw.Model):
    title = pw.CharField()
    author = pw.CharField()
    finger_print = pw.CharField()
    path = pw.CharField()

    class Meta:
        database = db_song  # This model uses the "song.db" database.


def add_a_song(data_base_path: str, song_path: str, song_title: str, song_author: str):
    '''Function that takes in parameter all the attributes of a song and add it in the database
    :param 4 strings which correspond to the parameters necessary to add a line in the database
    :return add a line in the database'''
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    data_base.create_tables([Songs])
    song1 = Songs(title=song_title, author=song_author, finger_print=str(sh.musical_print_creation(song_path)),
                  path=song_path)
    song1.save()
    data_base.close()


def get_finger_print(data_base_path: str, song_title: str, song_author: str):
    '''Function to obtain the finger print of a song from title and the author of the song
        :param name of the data base, title and artist of the song
        :return finger print of the song'''
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for song in Songs.select().where(Songs.title == song_title and Songs.author == song_author):
        return ast.literal_eval(song.finger_print)
    data_base.close()


def see_songs_in_data_base(data_base_path: str):
    '''Function which display for each song the title and the author'''
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for song in Songs.select():
        print(song.title + "-" + song.author)
    data_base.close()


def delete_a_song_in_data_base(data_base_path: str, song_title: str, song_author: str):
    '''Delete a song from the database
    :param title and author of the song you want to delete
    :return delete a line in the database'''
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for song in Songs.select().where(Songs.title == song_title and Songs.author == song_author):
        song.delete_instance()
    data_base.close()


def delete_all_songs_in_data_base(data_base_path: str):
    '''Function which delete all the songs of the database
     :param name of the database
     :return database empty'''
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for song in Songs.select():
        song.delete_instance()
    data_base.close()


def get_all_data_base(data_base_path: str):
    '''Function which, get all the attributes of all the songs and add it in a list
    :param name of the database
    :return a list of list containing for each song the title, the author and the fingerprint
    exemple: [[title1,author1,fingerprint1],[title2,author2,fingerprint2],.....] '''
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    list_song = []
    for song in Songs.select():
        list_song.append([song.title, song.author, ast.literal_eval(song.finger_print)])
    return list_song


def add_file_in_data_base(data_base_path: str, file_path: str):
    data_file_path = path.Path(file_path)
    A = [str(x) for x in data_file_path.iterdir()]
    B = []
    for song in A:
        song = [song]
        song.append(song[0])
        song[0] = list(song[0].split('-'))[0:2]
        song[0][0] = list(song[0][0].split('\\'))[1]
        song[0][1] = song[0][1].replace('.flac', '')
        B.append(song)
    C = []
    for i in B:
        C.append([i[1], i[0][0], i[0][1]])
    for i in range(len(C)):
        add_a_song(data_base_path, C[i][0], C[i][2], C[i][1])
        print('Progression', i / len(C) * 100, '%')


def get_all_data_base_as_test_data(data_base_path: str):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    list_song = []
    for song in Songs.select():
        list_song.append([song.title, song.author, song.path])
    return list_song

test_db = pw.SqliteDatabase("test_song.db")


class TestSongs(pw.Model):
    title = pw.CharField()
    author = pw.CharField()
    finger_print = pw.CharField()
    path = pw.CharField()

    class Meta:
        database = test_db  # This model uses the "song.db" database.


def add_a_test_song(test_data_base_path: str, song_path: str, song_title: str, song_author: str):
    data_base = pw.SqliteDatabase(test_data_base_path)
    data_base.connect()
    data_base.create_tables([TestSongs])
    song1 = TestSongs(title=song_title, author=song_author, finger_print=str(sh.musical_print_creation(song_path)),
                  path=song_path)
    song1.save()
    data_base.close()


def see_test_songs_in_test_data_base(test_data_base_path: str):
    data_base = pw.SqliteDatabase(test_data_base_path)
    data_base.connect()
    for song in TestSongs.select():
        print(song.title + "-" + song.author)
    data_base.close()


def delete_a_test_song_in_test_data_base(data_base_path: str, song_title: str, song_author: str):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for song in TestSongs.select().where(Songs.title == song_title and Songs.author == song_author):
        song.delete_instance()
    data_base.close()


def delete_all_test_songs_in_test_data_base(data_base_path: str):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for song in TestSongs.select():
        song.delete_instance()
    data_base.close()


def get_all_test_data_base(data_base_path: str):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    list_song = []
    for song in TestSongs.select():
        list_song.append([song.title, song.author, ast.literal_eval(song.finger_print)])
    return list_song


def add_test_file_in_data_base(data_base_path: str, file_path: str):
    data_file_path = path.Path(file_path)
    A = [str(x) for x in data_file_path.iterdir()]
    B = []
    for song in A:
        song = [song]
        song.append(song[0])
        song[0] = list(song[0].split('-'))[0:2]
        song[0][0] = list(song[0][0].split('\\'))[1]
        song[0][1] = song[0][1].replace('.flac', '')
        B.append(song)
    C = []
    for i in B:
        C.append([i[1], i[0][0], i[0][1]])
    for i in range(len(C)):
        add_a_test_song(data_base_path, C[i][0], C[i][2], C[i][1])
        print('Progression', i / len(C) * 100, '%')


def get_all_test_data_base_as_test_data(data_base_path: str):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    list_song = []
    for song in TestSongs.select():
        list_song.append([song.title, song.author, song.path])
    return list_song



if __name__ == '__main__':
    #add_test_file_in_data_base('test_song.db','sons_test')
    #delete_all_test_songs_in_test_data_base('test_song.db')
    #see_test_songs_in_test_data_base('test_song.db')
    #add_file_in_data_base('song.db','sons_flac')
    #delete_all_songs_in_data_base('song.db')
    #see_songs_in_data_base('song.db')
    pass


