import os
import yt_dlp
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"success": False, "message": "Por favor, proporciona un enlace válido."}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioquality': 1,
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            mp3_filename = f"{info_dict['title']}.mp3"
            mp3_path = os.path.join(DOWNLOAD_FOLDER, mp3_filename)

            if os.path.exists(mp3_path):
                print(f"Archivo guardado en: {mp3_path}")
            else:
                print(f"Error: El archivo no se guardó en {mp3_path}")

        mp3_url = f"http://localhost:5001/downloads/{mp3_filename}"
        return jsonify({"success": True, "mp3Url": mp3_url})

    except Exception as e:
        print(f"Error al procesar el enlace: {e}")  # Aquí imprimimos el error para ayudar a la depuración
        return jsonify({"success": False, "message": f"Hubo un error: {str(e)}"}), 500

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
