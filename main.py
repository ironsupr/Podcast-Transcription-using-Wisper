#import modules
import whisper
from pydub import AudioSegment
import io
import tempfile
import os
import subprocess


# Function to check if the file is a video and convert to MP3 if it is
def convert_video_to_mp3(input_file):
    # Check if the file is an MP4 video file
    if input_file.lower().endswith('.mp4'):
        mp3_file = input_file.rsplit('.', 1)[0] + "_audio.mp3"
        print(f"Converting video {input_file} to MP3...")

        # Run FFmpeg to extract audio as MP3
        subprocess.run(["ffmpeg", "-i", input_file, "-q:a", "0", "-map", "a", mp3_file], check=True)
        print(f"Conversion complete: {mp3_file}")
        return mp3_file
    else:
        return input_file  # If the file is already an MP3, return the same file


def split_on_silence(sound, min_silence_len=1000, silence_thresh=-40):
    len_sound = len(sound)
    silence_chunks = []
    prev_i = 0
    for i in range(1, len_sound):
        if sound[i:i + 1].dBFS < silence_thresh and i - prev_i > min_silence_len:
            silence_chunks.append((prev_i, i))
            prev_i = i
    silence_chunks.append((prev_i, len_sound))
    return [sound[i[0]:i[1]] for i in silence_chunks]


def transcribe_podcast(podcast_audio_file, output_text_file):
    # Check if input file is a video, convert to MP3 if necessary
    audio_file = convert_video_to_mp3(podcast_audio_file)

    sound_file = AudioSegment.from_mp3(audio_file)
    audio_chunks = split_on_silence(sound_file, min_silence_len=1000, silence_thresh=-40)
    count = len(audio_chunks)
    print("Audio split into " + str(count) + " audio chunks \n")

    model = whisper.load_model("base")
    transcript = ""

    for i, chunk in enumerate(audio_chunks):
        # Process all chunks instead of just the first and last 10
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            chunk.export(tmp_file.name, format="wav")  # Save chunk as a temp file
            tmp_file.close()  # Close the file so Whisper can access it

            # Load the audio from the temporary file using whisper's internal loader
            result = model.transcribe(tmp_file.name)
            transcriptChunk = result["text"]
            print(f"Chunk {i + 1}/{count} transcribed: {transcriptChunk}")

            transcript += " " + transcriptChunk

            # Clean up the temporary file after processing
            os.remove(tmp_file.name)

    print("Full Transcript: \n")
    print(transcript)
    # Save the full transcript to a text file with UTF-8 encoding
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Full Transcript saved to: {output_text_file}")
    print("\n")


# Example usage: Provide the input MP4 or MP3 file path and the desired output text file path
transcribe_podcast(r"D:\Project\Podcast.mp3", r"D:\Project\transcription.txt")
