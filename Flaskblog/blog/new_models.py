import peewee as pw

db = pw.SqliteDatabase('people.db')

class User(pw.Model):
    id = pw.CharField()
    username = pw.CharField()
    email = pw.CharField()
    password = pw.CharField()

class RegistrationUser(pw.Model):
    username = pw.CharField()
    email = pw.CharField()
    password = pw.CharField()
    confirmed_password = pw.CharField()
    def validate_username(self):
        return True
    def validate_email(self):
        return True
    def validate_password(self):
        return True
    def validate_confirmed_password(self):
        return True

class LoginUser(pw.Model):
    email = pw.CharField()
    password = pw.CharField()
    def validate_email(self):
        return True
    def validate_password(self):
        return True

class Music(pw.Model):
    title = pw.CharField()
    author = pw.CharField()
    creation_date = pw.DateField()
    duration = pw.DateField()



