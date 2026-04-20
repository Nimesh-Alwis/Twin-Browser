from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel

class BookmarkManager(QWidget):
    def __init__(self, browser_window):
        super().__init__()
        self.browser = browser_window
        self.setWindowTitle("My Bookmarks")
        self.resize(300, 400)

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