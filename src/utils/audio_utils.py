from pydub import AudioSegment

def convert_mp3_to_wav(input_filename, output_filename):
    audio = AudioSegment.from_mp3(input_filename)
    audio.export(output_filename, format="wav")