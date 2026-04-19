import sys # පද්ධතියේ පරාමිතීන් පාලනය කිරීමට
from PyQt6.QtWidgets import QApplication, QMainWindow # ප්‍රධාන ජනේලය සඳහා
from PyQt6.QtWebEngineWidgets import QWebEngineView # වෙබ් පිටුව පෙන්වීමට
from PyQt6.QtCore import QUrl # URL එක නිවැරදිව හඳුනා ගැනීමට

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. වෙබ් පෙන්වන එන්ජිම (The Engine)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        # 2. මේ එන්ජිම ජනේලය මැදට දැමීම
        self.setCentralWidget(self.browser)
        
        # 3. ජනේලයේ නම සහ විශාලත්වය
        self.setWindowTitle("Twin-Browser v1.0")
        self.resize(800, 600)

# App එක පණගැන්වීමේ පියවර
app = QApplication(sys.argv)
window = SimpleBrowser()
window.show()
sys.exit(app.exec())