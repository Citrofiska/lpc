import datetime
from lpc_core import *
import lpc_config
import os
from concurrent.futures import ProcessPoolExecutor

def main(audio_files):
    # Create pairs of audio files
    pairs = [(audio_files[i], audio_files[j])
             for i in range(len(audio_files))
             for j in range(i + 1, len(audio_files))]

    # Process pairs in parallel
    with ProcessPoolExecutor() as executor:
        executor.map(lambda p: cross_synthesis(*p), pairs)

if __name__ == "__main__":
    time_start = datetime.datetime.now()

    # List of audio files (make sure to have 100 files in this list)
    audio_directory = "path/to/your/audio/files"
    audio_files = [os.path.join(audio_directory, f) for f in os.listdir(audio_directory) if f.endswith('.wav')]

    if len(audio_files) < 100:
        raise ValueError("Need at least 100 audio files.")

    main(audio_files[:100])  # Process the first 100 files

    time_end = datetime.datetime.now()

    print(f"iter: {i+1} | LPC order: {lpc_config.order} \n Start time: {time_start} "
          f"| End time: {time_end} | Total runtime: {(time_end - time_start).total_seconds()} seconds")