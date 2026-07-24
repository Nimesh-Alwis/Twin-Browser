from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel

class BookmarkManager(QWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser = browser_window
        self.setWindowTitle("My Bookmarks")
        self.resize(360, 450)

        self.setStyleSheet("""
            QWidget {
                background-color: #140b24;
                color: #f3e8ff;
                font-family: 'Segoe UI', sans-serif;
            }
            QListWidget {
                background-color: #201138;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 10px;
                padding: 6px;
                color: #f3e8ff;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 6px;
            }
            QListWidget::item:hover {
                background-color: #351a5c;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #a855f7;
                color: #140b24;
                font-weight: bold;
            }
            QLabel {
                color: #c084fc;
                font-weight: 600;
                font-size: 13px;
                margin-bottom: 4px;
            }
        """)

        self.list_widget = QListWidget()
        self.load_bookmarks()

        # ලින්ක් එකක් double click කළොත් ඒකට යන්න
        self.list_widget.itemDoubleClicked.connect(self.open_bookmark)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Double-click to open a bookmark:"))
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def load_bookmarks(self):
        try:
            with open("bookmarks.txt", "r") as f:
                for line in f:
                    self.list_widget.addItem(line.strip())
        except FileNotFoundError:
            self.list_widget.addItem("No bookmarks found yet.")

    def open_bookmark(self, item):
        url = item.text()
        self.browser.nav_bar.address_bar.setText(url)
        self.browser.secure_navigate() # අපේ ආරක්ෂිත navigation එක පාවිච්චි කරමු
        self.close()