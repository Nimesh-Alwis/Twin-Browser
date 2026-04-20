import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from browser_engine import TwinEngine
from ui_components import NavigationBar
from security_manager import SecurityManager
from site_scanner import SiteScanner
from snake_game import SnakeGame
from text_editor import PayloadNotebook
from bookmark_manager import BookmarkManager



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


        try:
            self.nav_bar.address_bar.returnPressed.disconnect()
        except:
            pass
            
        self.nav_bar.address_bar.returnPressed.connect(self.secure_navigate)

        # Layout එක සැකසීම
        layout = QVBoxLayout()
        layout.addWidget(self.nav_bar)
        layout.addWidget(self.engine)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Twin-Browser Secure v1.5")
        self.resize(1000, 700)


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