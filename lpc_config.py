sr = 44100
fft_size = 1024
hop_size = 512
order = round(fft_size * 0.3)
pair_num = 10  # Number of pairs to process in parallel

# Instruments: Drum, Guitar, Violin, Piano
car_timb = 'Piano'
mod_timb = 'Violin'

car_dir = f"data/preprocessed/{car_timb}/"
mod_dir = f"data/preprocessed/{mod_timb}/"
output_dir = "data/output/"

