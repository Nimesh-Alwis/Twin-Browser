import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                             QMessageBox, QProgressBar, QLabel, QTabWidget, QPushButton)
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from path_utils import get_data_path, get_resource_path
from browser_engine import TwinEngine
from ui_components import NavigationBar, ToolsSidebar
from security_manager import SecurityManager
from site_scanner import SiteScanner
from snake_game import SnakeGame
from text_editor import PayloadNotebook
from bookmark_manager import BookmarkManager
from traffic_monitor import TrafficMonitor
from video_downloader import DownloadThread
from subdomain_finder import SubdomainDialog
from theme_manager import ThemeManager, ThemeDialog
from ad_blocker import AdBlockerInterceptor
from download_manager import DownloadManagerWidget
from split_screen import SplitScreenWidget
from script_injector import ScriptInjectorWidget


class TwinBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TwinBrowser")
        icon_path = get_resource_path("twin.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Core Security & Managers
        self.security = SecurityManager()
        self.scanner = SiteScanner()
        self.monitor = TrafficMonitor()
        self.adblock_interceptor = AdBlockerInterceptor(enabled=True)
        self.download_manager = DownloadManagerWidget()

        # Left Collapsible Sidebar
        self.sidebar = ToolsSidebar()

        # Multi-Tab Widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Add New Tab Button (+)
        self.add_tab_btn = QPushButton("➕")
        self.add_tab_btn.setToolTip("Open New Tab")
        self.add_tab_btn.setStyleSheet("padding: 4px 10px; border-radius: 6px; font-weight: bold;")
        self.add_tab_btn.clicked.connect(lambda: self.add_new_tab())
        self.tab_widget.setCornerWidget(self.add_tab_btn)

        # Create initial tab
        self.add_new_tab()

        # Single Clean Navigation Bar
        self.nav_bar = NavigationBar(self.current_engine())
        
        # Connect tab change signal after nav_bar is created
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # Connect Sidebar Toggle Button
        self.nav_bar.sidebar_toggle_btn.clicked.connect(self.sidebar.toggle_sidebar)
        self.nav_bar.home_btn.clicked.connect(self.go_home)

        # Connect Sidebar Tools Action Buttons
        self.sidebar.adblock_btn.clicked.connect(self.toggle_adblocker)
        self.sidebar.split_view_btn.clicked.connect(self.open_split_screen)
        self.sidebar.incognito_btn.clicked.connect(lambda: self.add_new_tab(is_private=True))
        self.sidebar.script_injector_btn.clicked.connect(self.open_script_injector)
        self.sidebar.download_manager_btn.clicked.connect(self.open_download_manager)
        
        self.sidebar.scan_btn.clicked.connect(self.run_site_scan)
        self.sidebar.subdomain_btn.clicked.connect(self.run_subdomain_finder)
        self.sidebar.traffic_btn.clicked.connect(self.monitor.show)
        self.sidebar.notes_btn.clicked.connect(self.open_editor)
        self.sidebar.bookmark_btn.clicked.connect(self.add_bookmark)
        self.sidebar.view_bookmarks_btn.clicked.connect(self.show_bookmarks)
        self.sidebar.theme_btn.clicked.connect(self.open_theme_dialog)
        self.sidebar.download_btn.clicked.connect(self.start_video_download)
        self.sidebar.game_btn.clicked.connect(self.start_snake_game)
        
        self.p_bar = QProgressBar()
        self.speed_label = QLabel("Speed: 0 MB/s")
        self.p_bar.setVisible(False)
        self.speed_label.setVisible(False)
        
        # Load and Apply Saved Theme
        self.theme_config = ThemeManager.load_config()
        self.setStyleSheet(ThemeManager.generate_qss(self.theme_config))

        try:
            self.nav_bar.address_bar.returnPressed.disconnect()
        except Exception:
            pass
            
        self.nav_bar.address_bar.returnPressed.connect(self.secure_navigate)

        # Register Keyboard Shortcuts
        self.setup_keyboard_shortcuts()

        # Middle Split Area (Left Sidebar + Right Tab Widget)
        middle_layout = QHBoxLayout()
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.setSpacing(0)
        middle_layout.addWidget(self.sidebar)
        middle_layout.addWidget(self.tab_widget, stretch=1)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.nav_bar)
        layout.addLayout(middle_layout, stretch=1)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.p_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Twin-Browser Futuristic Edition v3.0")
        self.resize(1180, 800)

    def setup_keyboard_shortcuts(self):
        # Ctrl + T : New Tab
        QShortcut(QKeySequence("Ctrl+T"), self, lambda: self.add_new_tab())
        # Ctrl + W : Close Current Tab
        QShortcut(QKeySequence("Ctrl+W"), self, self.close_current_tab)
        # Ctrl + Shift + N : New Incognito Tab
        QShortcut(QKeySequence("Ctrl+Shift+N"), self, lambda: self.add_new_tab(is_private=True))
        # Ctrl + R / F5 : Reload Current Tab
        QShortcut(QKeySequence("Ctrl+R"), self, self.reload_current_tab)
        QShortcut(QKeySequence("F5"), self, self.reload_current_tab)
        # Ctrl + D : Bookmark Page
        QShortcut(QKeySequence("Ctrl+D"), self, self.add_bookmark)
        # Ctrl + J : Open Download Manager
        QShortcut(QKeySequence("Ctrl+J"), self, self.open_download_manager)
        # Ctrl + Alt + S : Open Split Screen View
        QShortcut(QKeySequence("Ctrl+Alt+S"), self, self.open_split_screen)

    def current_engine(self):
        widget = self.tab_widget.currentWidget()
        if isinstance(widget, TwinEngine):
            return widget
        return None

    def add_new_tab(self, url=None, is_private=False):
        engine = TwinEngine(main_window=self, is_private=is_private)
        engine.set_interceptor(self.adblock_interceptor)
        return self.add_tab_from_engine(engine, url=url, is_private=is_private)

    def add_tab_from_engine(self, engine, url=None, is_private=False):
        engine.traffic_signal.connect(self.log_traffic)
        
        tab_title = "🕵️ Incognito" if is_private else "New Tab"
        index = self.tab_widget.addTab(engine, tab_title)
        self.tab_widget.setCurrentIndex(index)

        # Update tab title dynamically when page title changes
        engine.titleChanged.connect(lambda title, e=engine, p=is_private: self.update_tab_title(e, title, p))

        if url:
            engine.load_new_url(url)

        return engine

    def update_tab_title(self, engine, title, is_private=False):
        idx = self.tab_widget.indexOf(engine)
        if idx != -1:
            prefix = "🕵️ " if is_private else ""
            clean_title = title if title and title != "about:blank" else "New Tab"
            if len(clean_title) > 22:
                clean_title = clean_title[:20] + "..."
            self.tab_widget.setTabText(idx, f"{prefix}{clean_title}")

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            widget = self.tab_widget.widget(index)
            self.tab_widget.removeTab(index)
            widget.deleteLater()
        else:
            engine = self.current_engine()
            if engine:
                engine.load_home()

    def close_current_tab(self):
        self.close_tab(self.tab_widget.currentIndex())

    def reload_current_tab(self):
        engine = self.current_engine()
        if engine:
            engine.reload()

    def toggle_adblocker(self):
        new_state = not self.adblock_interceptor.enabled
        self.adblock_interceptor.set_enabled(new_state)
        text = "🛡️ Ad-Blocker: ON" if new_state else "🛡️ Ad-Blocker: OFF"
        self.sidebar.adblock_btn.setText(text)
        status_msg = "Ad-Blocker Enabled!" if new_state else "Ad-Blocker Disabled!"
        QMessageBox.information(self, "Ad-Blocker", status_msg)

    def open_split_screen(self):
        split_widget = SplitScreenWidget(main_window=self)
        index = self.tab_widget.addTab(split_widget, "🖥️ Split View")
        self.tab_widget.setCurrentIndex(index)

    def open_script_injector(self):
        self.injector_view = ScriptInjectorWidget(main_window=self)
        self.injector_view.show()

    def open_download_manager(self):
        self.download_manager.load_history()
        self.download_manager.show()

    def on_tab_changed(self, index):
        engine = self.current_engine()
        if hasattr(self, 'nav_bar'):
            if engine:
                self.nav_bar.set_engine(engine)
                self.nav_bar.address_bar.setEnabled(True)
            else:
                self.nav_bar.address_bar.setText("twin://splitview")
                self.nav_bar.address_bar.setEnabled(False)

    def start_video_download(self):
        engine = self.current_engine()
        url = self.nav_bar.address_bar.text() if engine else ""
        quality = self.sidebar.quality_selector.currentText()

        if url:
            self.p_bar.setVisible(True)
            self.speed_label.setVisible(True)
            self.p_bar.setValue(0)
            
            self.download_worker = DownloadThread(url, quality)
            self.download_worker.progress_signal.connect(self.p_bar.setValue)
            self.download_worker.speed_signal.connect(self.speed_label.setText)
            self.download_worker.finished_signal.connect(lambda msg: self.on_download_finished(msg, url))
            self.download_worker.start()

    def on_download_finished(self, message, url):
        self.p_bar.setVisible(False)
        self.speed_label.setVisible(False)
        if "Finished" in message:
            download_dir = get_data_path("downloads")
            file_path = os.path.join(download_dir, "video.mp4")
            self.download_manager.add_record("Video Download", url, file_path, status="Completed")
        QMessageBox.information(self, "Twin-Browser", message)

    def go_home(self):
        engine = self.current_engine()
        if engine:
            self.nav_bar.address_bar.setText("twin://startpage")
            engine.load_home()

    def log_traffic(self, method, status, url):
        engine = self.current_engine()
        if engine and engine.is_private:
            return  # Do not log traffic for private tabs
        self.monitor.add_log(method, status, url)

    def open_editor(self):
        self.editor = PayloadNotebook()
        self.editor.show()

    def show_bookmarks(self):
        self.bookmark_view = BookmarkManager(self)
        self.bookmark_view.show()

    def add_bookmark(self):
        engine = self.current_engine()
        url = self.nav_bar.address_bar.text() if engine else ""
        if url and url != "twin://startpage" and not url.startswith("twin://"):
            with open(get_data_path("bookmarks.txt"), "a") as f:
                f.write(url + "\n")
            QMessageBox.information(self, "Success", "Page Bookmarked!")

    def start_snake_game(self):
        self.game_window = SnakeGame()
        self.game_window.show()

    def run_site_scan(self):
        current_url = self.nav_bar.address_bar.text()
        if current_url and current_url != "twin://startpage" and not current_url.startswith("twin://"):
            scan_report = self.scanner.scan(current_url)
            QMessageBox.information(self, "Site Scan Results", scan_report)
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid target URL first!")

    def open_theme_dialog(self):
        self.theme_dialog = ThemeDialog()
        self.theme_dialog.theme_updated_signal.connect(self.apply_theme)
        self.theme_dialog.show()

    def apply_theme(self, config_data):
        self.theme_config = config_data
        qss = ThemeManager.generate_qss(config_data)
        self.setStyleSheet(qss)
        engine = self.current_engine()
        if engine:
            engine.reload()

    def run_subdomain_finder(self):
        current_url = self.nav_bar.address_bar.text().strip()
        if current_url and current_url != "twin://startpage" and not current_url.startswith("twin://"):
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