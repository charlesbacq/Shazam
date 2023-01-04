# Imports
import peewee as pw
import ast
import pathlib as path

# Path and database
#data_base_path = 'C:/Users/briac/OneDrive/ENPC2A/semestre1/tdlog/Projet_shazam/Shazam/Shazam/user.db'
db_user_path = "Shazamage/user.db"
db_user = pw.SqliteDatabase(db_user_path)


# Define Exceptions
class UserNameError(Exception):
    pass


class PasswordError(Exception):
    pass


# Define Tables
class Users(pw.Model):
    username = pw.CharField()
    email = pw.CharField()
    password = pw.CharField()

    class Meta:
        database = db_user  # This model uses the "user.db" database.


class UsersMusics(pw.Model):
    username = pw.CharField()
    title = pw.CharField()
    author = pw.CharField()

    class Meta:
        database = db_user


# Functions for users/passwords management
def create_user(user_name: str, user_email: str, user_password: str):
    """Function that takes in parameters 2 strings and return the correspondant instance of class Users
        :param 2 strings necessary to define an instance of class Users
        :return instance of class Users """
    user0 = Users(username=user_name, email=user_email, password=user_password)
    return user0


def add_user(data_base_path: str, user_name: str, user_email: str, user_password: str):
    """Function that takes in parameters all the attributes of an instance of class Users and add it in the table users of the database
    :param 3 strings which correspond to the parameters necessary to add a line in the table users of the database
    :return add a line in the table users of the database"""
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    data_base.create_tables([Users])
    user0 = create_user(user_name, user_email, user_password)
    user0.save()
    data_base.close()


def delete_user(data_base_path: str, user_name: str):
    """Delete a line in the table users of the database
    :param database path and username of the user you want to delete
    :return delete a line in the table users of the database"""
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for user in Users.select().where(Users.username == user_name):
        user.delete_instance()
    data_base.close()


def delete_all_users(data_base_path: str):
    """Function which delete all the lines in the table users of the database
     :param database path
     :return users table empty"""
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for user in Users.select():
        user.delete_instance()
    data_base.close()


def assert_username(user_name: str, data_base_path: str):
    try:
        data_base = pw.SqliteDatabase(data_base_path)
        data_base.connect()
        Request = Users.select().where(Users.username == user_name)
        data_base.close()

        if (Request.count() != 0):
            raise UserNameError

        return True

    except UserNameError:
        print("This username is already taken! Please choose another username")
        return False

def assert_connection(user_name: str, user_password: str, data_base_path: str):
    """Function which allows the connection if the user writes a right (username,password) couple
     :param 3 strings (informations of connection)
     :return Bool (and print the type of error if there is one)"""
    try:
        data_base = pw.SqliteDatabase(data_base_path)
        data_base.connect()
        Request = Users.select().where(Users.username == user_name)
        data_base.close()

        if (Request.count() == 0):
            raise UserNameError

        for user in Request:
            if user.password != user_password:
                raise PasswordError
        return True

    except UserNameError:
        print("This username does not exist, please sign in!")
        return False
    except PasswordError:
        print("Password incorrect")
        return False

# Functions for users when they are connected
def create_user_music(user_name: str, music_title: str, music_author: str):
    """Function that takes in parameters 3 strings and return the correspondant instance of class UsersMusics
            :param 3 strings necessary to define an instance of class UsersMusics
            :return instance of class UsersMusics """
    music0 = UsersMusics(username=user_name, title=music_title, author=music_author)
    return music0


def add_user_music(data_base_path: str, user_name: str, music_title: str, music_author: str):
    """Function that takes in parameters all the attributes of an instance of class UsersMusics and add it in the table usersmusics of the database
        :param 4 strings which correspond to the parameters necessary to add a line in the table usersmusics of the database
        :return add a line in the table usersmusics of the database"""
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    data_base.create_tables([UsersMusics])
    music0 = create_user_music(user_name, music_title, music_author)
    music0.save()
    data_base.close()


def delete_user_music(data_base_path: str, user_name: str, music_title: str, music_author: str):
    """Delete a music of a user from the table usersmusics of the database
    :param database path, username, title and author of the user music you want to delete
    :return delete a line in the table usersmusics of the database"""
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for music in UsersMusics.select().where(
            UsersMusics.username == user_name and UsersMusics.title == music_title and UsersMusics.author == music_author):
        music.delete_instance()
    data_base.close()


def delete_all_musics(data_base_path: str):
    '''Function which delete all the musics in the table usersmusics of the database
     :param database path
     :return table usersmusics empty'''
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for music in UsersMusics.select():
        music.delete_instance()
    data_base.close()


def see_user_musics(data_base_path: str, user_name: str):
    """Function which display for a user the titles and the authors of all his musics"""
    data_base = pw.SqliteDatabase(data_base_path)
    data_base.connect()
    for music in UsersMusics.select().where(UsersMusics.username == user_name):
        print(music.title + "-" + music.author)
    data_base.close()


if __name__ == '__main__':
    # delete the previous users
    delete_all_users(db_user_path)
    #delete_all_musics(data_base_path)

    # Data user 1
    username1 = 'briac'
    password1 = '123'
    email1 = "briac@"

    user1_music1_title= '16'
    user1_music1_author = 'Baby Keem'

    user1_music2_title = 'Otto'
    user1_music2_author = 'SCH'

    # Data user 2
    username2 = 'cezambre'
    password2 = '456'
    email2= 'cezambre@'

    user2_music1_title = 'Mamacita'
    user2_music1_author = 'Ninho'

    user2_music2_title = 'Môme'
    user2_music2_author = 'Lomepal'

    # Data user 3
    username3 = 'ysee'
    password3 = '789'
    email3 = 'ysee@'

    user3_music1_title = 'Plume'
    user3_music1_author = 'Nekfeu'

    user3_music2_title = 'No Love'
    user3_music2_author = 'Dinos'

    # add the 3 users to the data base
    add_user(db_user_path, username1, email1, password1)
    add_user(db_user_path, username2, email2, password2)
    add_user(db_user_path, username3, email3, password3)


    # verify the information of connection
    assert_connection(username1, password1, db_user_path)
    assert_connection(username2, password2, db_user_path)
    assert_connection(username3, password3, db_user_path)

    #Add musics of users 1,2,3
    add_user_music(db_user_path, username1, user1_music1_title, user1_music1_author)
    add_user_music(db_user_path, username3, user3_music1_title, user3_music1_author)
    add_user_music(db_user_path, username2, user2_music1_title, user2_music1_author)
    add_user_music(db_user_path, username3, user3_music2_title, user3_music2_author)
    add_user_music(db_user_path, username1, user1_music2_title, user1_music2_author)
    add_user_music(db_user_path, username2, user2_music2_title, user2_music2_author)

    #See users musics
    see_user_musics(db_user_path, username1)
    print('-----------------------------------')
    see_user_musics(db_user_path, username2)
    print('-----------------------------------')
    see_user_musics(db_user_path, username3)
    print('-----------------------------------')

