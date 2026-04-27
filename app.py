from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

MUSIC_DIR = r'C:\Users\DELL\Music' 

@app.route('/')
def index():
    songs = []
    for root, dirs, files in os.walk(MUSIC_DIR):
        for file in files:
            if file.endswith(".mp3"):
                rel_path = os.path.relpath(os.path.join(root, file), MUSIC_DIR)
                songs.append(rel_path.replace("\\", "/"))
    return render_template('index.html', songs=songs)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(MUSIC_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))