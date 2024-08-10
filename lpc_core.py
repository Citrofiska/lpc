import numpy as np
import soundfile as sf # write signal to wav
import scipy.signal as signal
import librosa

def apply_lpc_to_stft(stft_carrier, stft_modulator, lpc_order, sr):

    n_frames = stft_carrier.shape[1]
    n_fft = stft_carrier.shape[0]
    modified_stft = np.zeros_like(stft_carrier, dtype=complex)

    for i in range(n_frames):
        modulator_frame = stft_modulator[:, i]
        carrier_frame = stft_carrier[:, i]

        # Apply LPC to the magnitude of the modulator frame
        magnitude_modulator = np.abs(modulator_frame)
        lpc_coeffs = librosa.lpc(magnitude_modulator, lpc_order)

        freqs, response = signal.freqz([1], lpc_coeffs, worN=n_fft, fs=sr)
        spectral_envelope = np.abs(response)

        # Apply the spectral envelope to the carrier frame
        modified_stft[:, i] = carrier_frame * spectral_envelope

    return modified_stft

def cross_synthesis(modulator_file, carrier_file, sr, output_dir, lpc_order, fft_size, hop_size):
    # Load the carrier and modulator signals
    carrier, _ = librosa.load(carrier_file, sr=sr)
    modulator, _ = librosa.load(modulator_file, sr=sr)
    min_length = min(len(carrier), len(modulator))
    # trim to the length of the shorter one
    carrier = carrier[:min_length]
    modulator = modulator[:min_length]
    print(f'Length of audios is {min_length}')

    # Compute the STFT of both signals
    stft_carrier = librosa.stft(carrier, n_fft=fft_size, hop_length=hop_size)
    stft_modulator = librosa.stft(modulator, n_fft=fft_size, hop_length=hop_size)

    # Apply the LPC coefficients of the modulator to the STFT of the carrier signal
    modified_stft = apply_lpc_to_stft(stft_carrier, stft_modulator, lpc_order, sr)

    # Perform ISTFT to get the synthesized signal
    synthesized_signal = librosa.istft(modified_stft, hop_length=hop_size)

    sf.write(output_dir, synthesized_signal, sr)

