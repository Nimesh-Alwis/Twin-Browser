import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from browser_engine import TwinEngine
from ui_components import NavigationBar
from security_manager import SecurityManager
from site_scanner import SiteScanner


class TwinBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.engine = TwinEngine()
        self.security = SecurityManager()
        self.scanner = SiteScanner() # 2. Scanner එක පණගන්වන්න
        # Navigation bar එක සම්බන්ධ කිරීම
        self.nav_bar = NavigationBar(self.engine)
        
        self.nav_bar.scan_btn.clicked.connect(self.run_site_scan)

        # පරණ Connection එක අයින් කර අලුත් එක (secure_navigate) සම්බන්ධ කිරීම
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

        self.setWindowTitle("Twin-Browser Secure v1.4")
        self.resize(1000, 700)

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