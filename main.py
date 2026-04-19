import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView

class TwinBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. වෙබ් පෙන්වන එන්ජිම (The Engine)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        # 2. Address Bar එක හදා ගැනීම (QLineEdit පාවිච්චි කරලා)
        self.address_bar = QLineEdit()
        # Enter එබූ විට navigate_to_url කියන function එකට පණිවිඩයක් යවන්න
        self.address_bar.returnPressed.connect(self.navigate_to_url)

        # 3. Layout එක සැකසීම (Address bar එක උඩින් සහ Browser එක පල්ලෙහායින්)
        layout = QVBoxLayout()
        layout.addWidget(self.address_bar) # ඇඩ්‍රස් බාර් එක එකතු කිරීම
        layout.addWidget(self.browser)     # බ්‍රවුසර් එක එකතු කිරීම

        # 4. ප්‍රධාන container එක සාදා ජනේලයට සම්බන්ධ කිරීම
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Twin-Browser v1.1")
        self.resize(1000, 700)

    # User ඇඩ්‍රස් එකක් ටයිප් කරලා Enter ගැහුවම වැඩ කරන function එක
    def navigate_to_url(self):
        url_text = self.address_bar.text() # User ටයිප් කරපු එක ගන්නවා
        
        # Cybersecurity Tip: හැමවිටම https:// තියෙනවාද කියා පරීක්ෂා කිරීම
        if not url_text.startswith('http'):
            url_text = 'https://' + url_text
            
        self.browser.setUrl(QUrl(url_text)) # අලුත් වෙබ් අඩවිය load කරනවා

app = QApplication(sys.argv)
window = TwinBrowser()
window.show()
sys.exit(app.exec())