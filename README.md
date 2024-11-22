# Podcast Transcription with Whisper

This project leverages the Whisper model by OpenAI to transcribe podcasts from audio or video files (MP3 or MP4). It also includes functionality to convert MP4 video files into MP3 audio files, allowing the transcription process to work seamlessly regardless of the file format.

## Features

- **Audio File Support:** Transcribe both MP3 and MP4 files.
- **Silence Chunking:** Split long audio files into smaller chunks based on periods of silence for more accurate transcription.
- **Whisper Model Integration:** Uses OpenAI's Whisper model for automatic speech recognition (ASR) and transcription.
- **MP4 to MP3 Conversion:** Converts MP4 video files into MP3 audio files using FFmpeg before transcription.
- **Temporary File Handling:** Processes audio chunks and cleans up temporary files automatically.

## Requirements

Before running the script, make sure you have the following:

1. **Python 3.x** installed on your system.
2. **Whisper** installed via `pip`:
   
   pip install openai-whisper
  
3. **pydub** installed for audio processing:
   
   pip install pydub
   
4. **FFmpeg** installed on your system for video-to-audio conversion:
   - [Download FFmpeg](https://ffmpeg.org/download.html) or install it via a package manager.
     - For Windows, add FFmpeg to your system’s PATH variable for easier command-line access.
     - For MacOS: `brew install ffmpeg`
     - For Ubuntu/Linux: `sudo apt install ffmpeg`

## Setup

1. Clone this repository to your local machine:
   
   git clone https://github.com/your-username/podcast-transcription-whisper.git
   cd podcast-transcription-whisper
   

2. Install the required Python libraries:
   
   pip install -r requirements.txt
   

   *If you don't have a `requirements.txt` file, run the following commands instead:*
   
   pip install openai-whisper pydub
   

3. **FFmpeg Setup:**
   - Ensure that FFmpeg is correctly installed on your machine and accessible from the command line (use `ffmpeg -version` to verify).
   - If FFmpeg is not in your system's `PATH`, provide the full path to the `ffmpeg` binary in the code by modifying the `subprocess.run()` call.

## Usage

1. Place your podcast audio or video file (MP3 or MP4) in the directory where you want to process it.

2. Run the script with the path to your audio or video file:
   
   python main.py "path_to_your_file.mp4"  # or .mp3
   

   If the input file is an MP4 video, it will be converted into an MP3 audio file before transcription.

3. The script will:
   - Convert MP4 files to MP3 (if applicable).
   - Split long audio into chunks based on silence.
   - Transcribe each chunk using Whisper.
   - Output the full transcript.

## Example

If you have a podcast video (`podcast.mp4`), run the following command:


python main.py "podcast.mp4"


This will convert the video to an MP3 file (if it’s an MP4), split it into chunks, and transcribe it using Whisper. The full transcript will be printed on the console.

## Output

The transcript will be printed in the terminal, showing each chunk as it is transcribed. At the end of the process, the full transcript will be displayed.

### Example Output:


Converting video podcast.mp4 to MP3...
Conversion complete: podcast1.mp3
Audio split into 10 audio chunks

Chunk 1/10 transcribed: Hello, welcome to today's podcast.
Chunk 2/10 transcribed: Today we will be discussing...
...
Chunk 10/10 transcribed: Thank you for listening to the end.

Full Transcript: 
Hello, welcome to today's podcast. Today we will be discussing... Thank you for listening to the end.


## Notes

- **Audio Quality:** The transcription quality depends on the clarity of the audio. Whisper performs well on clear speech but may struggle with background noise or heavy accents.
- **Silence Chunking:** Silence detection is configurable. You can adjust `min_silence_len` (minimum silence duration) and `silence_thresh` (threshold for silence detection) in the `split_on_silence` function for optimal performance on different podcasts.
- **Performance:** Processing large audio files might take time depending on the system's resources. Consider using Whisper's `small` or `tiny` models if speed is a priority.

## Acknowledgments

- [Whisper by OpenAI](https://github.com/openai/whisper) for providing the ASR model.
- [FFmpeg](https://ffmpeg.org/) for audio/video conversion.
- [PyDub](https://pydub.com/) for audio processing.
