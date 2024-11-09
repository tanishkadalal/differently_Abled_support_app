from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from pydub import AudioSegment
import speech_recognition as sr
from transformers import pipeline
from gtts import gTTS

# Initialize the Flask app
app = Flask(__name__)

# Path for saving uploaded audio files
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

# Initialize the summarizer using Hugging Face pipeline
summarizer = pipeline("summarization")

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """
    Check if the uploaded file is allowed.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_mp3_to_wav(mp3_file_path):
    """
    Convert MP3 file to WAV format using pydub.
    """
    wav_file_path = mp3_file_path.replace(".mp3", ".wav")
    try:
        # Load the MP3 file and export it as WAV
        audio = AudioSegment.from_mp3(mp3_file_path)
        audio.export(wav_file_path, format="wav")
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
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return ""

def summarize_text(text):
    """
    Summarizes the provided text.
    """
    if len(text.split()) > 0:
        summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    else:
        return "No content to summarize."

def text_to_speech(text):
    """
    Convert text to speech using gTTS (Google Text-to-Speech).
    """
    tts = gTTS(text=text, lang='en')
    output_file = os.path.join(UPLOAD_FOLDER, "summary.mp3")
    tts.save(output_file)
    return output_file

@app.route('/')
def index():
    return "Welcome to the Speech to Text & Summarizer API!"

@app.route('/process_audio', methods=['POST'])
def process_audio():
    """
    Endpoint to process the uploaded audio file, convert to text, summarize, and convert summary to speech.
    """
    # Check if a file was uploaded
    if 'audio' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['audio']

    # If the user does not select a file or selects a non-allowed file type
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type, only mp3 and wav allowed"}), 400

    # Secure the file name and save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # If the uploaded file is MP3, convert it to WAV
    if file_path.endswith(".mp3"):
        wav_file_path = convert_mp3_to_wav(file_path)
        if wav_file_path:
            file_path = wav_file_path  # Update the path to the new WAV file

    # Step 1: Convert audio to text
    transcribed_text = audio_to_text(file_path)
    
    if transcribed_text:
        # Step 2: Summarize the transcribed text
        summary = summarize_text(transcribed_text)
        
        # Step 3: Convert the summary to speech
        summary_audio_path = text_to_speech(summary)

        # Step 4: Return the audio file of the summary
        return send_file(summary_audio_path, as_attachment=True)

    else:
        return jsonify({"error": "No speech detected in the audio file"}), 400

if __name__ == "__main__":
    app.run(debug=True)
