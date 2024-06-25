import librosa
import numpy as np
import pandas as pd


# Key extraction file (taken from: https://github.com/jackmcarthur/musical-key-finder)
class Tonal_Fragment:
    def __init__(self, waveform, sr, tstart=None, tend=None):
        self.waveform = waveform
        self.sr = sr
        self.tstart = (
            librosa.time_to_samples(tstart, sr=sr) if tstart is not None else None
        )
        self.tend = librosa.time_to_samples(tend, sr=sr) if tend is not None else None
        self.y_segment = self.waveform[self.tstart : self.tend]
        self.chromograph = librosa.feature.chroma_cqt(
            y=self.y_segment, sr=self.sr, bins_per_octave=24
        )

        self.chroma_vals = [np.sum(self.chromograph[i]) for i in range(12)]
        pitches = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.keyfreqs = {pitches[i]: self.chroma_vals[i] for i in range(12)}

        keys = [pitches[i] + " major" for i in range(12)] + [
            pitches[i] + " minor" for i in range(12)
        ]

        maj_profile = [
            6.35,
            2.23,
            3.48,
            2.33,
            4.38,
            4.09,
            2.52,
            5.19,
            2.39,
            3.66,
            2.29,
            2.88,
        ]
        min_profile = [
            6.33,
            2.68,
            3.52,
            5.38,
            2.60,
            3.53,
            2.54,
            4.75,
            3.98,
            2.69,
            3.34,
            3.17,
        ]

        self.maj_key_corrs = [
            round(
                np.corrcoef(
                    maj_profile,
                    [self.keyfreqs[pitches[(i + m) % 12]] for m in range(12)],
                )[1, 0],
                3,
            )
            for i in range(12)
        ]
        self.min_key_corrs = [
            round(
                np.corrcoef(
                    min_profile,
                    [self.keyfreqs[pitches[(i + m) % 12]] for m in range(12)],
                )[1, 0],
                3,
            )
            for i in range(12)
        ]

        self.key_dict = {
            **{keys[i]: self.maj_key_corrs[i] for i in range(12)},
            **{keys[i + 12]: self.min_key_corrs[i] for i in range(12)},
        }

        self.key = max(self.key_dict, key=self.key_dict.get)
        self.bestcorr = max(self.key_dict.values())

        self.altkey = None
        self.altbestcorr = None
        for key, corr in self.key_dict.items():

            if corr > self.bestcorr * 0.9 and corr != self.bestcorr:
                self.altkey = key
                self.altbestcorr = corr


def extract_keys(y, sr):  # Audio and sampling rate returned by librosa

    y_harmonic, _ = librosa.effects.hpss(y)
    tf = Tonal_Fragment(y_harmonic, sr)

    correlation_values = np.array(list(tf.key_dict.values()))
    abs_correlations = np.abs(correlation_values)
    probabilities = abs_correlations * 100 / np.sum(abs_correlations)
    prob = sorted(probabilities, reverse=True)

    top_keys = sorted(tf.key_dict, key=tf.key_dict.get, reverse=True)[:3]
    top_3_keys = {top_keys[i]: round(prob[i], 2) for i in range(3)}

    return top_3_keys
