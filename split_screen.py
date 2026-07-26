from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QSplitter, QLabel)
from PyQt6.QtCore import Qt, QUrl
from browser_engine import TwinEngine

class SplitScreenWidget(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window

        # Header controls
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(8, 6, 8, 6)

        self.left_input = QLineEdit()
        self.left_input.setPlaceholderText("Left Window URL (e.g. google.com)...")
        self.left_input.returnPressed.connect(self.load_left)

        self.right_input = QLineEdit()
        self.right_input.setPlaceholderText("Right Window URL (e.g. github.com)...")
        self.right_input.returnPressed.connect(self.load_right)

        self.swap_btn = QPushButton("⇄ Swap Windows")
        self.swap_btn.setToolTip("Swap Left and Right Webpages")
        self.swap_btn.clicked.connect(self.swap_engines)

        header_layout.addWidget(QLabel("Left:"))
        header_layout.addWidget(self.left_input, stretch=1)
        header_layout.addWidget(self.swap_btn)
        header_layout.addWidget(QLabel("Right:"))
        header_layout.addWidget(self.right_input, stretch=1)

        # Create dual engines
        self.left_engine = TwinEngine(main_window=self.main_window)
        self.right_engine = TwinEngine(main_window=self.main_window)

        self.left_engine.urlChanged.connect(lambda qurl: self.left_input.setText(qurl.toString()))
        self.right_engine.urlChanged.connect(lambda qurl: self.right_input.setText(qurl.toString()))

        # Splitter to hold both views
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.left_engine)
        self.splitter.addWidget(self.right_engine)
        self.splitter.setSizes([500, 500])

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.addLayout(header_layout)
        layout.addWidget(self.splitter, stretch=1)

        self.setLayout(layout)

    def load_left(self):
        url = self.left_input.text().strip()
        if url:
            self.left_engine.load_new_url(url)

    def load_right(self):
        url = self.right_input.text().strip()
        if url:
            self.right_engine.load_new_url(url)

    def swap_engines(self):
        left_url = self.left_engine.url().toString()
        right_url = self.right_engine.url().toString()
        if left_url and right_url:
            self.left_engine.load_new_url(right_url)
            self.right_engine.load_new_url(left_url)
