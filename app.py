from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Имя временного файла для видео
output_filename = 'video_download.mp4'

# Функция для чтения твоего HTML
def get_html():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Файл index.html не найден! Проверьте, что он загружен на GitHub.</h3>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('url')
        
        # 1. Удаляем старый файл, если он остался от прошлых попыток
        if os.path.exists(output_filename):
            try:
                os.remove(output_filename)
            except:
                pass
        
        # 2. Настройки скачивания (Оптимизировано для бесплатного хостинга)
        ydl_opts = {
            # Берем лучший готовый MP4, чтобы серверу не нужно было ничего склеивать
            'format': 'best[ext=mp4]/best',
            'outtmpl': output_filename,
            'quiet': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

        # 3. Подключаем твои куки, если файл cookies.txt загружен на GitHub
        if os.path.exists('cookies.txt'):
            ydl_opts['cookiefile'] = 'cookies.txt'
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            # Если всё ок, отправляем файл тебе в браузер
            return send_file(output_filename, as_attachment=True)
            
        except Exception as e:
            # Если будет ошибка, ты увидишь её текст прямо на странице
            return f"<h2>Произошла ошибка:</h2><p>{str(e)}</p><a href='/'>Попробовать снова</a>"
            
    return render_template_string(get_html())

if __name__ == '__main__':
    # Эта часть обязательна для Render.com
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
