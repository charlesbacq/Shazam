import peewee as pw
from flask import flash

db = pw.SqliteDatabase("song.db")
db1 = pw.SqliteDatabase("people.db")
db2 = pw.SqliteDatabase("song_user.db")


def add_a_songE(data_base_path, song_title, song_author):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    data_base.create_tables([Songs])
    song1 = SongsE(title=song_title, author=song_author)
    song1.save()
    data_base.close()

def delete_a_song_in_data_baseE(data_base_path: str, song_title: str, song_author: str):
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for song in Songs.select().where(Songs.title == song_title and Songs.author == song_author):
        song.delete_instance()
    data_base.close()

def get_all_songs_userE(data_base_path):
    ''' la data base correspond à celle d'un utilisateur avec toutes ses musiques'''
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    list_song = []
    for song in Songs.select():
        list_song.append([song.title, song.author])
    return list_song

class RegistrationUser(pw.Model):
    username = pw.CharField()
    email = pw.CharField()
    #password = pw.PasswordField()
    confirmed_password = pw.CharField()
    def validate_username(self,username,db1):
        if username not in db1.username :
            return True
    def validate_email(self,email,db1):
        if email not in db1.email:
            return True
    def validate_password(self):
        return True
    def validate_confirmed_password(self):
        return True

class LoginUser(pw.Model):
    email = pw.CharField()
    #password = pw.PasswordField()
    def validate_email_password(self, User, db1):
        if User.email in db1.email :
            user = User.select().where(User.email == db1.email).get()
            #if user.password == User.password:
                #return True
            #else:
                #return False
            return True