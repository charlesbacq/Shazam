import Shazamage as sh
import shazam_data_base as db

if __name__ == '__main__':
    # print(musical_print_creation("Avicii - Hey Brother.flac")[0:10])
    #sh.display_spectro("Avicii - Hey Brother.flac")

    data_base = db.get_all_data_base("song.db")
    sample_print = sh.musical_print_creation("hey brother maison.flac")
    sh.matching_random(data_base, sample_print)
    print(sh.matching_brute_force(data_base, sample_print))
