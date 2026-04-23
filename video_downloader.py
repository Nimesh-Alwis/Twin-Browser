import yt_dlp
import os
from PyQt6.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    # progress එක (percentage) යැවීමට අලුත් signal එකක්
    progress_signal = pyqtSignal(float)
    finished_signal = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # දැනට download වී ඇති ප්‍රතිශතය ගණනය කිරීම
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                self.progress_signal.emit(float(p))
            except:
                pass

    def run(self):
        try:
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook], # Hook එක සම්බන්ධ කිරීම
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.finished_signal.emit("Successfully Downloaded!")
        except Exception as e:
            self.finished_signal.emit(f"Error: {str(e)}")