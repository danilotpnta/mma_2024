from pydub import AudioSegment
import logging

# Catch corrupted files into a txt file
logging.basicConfig(filename='conversion_errors.log', level=logging.ERROR)

def convert_mp3_to_wav(input_filename, output_filename):
    try:
        audio = AudioSegment.from_mp3(input_filename)
        audio.export(output_filename, format="wav")
    except Exception as e:
        error_message = f"Error converting {input_filename}: {e}"
        print(error_message)
        logging.error(error_message)
