from lpc_core import *

car_names = os.listdir(car_dir)
mod_names = os.listdir(mod_dir)

pairs = [(car_names[i], mod_names[i]) for i in range(10)]

synthesized_name = cross_synthesis(pairs[3][0], pairs[3][1], sr, output_dir, order, fft_size, hop_size)
cs, _ = librosa.load(synthesized_name, sr=sr)