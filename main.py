import whisper
from pydub import AudioSegment
import io
import tempfile
import os

def split_on_silence(sound, min_silence_len=1000, silence_thresh=-40):
    len_sound = len(sound)
    silence_chunks = []
    prev_i = 0
    for i in range(1, len_sound):
        if sound[i:i+1].dBFS < silence_thresh and i - prev_i > min_silence_len:
            silence_chunks.append((prev_i, i))
            prev_i = i
    silence_chunks.append((prev_i, len_sound))
    return [sound[i[0]:i[1]] for i in silence_chunks]

def transcribe_podcast(podcast_audio_file):
    sound_file = AudioSegment.from_mp3(podcast_audio_file)
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
    print("\n")

transcribe_podcast(r"D:\Project\Podcast.mp3")
