import Shazamage.py as sh

if __name__ == '__main__':
    # print(musical_print_creation("Avicii - Hey Brother.flac")[0:10])
    sh.display_spectro("Avicii - Hey Brother.flac")
    song_print = [["Hey brother", "Avicii", sh.musical_print_creation("Avicii - Hey Brother.flac")],
                  ["Give Me Your Loving (feat. Lorne)", "Armand van Helden",
                   sh.musical_print_creation("Armand van Helden - Give Me Your Loving (feat. Lorne).flac")]]
    sample_print = sh.musical_print_creation("Avicii - Hey Brother 142.flac")
    sh.matching_random(song_print, sample_print)
    sh.matching_brute_force(song_print, sample_print)
