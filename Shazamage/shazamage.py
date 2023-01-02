from pathlib import Path
from typing import List, Tuple


import numpy as np
import matplotlib.pyplot as plt
import hashlib
import random as rd
import librosa
#import librosa.display
from Shazamage import shazam_data_base as db

IDX_FREQ_I = 0
IDX_TIME_J = 1

# Size of the FFT window, affects frequency granularity
DEFAULT_WINDOW_SIZE = 4096

# Ratio by which each sequential window overlaps the last and the
# next window. Higher overlap will allow a higher granularity of offset
# matching, but potentially more fingerprints.
DEFAULT_OVERLAP_RATIO = 0.5

# Degree to which a fingerprint can be paired with its neighbors --
# higher will cause more fingerprints, but potentially better accuracy.
DEFAULT_FAN_VALUE = 15

# Minimum amplitude in spectrogram in order to be considered a peak.
# This can be raised to reduce number of fingerprints, but can negatively
# affect accuracy.
DEFAULT_AMP_MIN = 10

# Number of cells around an amplitude peak in the spectrogram in order
# for Dejavu to consider it a spectral peak. Higher values mean less
# fingerprints and faster matching, but can potentially affect accuracy.
PEAK_NEIGHBORHOOD_SIZE = 20

# Thresholds on how close or far fingerprints can be in time in order
# to be paired as a fingerprint. If your max is too low, higher values of
# DEFAULT_FAN_VALUE may not perform as expected.
MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200

# Number of bits to throw away from the front of the SHA1 hash in the
# fingerprint calculation. The more you throw away, the less storage, but
# potentially higher collisions and misclassifications when identifying songs.
FINGERPRINT_REDUCTION = 20


def sample_loading(sample_path: str):
    """
    Function that takes a sample path and loads it in Librosa to be analyse
    :param sample_path: path of the sample of the song you want to load
    :return: A loaded sample exploitable in Librosa
    """
    return librosa.load(sample_path)


def create_peaks(sample_path: str):
    """
    Function that gives the peaks(time and frequency) in a song
    :param sample_path: path of the sample path of the song you want to analyse
    :return: List of the peaks time and frequency : [[time_peak,freq_peak] for peaks in song]
    """
    y, sr = sample_loading(sample_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr,
                                             hop_length=512,
                                             aggregate=np.median)
    S = np.abs(librosa.stft(y))
    peaks = librosa.util.peak_pick(onset_env, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.5, wait=10)
    peaks_frequency = []
    for t in peaks:
        max_f_t = 0
        for i in range(S.shape[0]):
            if S[i][t] > S[max_f_t][t]:
                max_f_t = i
        peaks_frequency.append(max_f_t)
    times = librosa.times_like(onset_env, sr=sr, hop_length=512)
    return [[peaks_frequency[i], times[peaks[i]]] for i in range(len(peaks))]


def musical_print_creation(sample_path: str, is_hash: bool = False):
    """
    Function that takes a sample of a song and gives its musical print
    :param is_hash: if True the temporal marks ar of this form [hash, t1]
    :param sample_path: path of the sample of the song you want to turn into the spectrogram
    :return: musical print : list of temporal marks
    of this form : [[freq1, freq2, t_delta], t1]

    """
    peaks = create_peaks(sample_path)
    musical_print = []
    for i in range(len(peaks)):
        for j in range(1, DEFAULT_FAN_VALUE):
            if (i + j) < len(peaks):

                # take current & next peak frequency value
                freq1 = peaks[i][IDX_FREQ_I]
                freq2 = peaks[i + j][IDX_FREQ_I]

                # take current & next -peak time of²fset
                t1 = peaks[i][IDX_TIME_J]
                t2 = peaks[i + j][IDX_TIME_J]

                # get diff of time offsets
                t_delta = t2 - t1
                # check if delta is between min & max
                if MIN_HASH_TIME_DELTA <= t_delta <= MAX_HASH_TIME_DELTA:
                    if not is_hash:
                        musical_print.append([[freq1, freq2, t_delta], t1])
                    else:

                        phrase = str(freq1) + '|' + str(freq2) + '|' + str(t_delta)
                        phrase = str.encode(phrase)
                        musical_print.append([hashlib.sha1(phrase).hexdigest(), t1])
    return musical_print


def display_spectro(sample_path: str, show_peaks: bool = True):
    """
    Function that displays the spectrogram of a sample
    :param sample_path: path of the sample of the song you want to turn into the spectrogram
    :param show_peaks: bool if True shows the peaks selected in the song on the spectrogram
    :return: void
    """
    y, sr = sample_loading(sample_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr,
                                             hop_length=512,
                                             aggregate=np.median)
    times = librosa.times_like(onset_env, sr=sr, hop_length=512)
    fig, ax = plt.subplots(nrows=2, sharex=True)
    D = np.abs(librosa.stft(y))
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                             y_axis='log', x_axis='time', ax=ax[1])
    ax[0].plot(times, onset_env, alpha=0.8, label='Onset strength')
    ax[0].vlines(times, 0,
                 onset_env.max(), color='r', alpha=0.8,
                 label='Selected peaks')
    ax[0].legend(frameon=True, framealpha=0.8)
    ax[0].label_outer()

    if show_peaks:
        peaks = create_peaks(sample_path)
        peaks_frequency = [peaks[i][0] for i in range(len(peaks))]
        peaks_time = [peaks[i][1] for i in range(len(peaks))]
        plt.scatter(peaks_time, peaks_frequency)

    plt.show()


def most_frequent(list: List):
    """
    Function that give the most frequent element in a List
    :param list: List of element
    :return: The most frequent element in the list
    """
    if len(list) == 0:
        return "no_match"
    counter = 0
    num = list[0]

    for i in list:
        curr_frequency = list.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            num = i

    return num



class BaseMatcher:
    NAME: str
    data_base = []

    def load_db(self, data_base_path: str):
        self.data_base = db.get_all_data_base(data_base_path)

    def match(self, song_path: str):
        raise NotImplemented()

    def test(self, test_data_base_path: str):
        test_data_base = db.get_all_data_base_as_test_data(test_data_base_path)
        nb_good_match = 0
        for song in test_data_base:
            match = self.match(song[2])
            if match[0] == song[0] and match[1] == song[1]:
                nb_good_match += 1
        return nb_good_match / len(test_data_base) * 100


class RandomMatcher(BaseMatcher):
    NAME = "random"

    def match(self, song_path: str):
        """
        Function that takes a song_path and
        randomly gives a the matching song in the
        database
        :param song_path:  Musical print of the song you want to know the name
        :return: The name and artist of the song that matched in the data base, and a statistic
        showing the accuracy of the match : ["name", "artist", float stat = 0]
        """
        random_int = rd.randint(0, len(self.data_base) - 1)
        return [self.data_base[random_int][0], self.data_base[random_int][1], 0]


class BruteforceMatcher(BaseMatcher):
    NAME = "brute-force"

    def match(self, song_path: str, show_histo: bool = False, show_stats: bool = False):
        """
        Function that takes a musical print and  gives a the matching song in the
        database using brute forcing
        :param data_base: List that gives for each song its name, artist and musical print
        :param musical_print: Musical print of the song you want to know the name
        :return: The name and artist of the song that matched in the data base, and a statistic
        showing the accuracy of the match : ("name", "artist", float stat)
        """
        song_title = 'unknow'
        matching_rate = 0
        musical_print = musical_print_creation(song_path)
        # Brute forced researsh of temporal marks match comparing musical print in the data base with the one
        # of the song
        match = ['none', 'none',
                0]
        for song_musical_print in self.data_base:
            matching_detlaT = []
            nb_temporal_mark_match = 0
            for song_temporal_mark in song_musical_print[2]:

                for sample_temporal_mark in musical_print:
                    if sample_temporal_mark[0] == song_temporal_mark[0]:
                        matching_detlaT.append(song_temporal_mark[1] - sample_temporal_mark[1])
                        nb_temporal_mark_match += 1
            if show_stats:
                print("Nombre de match pour " + song_musical_print[0] + "-" + song_musical_print[1] + " :",
                      nb_temporal_mark_match)
                print("Meuilleur DeltaT : ", most_frequent(matching_detlaT))
            if show_histo:
                plt.hist(matching_detlaT)
                plt.show()
            accuracy = nb_temporal_mark_match * matching_detlaT.count(most_frequent(matching_detlaT)) / len(
                musical_print)
            if accuracy > match[2]:
                match = [song_musical_print[0], song_musical_print[1], accuracy]
        return match


MATCHERS = {matcher_class.NAME: matcher_class
            for matcher_class in [RandomMatcher, BruteforceMatcher]}

v = MATCHERS["random"]()
