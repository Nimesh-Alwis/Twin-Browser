from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QComboBox

class NavigationBar(QWidget):
    def __init__(self, browser_engine):
        super().__init__()
        self.engine = browser_engine

        # 1. Top Tier: Main Navigation & Address Bar
        self.back_btn = QPushButton("◀")
        self.forward_btn = QPushButton("▶")
        self.reload_btn = QPushButton("↻")
        self.home_btn = QPushButton("🏠 Home")

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("🔍 Search or enter an address...")

        self.ua_combo = QComboBox()
        self.ua_combo.addItems([
            "Default (Twin-Browser)",
            "Google Chrome (Windows)",
            "Googlebot",
            "iPhone Safari",
            "cURL"
        ])

        # 2. Bottom Tier: Security & Productivity Tools
        self.scan_btn = QPushButton("🔍 Scan Site")
        self.subdomain_btn = QPushButton("🕵️ Subdomains")
        self.traffic_btn = QPushButton("🌐 Traffic Monitor")
        self.notes_btn = QPushButton("📝 Payload Notes")
        self.bookmark_btn = QPushButton("⭐ Bookmark")
        self.view_bookmarks_btn = QPushButton("📂 View Bookmarks")
        
        self.quality_selector = QComboBox()
        self.quality_selector.addItems(["Best", "1080p", "720p", "480p", "360p"])
        self.download_btn = QPushButton("📥 Download Video")
        self.game_btn = QPushButton("🎮 Mini Game")

        # Connect Navigation Signals
        self.back_btn.clicked.connect(self.engine.back)
        self.forward_btn.clicked.connect(self.engine.forward)
        self.reload_btn.clicked.connect(self.engine.reload)
        self.address_bar.returnPressed.connect(self.navigate)
        self.ua_combo.currentTextChanged.connect(self.change_user_agent)
        self.engine.urlChanged.connect(self.update_address_bar)

        # 3. Create 2-Tier Layout
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(8)
        top_layout.addWidget(self.back_btn)
        top_layout.addWidget(self.forward_btn)
        top_layout.addWidget(self.reload_btn)
        top_layout.addWidget(self.home_btn)
        top_layout.addWidget(self.address_bar, stretch=1)
        top_layout.addWidget(self.ua_combo)

        tools_layout = QHBoxLayout()
        tools_layout.setContentsMargins(0, 4, 0, 0)
        tools_layout.setSpacing(8)
        tools_layout.addWidget(self.scan_btn)
        tools_layout.addWidget(self.subdomain_btn)
        tools_layout.addWidget(self.traffic_btn)
        tools_layout.addWidget(self.notes_btn)
        tools_layout.addWidget(self.bookmark_btn)
        tools_layout.addWidget(self.view_bookmarks_btn)
        tools_layout.addStretch()
        tools_layout.addWidget(self.quality_selector)
        tools_layout.addWidget(self.download_btn)
        tools_layout.addWidget(self.game_btn)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 8, 10, 8)
        main_layout.setSpacing(6)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(tools_layout)

        self.setLayout(main_layout)

    def navigate(self):
        url = self.address_bar.text()
        if url.strip():
            self.engine.load_new_url(url)

    def update_address_bar(self, qurl):
        url_str = qurl.toString()
        if "homepage.html" in url_str:
            self.address_bar.setText("twin://startpage")
        else:
            self.address_bar.setText(url_str)

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