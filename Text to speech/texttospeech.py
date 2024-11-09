import speech_recognition as sr
from transformers import pipeline
from pydub import AudioSegment
import os
from gtts import gTTS
from IPython.display import Audio

# Initialize the summarizer using Hugging Face pipeline
summarizer = pipeline("summarization")

# Save the summarizer model to a directory
model_save_path = "/content/summarization_model"
summarizer.save_pretrained(model_save_path)
print(f"Model saved at {model_save_path}")

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def convert_mp3_to_wav(mp3_file_path):
    """
    Convert MP3 file to WAV format using pydub.
    """
    wav_file_path = mp3_file_path.replace(".mp3", ".wav")
    try:
        # Load the MP3 file and export it as WAV
        audio = AudioSegment.from_mp3(mp3_file_path)
        audio.export(wav_file_path, format="wav")
        print(f"Converted MP3 to WAV: {wav_file_path}")
        return wav_file_path
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")
        return None

def audio_to_text(audio_file_path):
    """
    Convert audio file to text using SpeechRecognition library.
    """
    with sr.AudioFile(audio_file_path) as source:
        # Record the audio from the file
        audio_data = recognizer.record(source)
    
    try:
        # Convert audio to text using Google's speech-to-text
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio_data)
        print("Audio transcribed to text: ", text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def summarize_text(text):
    """
    Summarizes the provided text.
    """
    if len(text.split()) > 0:
        print("Summarizing text...")
        summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    else:
        return "No content to summarize."

def text_to_speech(text):
    """
    Convert text to speech using gTTS (Google Text-to-Speech).
    """
    tts = gTTS(text=text, lang='en')
    tts.save("/content/summary.mp3")
    print("Summary saved as audio.")
    return "/content/summary.mp3"

def play_audio(file_path):
    """
    Play the audio in the notebook.
    """
    return Audio(file_path)

def main(audio_file_path):
    """
    Main function to process the audio, convert it to text, summarize, and convert summary to speech.
    """
    # Step 1: Convert MP3 to WAV if the file is MP3
    if audio_file_path.endswith(".mp3"):
        wav_file_path = convert_mp3_to_wav(audio_file_path)
        if wav_file_path:
            audio_file_path = wav_file_path  # Update the path to the new WAV file
    
    # Step 2: Convert audio to text
    transcribed_text = audio_to_text(audio_file_path)
    
    if transcribed_text:
        # Step 3: Summarize the transcribed text
        summary = summarize_text(transcribed_text)
        print("Summary: ", summary)
        
        # Step 4: Convert the summary to speech
        summary_audio_path = text_to_speech(summary)
        
        # Play the audio of the summary in the notebook
        play_audio(summary_audio_path)
    else:
        print("No audio content to process.")

# Path to the audio file (MP3 or WAV)
audio_file_path = "/content/summary.mp3"  # Replace with your audio file path

# Run the main function
main(audio_file_path)
