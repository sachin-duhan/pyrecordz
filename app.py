import cv2
import numpy as np
import pyaudio
import wave
import threading
from moviepy.editor import AudioFileClip, VideoClip, VideoFileClip
import os
import pyautogui

# Define resolution and framerate
SCREEN_SIZE = (640, 480)
FPS = 30.0

# Define audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10

# Define video output settings
VIDEO_NAME = "output.mp4"
VIDEO_CODEC = "libx264"
VIDEO_FPS = FPS

# Initialize audio recording
audio_frames = []

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE,
        input=True, frames_per_buffer=CHUNK
    )

    while True:
        data = stream.read(CHUNK)
        audio_frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

audio_thread = threading.Thread(target=record_audio)
audio_thread.start()

def get_frames():
    while True:
        # Take screenshot using PyAutoGUI
        img = pyautogui.screenshot()
        # Convert the screenshot to a numpy array
        frame = np.array(img)
        # Convert color space from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Resize the frame to the specified resolution
        frame = cv2.resize(frame, SCREEN_SIZE)
        yield frame

# Initialize the video clip
video = VideoClip(lambda t: get_frames()[(t * FPS) % RECORD_SECONDS], duration=RECORD_SECONDS)

# Save the video clip to a file
video.write_videofile(VIDEO_NAME, fps=VIDEO_FPS, codec=VIDEO_CODEC)

# Release the audio recording thread
audio_thread.join()

# Save the recorded audio to a WAV file
audio_data = b"".join(audio_frames)
with wave.open("audio.wav", "wb") as wavfile:
    wavfile.setnchannels(CHANNELS)
    wavfile.setsampwidth(pyaudio.get_sample_size(FORMAT))
    wavfile.setframerate(RATE)
    wavfile.writeframes(audio_data)

# Load the video and audio files and concatenate them
video = VideoFileClip(VIDEO_NAME)
audio = AudioFileClip("audio.wav")
final = video.set_audio(audio)
final.write_videofile(VIDEO_NAME, codec=VIDEO_CODEC, fps=VIDEO_FPS)

# Delete the temporary audio file
print("hello cutie, 1 2 3 4 5")
os.remove("audio.wav")
