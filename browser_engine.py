from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class TwinEngine(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setUrl(QUrl("https://www.google.com"))

    def load_new_url(self, url_text):
        if not url_text.startswith('http'):
            url_text = 'https://' + url_text
        self.setUrl(QUrl(url_text))