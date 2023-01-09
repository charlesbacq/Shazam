from Shazamage import shazamage as sh
from Shazamage import shazam_data_base as db

if __name__ == '__main__':
    db.see_songs_in_data_base('song.db')
    v = sh.BruteforceMatcher()
    v.load_db('song.db')
    #print(v.test('test_song.db'))
    #print(v.match('hey brother maison.flac'))
    #print(v.match('Avicii - Hey Brother extrait.flac'))
    #print(v.match('hey brother maison2.flac'))
    print(v.match('Avicii - Hey Brother 142 copie.flac'))
    pass

