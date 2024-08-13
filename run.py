# parallel processing of 10 pairs of audio files to do LPC cross-synthesis

import datetime
from lpc_core import *
from lpc_config import *
import os
from concurrent.futures import ProcessPoolExecutor

def main(file_names_1, file_names_2, pair_num):
    # Create pairs of audio files
    pairs = [(file_names_1[i], file_names_2[i]) for i in range(pair_num)]

    # Process pairs in parallel
    with ProcessPoolExecutor() as executor:
        futures = []
        for car_name, mod_name in pairs:
            futures.append(executor.submit(cross_synthesis, car_name, mod_name, sr, output_dir, order, fft_size, hop_size))

        # Wait for all tasks to complete
        for future in futures:
            future.result()

if __name__ == "__main__":
    time_start = datetime.datetime.now()

    # List of audio files (make sure to have 100 files in this list)
    car_names = os.listdir(car_dir)
    mod_names = os.listdir(mod_dir)
    print(f"Number of files in car_dir: {len(car_names)}")
    print(f"Number of files in mod_dir: {len(mod_names)}")

    main(car_names, mod_names, pair_num)  # Process the first 100 files

    time_end = datetime.datetime.now()

    print(f"LPC order: {order} \n Start time: {time_start} | End time: {time_end} "
          f"| Total runtime: {(time_end - time_start).total_seconds()} seconds")