from PyQt6.QtWidgets import (QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, 
                             QWidget, QComboBox, QLabel, QScrollArea)

class NavigationBar(QWidget):
    def __init__(self, browser_engine):
        super().__init__()
        self.engine = browser_engine

        # Sidebar Toggle Button
        self.sidebar_toggle_btn = QPushButton("🛠️ Tools")
        self.sidebar_toggle_btn.setToolTip("Toggle Tools Panel")

        # Navigation Controls
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

        # Connect Navigation Signals
        self.back_btn.clicked.connect(self.engine.back)
        self.forward_btn.clicked.connect(self.engine.forward)
        self.reload_btn.clicked.connect(self.engine.reload)
        self.address_bar.returnPressed.connect(self.navigate)
        self.ua_combo.currentTextChanged.connect(self.change_user_agent)
        self.engine.urlChanged.connect(self.update_address_bar)

        # Single Clean Header Layout
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)
        layout.addWidget(self.sidebar_toggle_btn)
        layout.addWidget(self.back_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.reload_btn)
        layout.addWidget(self.home_btn)
        layout.addWidget(self.address_bar, stretch=1)
        layout.addWidget(self.ua_combo)

        self.setLayout(layout)

    def set_engine(self, new_engine):
        try:
            self.back_btn.clicked.disconnect()
            self.forward_btn.clicked.disconnect()
            self.reload_btn.clicked.disconnect()
            self.engine.urlChanged.disconnect(self.update_address_bar)
        except Exception:
            pass

        self.engine = new_engine
        self.back_btn.clicked.connect(self.engine.back)
        self.forward_btn.clicked.connect(self.engine.forward)
        self.reload_btn.clicked.connect(self.engine.reload)
        self.engine.urlChanged.connect(self.update_address_bar)
        self.update_address_bar(self.engine.url())

    def navigate(self):
        url = self.address_bar.text()
        if url.strip() and self.engine:
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
        if self.engine:
            self.engine.set_custom_user_agent(selected_ua)


class ToolsSidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)

        # Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1a0e30;
                color: #f3e8ff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #c084fc;
                font-weight: 700;
                font-size: 13px;
                padding: 4px;
            }
            QPushButton {
                background-color: #251442;
                border: 1px solid rgba(192, 132, 252, 0.25);
                border-radius: 10px;
                padding: 9px 14px;
                color: #e9d5ff;
                font-weight: 600;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #381c63;
                border: 1px solid #c084fc;
                color: #ffffff;
            }
            QComboBox {
                background-color: #251442;
                border: 1px solid rgba(192, 132, 252, 0.25);
                border-radius: 10px;
                padding: 6px 10px;
                color: #e9d5ff;
            }
        """)

        # Title
        self.title_label = QLabel("🛠️ Security Tools")

        # Tool Action Buttons
        self.scan_btn = QPushButton("🔍 Scan Site")
        self.subdomain_btn = QPushButton("🕵️ Subdomains")
        self.traffic_btn = QPushButton("🌐 Traffic Monitor")
        self.notes_btn = QPushButton("📝 Payload Notes")
        self.bookmark_btn = QPushButton("⭐ Bookmark Page")
        self.view_bookmarks_btn = QPushButton("📂 View Bookmarks")
        self.theme_btn = QPushButton("🎨 Customize Theme")
        
        self.media_label = QLabel("📥 Downloader")
        self.quality_selector = QComboBox()
        self.quality_selector.addItems(["Best", "1080p", "720p", "480p", "360p"])
        self.download_btn = QPushButton("📥 Download Video")

        self.game_label = QLabel("🎮 Downtime")
        self.game_btn = QPushButton("🎮 Mini Game")

        # Scroll Content
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 12, 10, 12)
        layout.setSpacing(10)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.scan_btn)
        layout.addWidget(self.subdomain_btn)
        layout.addWidget(self.traffic_btn)
        layout.addWidget(self.notes_btn)
        layout.addWidget(self.bookmark_btn)
        layout.addWidget(self.view_bookmarks_btn)
        layout.addWidget(self.theme_btn)
        
        layout.addSpacing(10)
        layout.addWidget(self.media_label)
        layout.addWidget(self.quality_selector)
        layout.addWidget(self.download_btn)

        layout.addSpacing(10)
        layout.addWidget(self.game_label)
        layout.addWidget(self.game_btn)
        layout.addStretch()

        content_widget.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def toggle_sidebar(self):
        self.setVisible(not self.isVisible())