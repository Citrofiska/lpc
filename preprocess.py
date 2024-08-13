# selecting audios form a given directory, with the following steps:
# trim long silence from the audio
# get the length of the trimmed audio
# only pick up the audios that are longer than 30 seconds
# rewrite the modified data as wav file

import os
import librosa
import soundfile as sf
from lpc_config import *

def preprocess_dir(dir, output_folder_name):
    # create a output folder
    preprocess_folder = f'data/preprocessed/{output_folder_name}/'
    os.makedirs(preprocess_folder, exist_ok=True)
    for file in os.listdir(dir):
        audio, _ = librosa.load(dir + file, sr=sr)
        audio, _ = librosa.effects.trim(audio, top_db=10)
        if len(audio) > 30*sr:
            # write the audio to the output dir with the original filename
            sf.write(preprocess_folder + file, audio, sr)
    return len(os.listdir(preprocess_folder))

if __name__ == "__main__":

    pred_car = preprocess_dir(car_dir, car_timb)
    pred_mod = preprocess_dir(mod_dir, mod_timb)
    print(f"Number of carrier files after preprocessing: {pred_car}")
    print(f"Number of modulator files after preprocessing: {pred_mod}")


