import yt_dlp
import os
from PyQt6.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            # 'downloads' folder එක නැත්නම් හදනවා
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.finished_signal.emit("Download Completed Successfully!")
        except Exception as e:
            self.finished_signal.emit(f"Error: {str(e)}")