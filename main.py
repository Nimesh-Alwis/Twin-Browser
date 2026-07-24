import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QMessageBox, QProgressBar, QLabel, QTabWidget, QPushButton)
from browser_engine import TwinEngine
from ui_components import NavigationBar
from security_manager import SecurityManager
from site_scanner import SiteScanner
from snake_game import SnakeGame
from text_editor import PayloadNotebook
from bookmark_manager import BookmarkManager
from traffic_monitor import TrafficMonitor
from video_downloader import DownloadThread
from subdomain_finder import SubdomainDialog


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

/* Tab Widget & Tab Bar */
QTabWidget::pane {
    border: none;
    background-color: #140b24;
}

QTabBar::tab {
    background-color: #1c1033;
    color: #b8a2d1;
    border: 1px solid rgba(192, 132, 252, 0.15);
    border-bottom: none;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 7px 16px;
    min-width: 110px;
    max-width: 220px;
    margin-right: 3px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: #261642;
    color: #ffffff;
    font-weight: 600;
    border: 1px solid rgba(192, 132, 252, 0.4);
    border-bottom: 2.5px solid #a855f7;
}

QTabBar::tab:hover:!selected {
    background-color: #2b1747;
    color: #e9d5ff;
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

        self.security = SecurityManager()
        self.scanner = SiteScanner()
        self.monitor = TrafficMonitor()

        # Multi-Tab Widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # Add New Tab Button (+)
        self.add_tab_btn = QPushButton("➕")
        self.add_tab_btn.setToolTip("Open New Tab")
        self.add_tab_btn.setStyleSheet("padding: 4px 10px; border-radius: 6px; font-weight: bold;")
        self.add_tab_btn.clicked.connect(lambda: self.add_new_tab())
        self.tab_widget.setCornerWidget(self.add_tab_btn)

        # Create initial tab
        self.add_new_tab()

        # Navigation bar
        self.nav_bar = NavigationBar(self.current_engine())
        
        self.nav_bar.scan_btn.clicked.connect(self.run_site_scan)
        self.nav_bar.subdomain_btn.clicked.connect(self.run_subdomain_finder)
        self.nav_bar.game_btn.clicked.connect(self.start_snake_game)
        self.nav_bar.notes_btn.clicked.connect(self.open_editor)
        self.nav_bar.bookmark_btn.clicked.connect(self.add_bookmark)
        self.nav_bar.view_bookmarks_btn.clicked.connect(self.show_bookmarks)
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
        except Exception:
            pass
            
        self.nav_bar.address_bar.returnPressed.connect(self.secure_navigate)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.nav_bar)
        layout.addWidget(self.tab_widget, stretch=1)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.p_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Twin-Browser Futuristic Edition v2.0")
        self.resize(1100, 750)

    def current_engine(self):
        return self.tab_widget.currentWidget()

    def add_new_tab(self, url=None):
        engine = TwinEngine(main_window=self)
        return self.add_tab_from_engine(engine, url=url)

    def add_tab_from_engine(self, engine, url=None):
        engine.traffic_signal.connect(self.log_traffic)
        
        index = self.tab_widget.addTab(engine, "New Tab")
        self.tab_widget.setCurrentIndex(index)

        # Update tab title dynamically when page title changes
        engine.titleChanged.connect(lambda title, e=engine: self.update_tab_title(e, title))

        if url:
            engine.load_new_url(url)

        return engine

    def update_tab_title(self, engine, title):
        idx = self.tab_widget.indexOf(engine)
        if idx != -1:
            clean_title = title if title and title != "about:blank" else "New Tab"
            if len(clean_title) > 22:
                clean_title = clean_title[:20] + "..."
            self.tab_widget.setTabText(idx, clean_title)

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            engine = self.tab_widget.widget(index)
            self.tab_widget.removeTab(index)
            engine.deleteLater()
        else:
            # If it's the last tab, reset to startpage instead of closing window
            self.current_engine().load_home()

    def on_tab_changed(self, index):
        engine = self.current_engine()
        if engine:
            self.nav_bar.set_engine(engine)

    def start_video_download(self):
        engine = self.current_engine()
        url = self.nav_bar.address_bar.text() if engine else ""
        quality = self.nav_bar.quality_selector.currentText()

        if url:
            self.p_bar.setVisible(True)
            self.speed_label.setVisible(True)
            self.p_bar.setValue(0)
            
            self.download_worker = DownloadThread(url, quality)
            self.download_worker.progress_signal.connect(self.p_bar.setValue)
            self.download_worker.speed_signal.connect(self.speed_label.setText)
            self.download_worker.finished_signal.connect(self.on_download_finished)
            self.download_worker.start()

    def on_download_finished(self, message):
        self.p_bar.setVisible(False)
        self.speed_label.setVisible(False)
        QMessageBox.information(self, "Twin-Browser", message)

    def go_home(self):
        engine = self.current_engine()
        if engine:
            self.nav_bar.address_bar.setText("twin://startpage")
            engine.load_home()

    def log_traffic(self, method, status, url):
        self.monitor.add_log(method, status, url)

    def open_editor(self):
        self.editor = PayloadNotebook()
        self.editor.show()

    def show_bookmarks(self):
        self.bookmark_view = BookmarkManager(self)
        self.bookmark_view.show()

    def add_bookmark(self):
        url = self.nav_bar.address_bar.text()
        if url and url != "twin://startpage":
            with open("bookmarks.txt", "a") as f:
                f.write(url + "\n")
            QMessageBox.information(self, "Success", "Page Bookmarked!")

    def start_snake_game(self):
        self.game_window = SnakeGame()
        self.game_window.show()

    def run_site_scan(self):
        current_url = self.nav_bar.address_bar.text()
        if current_url and current_url != "twin://startpage":
            scan_report = self.scanner.scan(current_url)
            QMessageBox.information(self, "Site Scan Results", scan_report)
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid target URL first!")

    def run_subdomain_finder(self):
        current_url = self.nav_bar.address_bar.text().strip()
        if current_url and current_url != "twin://startpage":
            self.subdomain_view = SubdomainDialog(current_url)
            self.subdomain_view.show()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter or navigate to a target website first!")

    def secure_navigate(self):
        url = self.nav_bar.address_bar.text().strip()
        engine = self.current_engine()
        if not engine:
            return

        if not url or url == "twin://startpage" or "homepage.html" in url:
            self.nav_bar.address_bar.setText("twin://startpage")
            engine.load_home()
            return

        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url

        is_safe, reason = self.security.is_url_safe(url)
        
        if is_safe:
            engine.load_new_url(url)
        else:
            QMessageBox.warning(self, "Security Risk", f"Access Blocked: {reason}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TwinBrowser()
    window.show()
    sys.exit(app.exec())