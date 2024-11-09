from flask import Flask, request, jsonify
import os
from transformers import pipeline
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
from urllib.parse import quote as url_quote
import gdown
model_url = 'https://drive.google.com/drive/folders/10AQQEwlLg-DUEozX7be4DY8F4EKFzY8j?usp=sharing' 
output_path = 'Models/Summarisation_Model' 
gdown.download(model_url, output_path, quiet=False)


# Initialize Flask app
app = Flask(__name__)

# Initialize the summarizer
summarizer = pipeline("summarization")

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def convert_mp3_to_wav(mp3_file_path):
    wav_file_path = mp3_file_path.replace(".mp3", ".wav")
    try:
        audio = AudioSegment.from_mp3(mp3_file_path)
        audio.export(wav_file_path, format="wav")
        return wav_file_path
    except Exception as e:
        return None

def audio_to_text(audio_file_path):
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return ""

def summarize_text(text):
    if len(text.split()) > 0:
        summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    return "No content to summarize."

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("/tmp/summary.mp3")
    return "/tmp/summary.mp3"

@app.route('/')
def index():
    return "Welcome to the Speech-to-Text & Summarizer API!"

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    # Convert to WAV if it's MP3
    if file.filename.endswith('.mp3'):
        file_path = convert_mp3_to_wav(file_path)

    # Process the audio file
    text = audio_to_text(file_path)
    if text:
        summary = summarize_text(text)
        summary_audio_path = text_to_speech(summary)
        return jsonify({
            "summary": summary,
            "audio_summary": summary_audio_path
        })

    return jsonify({"error": "Failed to process audio"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  

if __name__ == '__main__':
    app.run(debug=True)
