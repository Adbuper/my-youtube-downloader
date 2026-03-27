from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

output_filename = 'video_download.mp4'

def get_html():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Файл index.html не найден!</h3>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('url')
        
        if os.path.exists(output_filename):
            try: os.remove(output_filename)
            except: pass
        
        # САМЫЕ ГИБКИЕ НАСТРОЙКИ
        ydl_opts = {
            # 'b' выберет лучший файл, который уже содержит и видео, и звук вместе
            'format': 'b', 
            'outtmpl': output_filename,
            'quiet': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

        if os.path.exists('cookies.txt'):
            ydl_opts['cookiefile'] = 'cookies.txt'
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            return send_file(output_filename, as_attachment=True)
        except Exception as e:
            # Выводим подробную ошибку, если что-то пойдет не так
            return f"<h2>Ошибка:</h2><p>{str(e)}</p><a href='/'>Назад</a>"
            
    return render_template_string(get_html())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
