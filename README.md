Shazamage
==========

Audio fingerprinting and recognition algorithm implemented in Python, see the explanation here:  
[How it works](https://www.lesnumeriques.com/audio/magie-shazam-dans-entrailles-algorithme-a2375.html)

The algorithm can memorize .flac type audio by listening to it once and fingerprinting it. Then by reading from disk, it attempts to match the audio against the fingerprints held in the database, returning the song being played. 
You can use this tool using the webpage, using $run.py.
On the website each user have his own database where he can 
add songs of his own.
You can also create your own data base in $cli.py.

This project is the final project of the class TDLOG.
## SetUp

## Fingerprinting

Let's say we want to fingerprint the song Freed-from-desire by Gala  and add
it to the database called "songs.db".
You can follow the instructions on the webpage in part "Upload" or you can execute this code : 
```python
>>>add_a_song(data_base_path: "songs.db", song_path: "Freed-from-desire-Gala.flac",
...song_title: 'Freed-from-desire', song_author: 'Gala')
```

 

## Tuning

Inside `Shazamage/shazamage.py`, you may want to adjust following parameters (some values are given below).

    IDX_FREQ_I = 0
    IDX_TIME_J = 1
    DEFAULT_SAMPLING_RATE = 22050
    DEFAULT_HOP_LENGHT = 512
    DEFAULT_WAIT = 5
    DEFAULT_PEAKS_DELTA = 0.5
    DEFAULT_FAN_VALUE = 40
    DEFAULT_AMP_MIN = 3
    MIN_HASH_TIME_DELTA = 0
    MAX_HASH_TIME_DELTA = 200

    
These parameters are described within the file in detail. Read that in-order to understand the impact of changing these values.

## Matching
Let's say we want to launch the recognition tool on a song on your disk : "Avicii-Hey Brother.flac"
You can follow the instructions on the webpage in part "Matching" or you can execute this code : 
```python
>>>db.see_songs_in_data_base('song.db')
>>>v = sh.BruteforceMatcher()
>>>v.load_db('song.db')
>>>print(v.match('Avicii-Hey Brother.flac'))
```
Where 'song.db' is your database of songs. You can print in the console the statistic concerning
the number of match for each song by setting to True the parameters : show_histo and show_stats of the 
function v.match.

##Visualization of the Spectrogram 
You can also visualize the "Constellation Spectrogram" and the Usual Spectrogram of a song
using this code : 
```python
>>>display_spectro(sample_path: str, show_peaks: bool = True):
```

## Testing
