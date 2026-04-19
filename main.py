import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from browser_engine import TwinEngine
from ui_components import NavigationBar
from security_manager import SecurityManager

class TwinBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.engine = TwinEngine()
        self.security = SecurityManager()
        
        # Navigation bar එක සම්බන්ධ කිරීම
        self.nav_bar = NavigationBar(self.engine)
        
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