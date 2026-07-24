import os
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSignal

class TwinEngine(QWebEngineView):
    traffic_signal = pyqtSignal(str, str, str) 

    def __init__(self):
        super().__init__()
        self.default_ua = self.page().profile().httpUserAgent()
        self.home_file_path = os.path.abspath("homepage.html")
        self.load_home()
        
        self.urlChanged.connect(self.on_url_changed)
        self.loadFinished.connect(self.on_load_finished)

    def load_home(self):
        if os.path.exists(self.home_file_path):
            self.setUrl(QUrl.fromLocalFile(self.home_file_path))
        else:
            self.setUrl(QUrl("https://www.google.com"))

    def set_custom_user_agent(self, user_agent):
        if user_agent:
            self.page().profile().setHttpUserAgent(user_agent)
        else:
            self.page().profile().setHttpUserAgent(self.default_ua)
        self.reload()

    def load_new_url(self, url_text):
        if url_text.startswith("file://") or "homepage.html" in url_text or url_text == "twin://startpage":
            self.load_home()
            return

        if not (url_text.startswith('http://') or url_text.startswith('https://')):
            url_text = 'https://' + url_text
        self.setUrl(QUrl(url_text))

    def on_url_changed(self, url):
        # URL එක load වෙන්න පටන් ගන්නා විට "GET" request එකක් ලෙස සලකමු
        self.traffic_signal.emit("GET", "Pending...", url.toString())

    def on_load_finished(self, success):
        status = "200 OK" if success else "Failed/Blocked"
        current_url = self.url().toString()
        # Load එක ඉවර වුණාම status එක යාවත්කාලීන කරනවා
        self.traffic_signal.emit("GET", status, current_url)