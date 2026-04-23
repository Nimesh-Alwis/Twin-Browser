from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget, QComboBox

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
        self.view_bookmarks_btn = QPushButton("📂 View Bookmarks")
        self.home_btn = QPushButton("🏠 Home") # Home බොත්තම සාදන්න
        self.quality_selector = QComboBox()
        self.quality_selector.addItems(["Best", "1080p", "720p", "480p", "360p"])
        # අලුතින් එකතු කළ Traffic Monitor බොත්තම
        self.traffic_btn = QPushButton("🌐 Traffic")

        # User-Agent Switcher (අනන්‍යතාවය සැඟවීම)
        self.ua_combo = QComboBox()
        self.ua_combo.addItems([
            "Default (Twin-Browser)",
            "Google Chrome (Windows)",
            "Googlebot",
            "iPhone Safari",
            "cURL"
        ])

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter URL here...")

        # 2. මූලික Navigation සඳහා වැඩ පැවරීම (Signals & Slots)
        self.back_btn.clicked.connect(self.engine.back)
        self.forward_btn.clicked.connect(self.engine.forward)
        self.reload_btn.clicked.connect(self.engine.reload)
        self.address_bar.returnPressed.connect(self.navigate)
        self.ua_combo.currentTextChanged.connect(self.change_user_agent)
        self.download_btn = QPushButton("📥 Download Video")
        
        # Address Bar එක Update කිරීම සඳහා
        self.engine.urlChanged.connect(self.update_address_bar)

        # සටහන: scan_btn සහ game_btn සම්බන්ධ කරන්නේ main.py එකෙනි.
        
        # 3. Layout එක සැකසීම (බොත්තම් පේළියට තැබීම)
        layout = QHBoxLayout()
        layout.addWidget(self.back_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.reload_btn)
        layout.addWidget(self.ua_combo)
        layout.addWidget(self.home_btn) # Home බොත්තම මෙතැනට දාන්න
        layout.addWidget(self.address_bar)
        layout.addWidget(self.scan_btn)
        layout.addWidget(self.traffic_btn) # Traffic බොත්තම මෙතැනට දැම්මා
        layout.addWidget(self.game_btn) 
        layout.addWidget(self.bookmark_btn)
        layout.addWidget(self.notes_btn)
        layout.addWidget(self.view_bookmarks_btn)
        layout.addWidget(self.quality_selector)
        layout.addWidget(self.download_btn)


        self.setLayout(layout)

    def navigate(self):
        url = self.address_bar.text()
        # හිස් URL එකක් නම් navigate නොකර සිටීම හොඳ පුරුද්දකි
        if url.strip():
            self.engine.load_new_url(url)

    def update_address_bar(self, qurl):
        # අලුත් URL එක Address Bar එකේ පෙන්වීම
        self.address_bar.setText(qurl.toString())

    def change_user_agent(self, text):
        user_agents = {
            "Default (Twin-Browser)": "",
            "Google Chrome (Windows)": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "iPhone Safari": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "cURL": "curl/7.68.0"
        }
        selected_ua = user_agents.get(text, "")
        self.engine.set_custom_user_agent(selected_ua)