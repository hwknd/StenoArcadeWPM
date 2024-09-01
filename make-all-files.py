import os
import torch
import datetime
import random
from pydub import AudioSegment
from TTS.api import TTS
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

#! Set these variables
# Words per minute
wpm = 10
# Your song title and the name of all the files
thefilename = "practice01"


#! Script starts here
# other models might get better/worse results..
tts = TTS("tts_models/en/jenny/jenny", progress_bar=True).to(device)

textfile_path = "mytext.txt"
voices_dir = "source_voices"
output_dir = "output"
output_filename = f"{thefilename}.wav"  # Name for the final audio file
lrc_filename = f"{thefilename}.lrc"


# This function generate a random 800x800 px png file to use as album art in Steno Hero
def generate_random_gradient_image(size=(800, 800)):
    # Create a new image with RGBA mode
    img = Image.new("RGBA", size)
    width, height = size

    # Generate two random colors
    color1 = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        255,
    )
    color2 = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        255,
    )

    # Create the gradient
    for y in range(height):
        for x in range(width):
            # Calculate the interpolation factor between the two colors
            factor = (x / width + y / height) / 2
            r = int(color1[0] * (1 - factor) + color2[0] * factor)
            g = int(color1[1] * (1 - factor) + color2[1] * factor)
            b = int(color1[2] * (1 - factor) + color2[2] * factor)
            a = int(color1[3] * (1 - factor) + color2[3] * factor)
            img.putpixel((x, y), (r, g, b, a))

    return img


gradient_image = generate_random_gradient_image()
gradient_image.save(rf"output\{thefilename}.png")

# Load the text
with open(textfile_path, "r", encoding="utf-8") as file:
    text = file.read()

# Split text into words
words = text.split()

# Calculate the duration of the pause between words
pause_duration_ms = 60000 / wpm  # in milliseconds

# Initialize an empty AudioSegment for the final output
final_audio = AudioSegment.silent(duration=0)

# List to store timestamps for the .lrc file
timestamps = []
current_time_ms = 0

# Process each word separately
for word in words:
    try:
        # Convert the word to speech and save it to a temporary file
        temp_output_path = os.path.join(output_dir, "temp.wav")
        tts.tts_to_file(
            text=word,
            file_path=temp_output_path,
        )

        # Load the generated audio for the word
        word_audio = AudioSegment.from_wav(temp_output_path)

        # Add the word's audio to the final output
        final_audio += word_audio

        # Record the timestamp for the word
        timestamps.append((word, current_time_ms))

        # Update the current time
        current_time_ms += len(word_audio) + pause_duration_ms

        # Add the pause after the word
        final_audio += AudioSegment.silent(duration=pause_duration_ms)

    except ValueError as e:
        print(f"Error in text_to_speech for word '{word}': {e}")

# Define the output path
output_path = os.path.join(output_dir, output_filename)

# Export the final audio to the output file
final_audio.export(output_path, format="wav")

# Optionally, convert the WAV file to OGG
wav_audio = AudioSegment.from_wav(output_path)
ogg_output_path = os.path.join(output_dir, f"{thefilename}.ogg")
wav_audio.export(ogg_output_path, format="ogg")

# Generate the .lrc file
lrc_path = os.path.join(output_dir, lrc_filename)
with open(lrc_path, "w", encoding="utf-8") as lrc_file:
    lrc_file.write(f"[ti:PracticeWords]\n")
    lrc_file.write(f"[ar:Me]\n")
    lrc_file.write(f"[al:PracticeAlbum]\n")
    lrc_file.write(f"[art: Art\{thefilename}.png ]\n")
    lrc_file.write(f"[la:EN]\n")
    lrc_file.write(
        f"[length:{str(datetime.timedelta(milliseconds=current_time_ms))[:-3]}]\n"
    )
    lrc_file.write(f"[dif: 3]\n")
    lrc_file.write(f"[relyear: 2024]\n")
    lrc_file.write(f"[file:Audio\{thefilename}.ogg]\n\n")

    for word, timestamp in timestamps:
        minutes = timestamp // 60000
        seconds = (timestamp % 60000) // 1000
        milliseconds = (timestamp % 1000) // 10
        lrc_file.write(f"[{minutes:02}:{seconds:02}.{milliseconds:02}] {word}\n")

print("DONE!")
