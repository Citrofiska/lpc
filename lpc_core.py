import numpy as np
import soundfile as sf # write signal to wav
import scipy.signal as signal
import librosa
import os
from lpc_config import *

def compute_lpc_envelope(frame, order, n_fft):
    """Compute the LPC envelope of a single frame."""
    lpc_coeffs = librosa.lpc(frame, order)
    w, h = signal.freqz([1], lpc_coeffs, worN=n_fft // 2 + 1)
    return np.abs(h)

def cross_synthesis(filename_car, filename_mod, sr, output_dir, order, fft_size, hop_size):
    # Load the carrier and modulator signals
    carrier, _ = librosa.load(car_dir+filename_car, sr=sr)
    modulator, _ = librosa.load(mod_dir+filename_mod, sr=sr)
    min_length = min(len(carrier), len(modulator))
    # trim to the length of the shorter one
    carrier = carrier[:min_length]
    modulator = modulator[:min_length]
    print(f'Number of samples in both audios is {min_length}')

    # Compute the STFT of both signals
    stft_carrier = librosa.stft(carrier, n_fft=fft_size, hop_length=hop_size)
    stft_modulator = librosa.stft(modulator, n_fft=fft_size, hop_length=hop_size)

    carrier_magnitude = np.abs(stft_carrier)
    modulator_magnitude = np.abs(stft_modulator)

    # Number of frames
    n_frames = carrier_magnitude.shape[1]

    # Initialize arrays to hold the LPC envelopes
    carrier_envelopes = np.zeros(carrier_magnitude.shape)
    modulator_envelopes = np.zeros(modulator_magnitude.shape)

    # Compute LPC envelopes for each frame
    for frame in range(n_frames):
        # Compute LPC envelopes for each frame
        carrier_envelopes[:, frame] = compute_lpc_envelope(carrier_magnitude[:, frame], order, fft_size)
        modulator_envelopes[:, frame] = compute_lpc_envelope(modulator_magnitude[:, frame], order, fft_size)

    # Normalize the envelopes
    carrier_envelopes /= np.max(carrier_envelopes, axis=0)
    modulator_envelopes /= np.max(modulator_envelopes, axis=0)

    # Flatten the carrier's magnitude spectrum
    flattened_carrier = carrier_magnitude / (carrier_envelopes + 1e-10)  # Avoid division by zero

    # Multiply by the modulator's spectral envelope
    cross_synthesized_magnitude = flattened_carrier * modulator_envelopes

    # Reconstruct the modified STFT using the original phase from the carrier
    cross_synthesized_stft = cross_synthesized_magnitude * np.exp(1j * np.angle(stft_carrier))

    # Inverse STFT to get the time-domain signal
    cross_synthesized_signal = librosa.istft(cross_synthesized_stft, hop_length=hop_size)
    output_file = os.path.join(output_dir, f'{filename_mod}___to___{filename_car}.wav')

    sf.write(output_file, cross_synthesized_signal, sr)
    print(f'Synthesized signal saved to as {output_file}')
    return output_file

