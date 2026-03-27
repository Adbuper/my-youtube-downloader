from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Читаем твой HTML файл
def get_html():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('url')
        
        # Настройки скачивания
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloaded_video.mp4', # Временное имя файла
            'quiet': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Скачиваем видео на сервер
                ydl.download([video_url])
                
            # Отправляем скачанный файл пользователю
            return send_file('downloaded_video.mp4', as_attachment=True)
        except Exception as e:
            return f"Ошибка: {e}"
            
    return render_template_string(get_html())

if __name__ == '__main__':
    # Хостинг Render автоматически назначит порт через переменную PORT
    port = int(os.environ.get("PORT", 5000))
    # Мы запускаем сервер на 0.0.0.0, чтобы он был доступен извне
    app.run(host='0.0.0.0', port=port)