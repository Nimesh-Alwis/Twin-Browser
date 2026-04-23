import yt_dlp
import os
from PyQt6.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    # progress (%), speed (MB/s), සහ අවසන් පණිවිඩය සඳහා signals
    progress_signal = pyqtSignal(float)
    speed_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str)

    def __init__(self, url, quality):
        super().__init__()
        self.url = url
        self.quality = quality # '720p', '1080p', හෝ 'best'

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # ප්‍රතිශතය ලබා ගැනීම
            p = d.get('_percent_str', '0%').replace('%','')
            # වේගය ලබා ගැනීම (MB/s)
            speed = d.get('_speed_str', '0MB/s')
            
            try:
                self.progress_signal.emit(float(p))
                self.speed_signal.emit(speed)
            except:
                pass

    def run(self):
        try:
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            # Quality එක අනුව format එක තීරණය කිරීම
            # 'bestvideo[height<=720]+bestaudio' වැනි format එකක් මෙහිදී භාවිතා වේ
            format_str = f'bestvideo[height<={self.quality.replace("p","")}]+bestaudio/best' if self.quality != "Best" else "best"

            ydl_opts = {
                'format': format_str,
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.finished_signal.emit("Download Finished!")
        except Exception as e:
            self.finished_signal.emit(f"Error: {str(e)}")