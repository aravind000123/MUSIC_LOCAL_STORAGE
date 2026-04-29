from flask import Flask, render_template, send_from_directory, request
import os
from user_agents import parse

app = Flask(__name__)

MUSIC_DIR_PC = r'C:\Users\DELL'
MUSIC_DIR_MOBILE = r'storage/emulated'

def get_music_dir():
    ua = parse(request.headers.get('User-Agent', ''))
    if ua.is_mobile or ua.is_tablet:
        return MUSIC_DIR_MOBILE
    return MUSIC_DIR_PC

@app.route('/')
def index():
    MUSIC_DIR = get_music_dir()
    songs = []
    for root, dirs, files in os.walk(MUSIC_DIR):
        for file in files:
            if file.endswith(".mp3"):
                rel_path = os.path.relpath(os.path.join(root, file), MUSIC_DIR)
                songs.append(rel_path.replace("\\", "/"))
    return render_template('index.html', songs=songs)

@app.route('/download/<path:filename>')
def download_file(filename):
    MUSIC_DIR = get_music_dir()
    return send_from_directory(MUSIC_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))