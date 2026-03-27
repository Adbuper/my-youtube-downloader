from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Читаем твой HTML файл
def get_html():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "Файл index.html не найден!"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('url')
        output_filename = 'video_download.mp4'
        
        # Удаляем старый файл, если он остался от прошлого скачивания
        if os.path.exists(output_filename):
            os.remove(output_filename)
        
        # Настройки скачивания с использованием куки для обхода блокировки
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_filename,
            'quiet': True,
            'cookiefile': 'cookies.txt', # Имя файла с твоими куками
            'nocheckcertificate': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                
            return send_file(output_filename, as_attachment=True)
        except Exception as e:
            return f"Ошибка скачивания: {e}. Убедитесь, что файл cookies.txt загружен на сервер."
            
    return render_template_string(get_html())

if __name__ == '__main__':
    # Настройка порта для Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
