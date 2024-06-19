import whisper
from pydub import AudioSegment

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
        if i < 10 or i > count - 10:
            out_file = "chunk{0}.wav".format(i)
            print("\r\nExporting >>", out_file, " - ", i, "/", count)
            chunk.export(out_file, format="wav")
            result = model.transcribe(out_file)
            transcriptChunk = result["text"]
            print(transcriptChunk)

            transcript += " " + transcriptChunk

    print("Transcript: \n")
    print(transcript)
    print("\n")

transcribe_podcast("path/to/podcast.mp3")
