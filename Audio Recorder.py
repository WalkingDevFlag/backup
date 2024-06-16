import pyaudio
import wave
from moviepy.editor import AudioFileClip

# Initialize PyAudio (1)
p = pyaudio.PyAudio()

# Open a stream (2)
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                input=False,
                frames_per_buffer=1024)

# Read the data (3)
data = stream.read(1024)

# Save the data as WAV file (4)
with wave.open('output.wav', 'wb') as f:
    f.setnchannels(2)
    f.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    f.setframerate(44100)
    f.writeframes(data)

# Convert WAV to MP4 using moviepy (5)
audio_clip = AudioFileClip("output.wav")
audio_clip.write_videofile("output.mp4", codec='libx264', fps=44100)

# Close the stream (6)
stream.stop_stream()
stream.close()
p.terminate()
