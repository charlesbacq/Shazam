import Shazamage *


#print(musical_print_creation("Avicii - Hey Brother.flac")[0:10])
display_spectro("Avicii - Hey Brother.flac")
song_print = [["Hey brother", "Avicii", musical_print_creation("Avicii - Hey Brother.flac")], ["Give Me Your Loving (feat. Lorne)", "Armand van Helden", musical_print_creation("Armand van Helden - Give Me Your Loving (feat. Lorne).flac")]]
sample_print = musical_print_creation("Avicii - Hey Brother 142.flac")
matching_random(song_print, sample_print)
matching_brute_force(song_print, sample_print)