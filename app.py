from flask import Flask, render_template, request, send_file
import pytesseract
from PIL import Image
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/read', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['image']
        language = request.form['language']
        img = Image.open(image)
        text = pytesseract.image_to_string(img, lang=language)
        print(f"el texto es: {text}")
        return render_template('result.html', text=text, lang=language)
    return render_template('read.html')

@app.route('/text_to_speech/<text>/<lang>')
def text_to_speech(text, lang):
    if lang == "eng":
        tts = gTTS(text, lang="en", tld="us")
    elif lang == "jpn":
        tts = gTTS(text, lang="ja")
    elif lang == "spa":
        tts = gTTS(text, lang="es", tld="com.mx")
    audio_file = 'speech.mp3'
    tts.save(audio_file)
    return send_file(audio_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)