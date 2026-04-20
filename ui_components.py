from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget

class NavigationBar(QWidget):
    def __init__(self, browser_engine):
        super().__init__()
        self.engine = browser_engine

        # 1. බොත්තම් සහ Address Bar එක නිර්මාණය කිරීම
        self.back_btn = QPushButton("<")
        self.forward_btn = QPushButton(">")
        self.reload_btn = QPushButton("R")
        self.scan_btn = QPushButton("Scan Site")
        self.game_btn = QPushButton("🎮 Game")
        self.bookmark_btn = QPushButton("⭐ Bookmark")
        self.notes_btn = QPushButton("📝 Notes")
        
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter URL here...")

        # 2. මූලික Navigation සඳහා වැඩ පැවරීම (Signals & Slots)
        self.back_btn.clicked.connect(self.engine.back)
        self.forward_btn.clicked.connect(self.engine.forward)
        self.reload_btn.clicked.connect(self.engine.reload)
        self.address_bar.returnPressed.connect(self.navigate)
        
        # සටහන: scan_btn සහ game_btn සම්බන්ධ කරන්නේ main.py එකෙනි.

        # 3. Layout එක සැකසීම (බොත්තම් පේළියට තැබීම)
        layout = QHBoxLayout()
        layout.addWidget(self.back_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.reload_btn)
        layout.addWidget(self.address_bar)
        layout.addWidget(self.scan_btn)
        layout.addWidget(self.game_btn) 
        layout.addWidget(self.bookmark_btn)
        layout.addWidget(self.notes_btn)
        
        self.setLayout(layout)

    def navigate(self):
        url = self.address_bar.text()
        # හිස් URL එකක් නම් navigate නොකර සිටීම හොඳ පුරුද්දකි
        if url.strip():
            self.engine.load_new_url(url)