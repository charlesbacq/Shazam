import librosa as lb
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import hashlib
import random as rd

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


def generate_hashes(peaks, fan_value=DEFAULT_FAN_VALUE):
    """
    Function that gives the musical print of the song where every temporal mark is
    turn into a hash
    :param peaks: Peaks
    :param fan_value:
    :return:
    """
    # bruteforce all peaks
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):

                # take current & next peak frequency value
                freq1 = peaks[i][IDX_FREQ_I]
                freq2 = peaks[i + j][IDX_FREQ_I]

                # take current & next -peak time offset
                t1 = peaks[i][IDX_TIME_J]
                t2 = peaks[i + j][IDX_TIME_J]

                # get diff of time offsets
                t_delta = t2 - t1
                print(str(freq1), str(freq2), str(t_delta))
                # check if delta is between min & max
                if MIN_HASH_TIME_DELTA <= t_delta <= MAX_HASH_TIME_DELTA:
                    h = hashlib.sha1(b'%s %s %s' % (str(freq1), str(freq2), str(t_delta)))

                    yield h.hexdigest()[0:FINGERPRINT_REDUCTION], t1


def sample_loading(sample):
    """
    Function that takes a sample and loads it in Librosa to be analyse
    :param sample: sample of the song you want to load
    :return: A loaded sample exploitable in Librosa
    """
    return lb.load(sample)


def create_peaks(sample):
    """
    Function that gives the peaks(time and frequency) in a song
    :param sample: sample of the song you want to analyse
    :return: List of the peaks time and frequency : [[time_peak,freq_peak] for peaks in song]
    """
    y, sr = sample_loading(sample)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr,
                                             hop_length=512,
                                             aggregate=np.median)
    S = np.abs(lb.stft(y))
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


def musical_print_creation(sample):
    """
    Function that takes a sample of a song and gives its musical print
    :param sample: sample of the song you want to turn into the spectrogram
    :return: muscial print : list of temporal marks
    of this form : [[freq1, freq2, t_delta], t1]
    """
    y, sr = sample_loading(sample)
    peaks = create_peaks(sample)
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
                if t_delta >= MIN_HASH_TIME_DELTA and t_delta <= MAX_HASH_TIME_DELTA:
                    musical_print.append([[freq1, freq2, t_delta], t1])
                    # musical_print.append([hashlib.sha1("%s|%s|%s" % (str(freq1), str(freq2), str(t_delta))), t1])
    return musical_print


def display_spectro(sample, show_peaks=True):
    """
    Function that displays the spectrogram of a sample
    :param sample: sample of the song you want to turn into the spectrogram
    :param show_peaks: bool if True shows the peaks selected in the song on the spectrogram
    :return: void
    """
    y, sr = sample_loading(sample)
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

    if (show_peaks):
        peaks = create_peaks(sample)
        peaks_frequency = [peaks[i][0] for i in range(len(peaks))]
        peaks_time = [peaks[i][1] for i in range(len(peaks))]
        plt.scatter(peaks_time, peaks_frequency)

    plt.show()


def most_frequent(list):
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


def matching_random(data_base, musical_print):
    """
    Function that takes a musical print and
    randomly gives a the matching song in the
    database
    :param data_base: List that gives for each song its name, artist and musical print
    :param musical_print: Musical print of the song you want to know the name
    :return: The name and artist of the song that matched in the data base, and a statistic
    showing the accuracy of the match : ("name", "artist", float stat)
    """
    random_int = rd.randint(0, len(data_base) - 1)
    # print("Random Match : ", data_base[random_int][0], " - ", data_base[random_int][1] , "; Accuracy : ", 0)
    return data_base[random_int][0], data_base[random_int][1], 0


def matching_brute_force(data_base, musical_print):
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
    # Brute forced researsh of temporal marks match comparing musical print in the data base with the one
    # of the song
    match = [matching_random(data_base, musical_print)[0], matching_random(data_base, musical_print)[1],
             matching_random(data_base, musical_print)[2]]
    for song_musical_print in data_base:
        matching_detlaT = []
        nb_temporal_mark_match = 0
        for song_temporal_mark in song_musical_print[2]:

            for sample_temporal_mark in musical_print:
                if (sample_temporal_mark[0] == song_temporal_mark[0]):
                    matching_detlaT.append(song_temporal_mark[1] - sample_temporal_mark[1])
                    nb_temporal_mark_match += 1
        plt.hist(matching_detlaT)
        print("Nombre de match pour " + song_musical_print[0] + "-" + song_musical_print[1] + " :",
              nb_temporal_mark_match)
        print("Meuilleur DeltaT : ", most_frequent(matching_detlaT))
        plt.show()
        accuracy = nb_temporal_mark_match * matching_detlaT.count(most_frequent(matching_detlaT)) / len(musical_print)
        if (accuracy > match[2]):
            match = [song_musical_print[0], song_musical_print[1], accuracy]
    print(match)


