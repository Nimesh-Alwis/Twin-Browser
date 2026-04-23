import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox, QProgressBar, QLabel
from browser_engine import TwinEngine
from ui_components import NavigationBar
from security_manager import SecurityManager
from site_scanner import SiteScanner
from snake_game import SnakeGame
from text_editor import PayloadNotebook
from bookmark_manager import BookmarkManager
from traffic_monitor import TrafficMonitor
from video_downloader import DownloadThread


CYBERPUNK_STYLE = """
QMainWindow {
    background-color: #0f1117; /* Softer dark */
}

QWidget {
    background-color: #0f1117;
    color: #c9d1d9; /* Soft light gray instead of harsh green */
    font-family: 'Segoe UI', 'Courier New', monospace;
    font-size: 14px;
}

/* Input Fields */
QLineEdit {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px;
    color: #58a6ff; /* Soft blue */
}

QLineEdit:focus {
    border: 1px solid #58a6ff;
    background-color: #1c2128;
}

/* Buttons */
QPushButton {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 8px 15px;
    color: #58a6ff;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #21262d;
    border: 1px solid #58a6ff;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #58a6ff;
    color: #0f1117;
}

/* Lists, Text Areas & Combo Box */
QListWidget, QTextEdit, QComboBox {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #c9d1d9;
}

/* Labels */
QLabel {
    color: #8b949e; /* softer than pink */
    font-weight: 500;
}
"""

class TwinBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.engine = TwinEngine()
        self.security = SecurityManager()
        self.scanner = SiteScanner() # 2. Scanner එක පණගන්වන්න
        # Navigation bar එක සම්බන්ධ කිරීම
        self.nav_bar = NavigationBar(self.engine)
        
        self.nav_bar.scan_btn.clicked.connect(self.run_site_scan)
        self.nav_bar.game_btn.clicked.connect(self.start_snake_game) # Game බොත්තම සම්බන්ධ කිරීම
        
        # පරණ Connection එක අයින් කර අලුත් එක (secure_navigate) සම්බන්ධ කිරීම
        self.nav_bar.notes_btn.clicked.connect(self.open_editor)
        self.nav_bar.bookmark_btn.clicked.connect(self.add_bookmark)
        self.nav_bar.view_bookmarks_btn.clicked.connect(self.show_bookmarks)
        self.engine.traffic_signal.connect(self.log_traffic) 
        self.monitor = TrafficMonitor() # මේ පේළිය අනිවාර්යයෙන්ම ඕනේ
        self.nav_bar.traffic_btn.clicked.connect(self.monitor.show)
        self.nav_bar.home_btn.clicked.connect(self.go_home)
        self.nav_bar.download_btn.clicked.connect(self.start_video_download)
        self.p_bar = QProgressBar()
        self.speed_label = QLabel("Speed: 0 MB/s")
        self.p_bar.setVisible(False) # සාමාන්‍ය වෙලාවට පේන්නෙ නැහැ
        # ... (අනිත් කේතයන්) ...
        self.setStyleSheet(CYBERPUNK_STYLE)

        try:
            self.nav_bar.address_bar.returnPressed.disconnect()
        except:
            pass
            
        self.nav_bar.address_bar.returnPressed.connect(self.secure_navigate)

        # Layout එක සැකසීම
        layout = QVBoxLayout()
        layout.addWidget(self.nav_bar)
        layout.addWidget(self.engine)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.p_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Twin-Browser Secure v1.5")
        self.resize(1000, 700)

    def start_video_download(self):
        url = self.nav_bar.address_bar.text()
        quality = self.nav_bar.quality_selector.currentText() # User තේරූ quality එක

        if url:
            self.p_bar.setVisible(True)
            self.speed_label.setVisible(True)
            self.p_bar.setValue(0)
            
            self.download_worker = DownloadThread(url, quality)
            
            # Signals සම්බන්ධ කිරීම
            self.download_worker.progress_signal.connect(self.p_bar.setValue)
            self.download_worker.speed_signal.connect(self.speed_label.setText)
            self.download_worker.finished_signal.connect(self.on_download_finished)
            
            self.download_worker.start()

    def on_download_finished(self, message):
        self.p_bar.setVisible(False)
        self.speed_label.setVisible(False)
        QMessageBox.information(self, "Twin-Browser", message)

    def go_home(self):
        home_url = "https://www.google.com" # ඔයා කැමති Home පිටුව මෙතැනට දෙන්න
        self.nav_bar.address_bar.setText(home_url)
        self.engine.load_new_url(home_url)

    def log_traffic(self, method, status, url):
        self.monitor.add_log(method, status, url)

    def open_editor(self):
        self.editor = PayloadNotebook()
        self.editor.show()

    def show_bookmarks(self):
        # Bookmark Manager එක විවෘත කිරීම
        self.bookmark_view = BookmarkManager(self)
        self.bookmark_view.show()

    def add_bookmark(self):
        url = self.nav_bar.address_bar.text()
        if url:
            with open("bookmarks.txt", "a") as f:
                f.write(url + "\n")
            QMessageBox.information(self, "Success", "Page Bookmarked!")

    # 3. Snake Game එක පණගන්වන Function එක
    def start_snake_game(self):
        # Game එක අලුත් Window එකක් ලෙස විවෘත කිරීම
        self.game_window = SnakeGame()
        self.game_window.show()

    # 4. ස්කෑන් එක සිදු කරන අලුත් Function එක
    def run_site_scan(self):
        # දැනට address bar එකේ තියෙන URL එක ගන්නවා
        current_url = self.nav_bar.address_bar.text()
        
        if current_url:
            # ස්කෑන් එක කරලා report එකක් ගන්නවා
            scan_report = self.scanner.scan(current_url)
            
            # ප්‍රතිඵලය Popup window එකකින් පෙන්වනවා
            QMessageBox.information(self, "Site Scan Results", scan_report)
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a URL first!")

    # මේ function එක Class එක ඇතුළත (Indented) තිබිය යුතුමයි
    def secure_navigate(self):
        url = self.nav_bar.address_bar.text()
        
        # URL එකේ Protocol එක පරීක්ෂාව
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url

        is_safe, reason = self.security.is_url_safe(url)
        
        if is_safe:
            self.engine.load_new_url(url)
        else:
            QMessageBox.warning(self, "Security Risk", f"Access Blocked: {reason}")


# මෙතැන් සිට පේළි Class එකෙන් පිටත (වම් පැත්තටම හේත්තු වී) තිබිය යුතුයි
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TwinBrowser()
    window.show()
    sys.exit(app.exec())