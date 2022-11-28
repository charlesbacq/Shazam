import peewee as pw

db = pw.SqliteDatabase('song.db')

class Songs(pw.Model):
    title = pw.CharField()
    author = pw.CharField()
    finger_print = pw.CharField()

    class Meta:
        database = db # This model uses the "song.db" database.

if __name__ == '__main__':
    db.connect()
    db.create_tables([Songs])
    song1 = Songs(title = "BOP", author = "Dababy", finger_print = "musical_print")
    song1.save()
    for song in Songs.select():
        print(Songs.title)