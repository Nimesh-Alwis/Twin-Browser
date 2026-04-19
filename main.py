import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from browser_engine import TwinEngine
from ui_components import NavigationBar # නම වෙනස් වුණා මතක තබා ගන්න

class TwinBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.engine = TwinEngine()
        # මෙතැනදී අපි මුළු NavigationBar එකම කැඳවනවා
        self.nav_bar = NavigationBar(self.engine)

        layout = QVBoxLayout()
        layout.addWidget(self.nav_bar)
        layout.addWidget(self.engine)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Twin-Browser Navigation v1.3")
        self.resize(1000, 700)

app = QApplication(sys.argv)
window = TwinBrowser()
window.show()
sys.exit(app.exec())