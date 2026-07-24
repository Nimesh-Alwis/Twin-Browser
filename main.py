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


VIVALDI_PURPLE_STYLE = """
QMainWindow {
    background-color: #140b24;
}

QWidget {
    background-color: #140b24;
    color: #f3e8ff;
    font-family: 'Segoe UI', 'Segoe UI Emoji', 'SF Pro Display', sans-serif;
    font-size: 13px;
}

/* Address Bar / Input Fields */
QLineEdit {
    background-color: #261642;
    border: 1px solid rgba(192, 132, 252, 0.35);
    border-radius: 16px;
    padding: 7px 16px;
    color: #f5e6ff;
    selection-background-color: #a855f7;
    font-size: 13px;
}

QLineEdit:focus {
    border: 1.5px solid #c084fc;
    background-color: #2f1b52;
}

/* Navigation & Action Buttons */
QPushButton {
    background-color: #23143c;
    border: 1px solid rgba(192, 132, 252, 0.25);
    border-radius: 10px;
    padding: 6px 14px;
    color: #e9d5ff;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #381c63;
    border: 1px solid #c084fc;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #a855f7;
    color: #140b24;
}

/* ComboBox Styling */
QComboBox {
    background-color: #23143c;
    border: 1px solid rgba(192, 132, 252, 0.25);
    border-radius: 10px;
    padding: 6px 12px;
    color: #e9d5ff;
    font-weight: 500;
}

QComboBox:hover {
    border: 1px solid #c084fc;
    background-color: #381c63;
}

QComboBox::drop-down {
    border: 0px;
    width: 20px;
}

QComboBox QAbstractItemView {
    background-color: #23143c;
    border: 1px solid #c084fc;
    selection-background-color: #a855f7;
    color: #f3e8ff;
    padding: 4px;
    border-radius: 8px;
}

/* Progress Bar */
QProgressBar {
    background-color: #1c1033;
    border: 1px solid rgba(192, 132, 252, 0.3);
    border-radius: 8px;
    text-align: center;
    color: #f3e8ff;
    height: 16px;
}

QProgressBar::chunk {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #a855f7, stop:1 #ec4899);
    border-radius: 7px;
}

/* Labels */
QLabel {
    color: #d8b4fe;
    font-weight: 500;
}

/* Message Boxes & Popups */
QMessageBox {
    background-color: #1c1033;
    color: #f3e8ff;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #140b24;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #3b1d66;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #a855f7;
}
"""

class TwinBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.engine = TwinEngine()
        self.security = SecurityManager()
        self.scanner = SiteScanner()
        
        self.nav_bar = NavigationBar(self.engine)
        
        self.nav_bar.scan_btn.clicked.connect(self.run_site_scan)
        self.nav_bar.game_btn.clicked.connect(self.start_snake_game)
        self.nav_bar.notes_btn.clicked.connect(self.open_editor)
        self.nav_bar.bookmark_btn.clicked.connect(self.add_bookmark)
        self.nav_bar.view_bookmarks_btn.clicked.connect(self.show_bookmarks)
        self.engine.traffic_signal.connect(self.log_traffic) 
        self.monitor = TrafficMonitor()
        self.nav_bar.traffic_btn.clicked.connect(self.monitor.show)
        self.nav_bar.home_btn.clicked.connect(self.go_home)
        self.nav_bar.download_btn.clicked.connect(self.start_video_download)
        self.p_bar = QProgressBar()
        self.speed_label = QLabel("Speed: 0 MB/s")
        self.p_bar.setVisible(False)
        self.speed_label.setVisible(False)
        
        self.setStyleSheet(VIVALDI_PURPLE_STYLE)

        try:
            self.nav_bar.address_bar.returnPressed.disconnect()
        except:
            pass
            
        self.nav_bar.address_bar.returnPressed.connect(self.secure_navigate)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.nav_bar)
        layout.addWidget(self.engine, stretch=1)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.p_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Twin-Browser Futuristic Edition v2.0")
        self.resize(1100, 750)

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