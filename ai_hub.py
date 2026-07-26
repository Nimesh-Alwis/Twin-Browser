from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QScrollArea, QGridLayout, QFrame)
from PyQt6.QtCore import Qt

AI_TOOLS = [
    {"name": "ChatGPT", "category": "Chat AI", "icon": "🤖", "url": "https://chatgpt.com", "desc": "OpenAI's Conversational AI"},
    {"name": "Claude AI", "category": "Chat AI", "icon": "🧠", "url": "https://claude.ai", "desc": "Anthropic's Advanced Reasoning AI"},
    {"name": "Google Gemini", "category": "Chat AI", "icon": "✨", "url": "https://gemini.google.com", "desc": "Google Multimodal AI Model"},
    {"name": "Perplexity AI", "category": "Research AI", "icon": "🔍", "url": "https://www.perplexity.ai", "desc": "AI Powered Search Engine"},
    {"name": "DeepSeek AI", "category": "Coding AI", "icon": "🐋", "url": "https://chat.deepseek.com", "desc": "Powerful Open Source Reasoning AI"},
    {"name": "Poe by Quora", "category": "Chat AI", "icon": "🦅", "url": "https://poe.com", "desc": "Access Multiple AI Bots in One Place"},
    {"name": "Microsoft Copilot", "category": "Chat AI", "icon": "💻", "url": "https://copilot.microsoft.com", "desc": "Microsoft Web & Productivity AI"},
    {"name": "HuggingChat", "category": "Coding AI", "icon": "🤗", "url": "https://huggingface.co/chat", "desc": "Open Source Models Hub"},
    {"name": "Mistral Le Chat", "category": "Chat AI", "icon": "🌪️", "url": "https://chat.mistral.ai", "desc": "Fast French Frontier AI"},
    {"name": "Phind (Dev AI)", "category": "Coding AI", "icon": "⚡", "url": "https://www.phind.com", "desc": "AI Search Engine for Developers"},
    {"name": "You.com", "category": "Research AI", "icon": "🧭", "url": "https://you.com", "desc": "Customizable AI Assistant & Search"},
    {"name": "Grok AI", "category": "Chat AI", "icon": "🚀", "url": "https://x.ai", "desc": "xAI Real-time Knowledge Engine"},
    {"name": "Consensus", "category": "Research AI", "icon": "📚", "url": "https://consensus.app", "desc": "AI Academic Research Assistant"},
    {"name": "SciSpace", "category": "Research AI", "icon": "🔬", "url": "https://typeset.io", "desc": "Read & Understand Scientific Papers"},
    {"name": "Midjourney", "category": "Image AI", "icon": "🎨", "url": "https://www.midjourney.com", "desc": "Photorealistic AI Image Generator"},
    {"name": "ElevenLabs", "category": "Audio AI", "icon": "🗣️", "url": "https://elevenlabs.io", "desc": "AI Voice Generator & Text to Speech"},
    {"name": "Suno AI", "category": "Audio AI", "icon": "🎵", "url": "https://suno.com", "desc": "AI Music & Song Creator"},
    {"name": "RunwayML", "category": "Video AI", "icon": "🎬", "url": "https://runwayml.com", "desc": "AI Video Generation & Editing"},
    {"name": "Leonardo.Ai", "category": "Image AI", "icon": "🖼️", "url": "https://leonardo.ai", "desc": "Creative Production Image AI"},
    {"name": "Krea AI", "category": "Image AI", "icon": "🪄", "url": "https://www.krea.ai", "desc": "Real-time AI Image Enhancement"},
    {"name": "DeepL Translator", "category": "Research AI", "icon": "🌐", "url": "https://www.deepl.com", "desc": "High Accuracy AI Translation"},
    {"name": "Perchance AI", "category": "Image AI", "icon": "🔮", "url": "https://perchance.org", "desc": "Free Text & Image Generators"}
]

class AIHubWidget(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("TwinBrowser: ALL AI Hub")
        self.resize(850, 580)

        self.setStyleSheet("""
            QWidget {
                background-color: #140b24;
                color: #f3e8ff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit {
                background-color: #201138;
                border: 1px solid rgba(192, 132, 252, 0.35);
                border-radius: 14px;
                padding: 8px 16px;
                color: #f3e8ff;
                font-size: 13px;
            }
            QPushButton.filter-btn {
                background-color: #23143c;
                border: 1px solid rgba(192, 132, 252, 0.25);
                border-radius: 10px;
                padding: 6px 14px;
                color: #d8b4fe;
                font-weight: 600;
            }
            QPushButton.filter-btn:hover, QPushButton.filter-btn:checked {
                background-color: #a855f7;
                color: #140b24;
            }
            QFrame.ai-card {
                background-color: #1e1038;
                border: 1px solid rgba(192, 132, 252, 0.2);
                border-radius: 12px;
                padding: 10px;
            }
            QFrame.ai-card:hover {
                border: 1px solid #c084fc;
                background-color: #29154a;
            }
            QPushButton.launch-btn {
                background-color: #a855f7;
                border: none;
                border-radius: 8px;
                padding: 6px 12px;
                color: #140b24;
                font-weight: bold;
            }
            QPushButton.launch-btn:hover {
                background-color: #c084fc;
            }
            QLabel {
                color: #f3e8ff;
            }
        """)

        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search 22+ Inbuilt AI Tools (e.g. ChatGPT, Claude, DeepSeek)...")
        self.search_input.textChanged.connect(self.filter_tools)

        # Categories
        cat_layout = QHBoxLayout()
        cat_layout.setSpacing(6)
        self.categories = ["All", "Chat AI", "Coding AI", "Research AI", "Image AI", "Audio AI", "Video AI"]
        self.category_btns = []

        for cat in self.categories:
            btn = QPushButton(cat)
            btn.setProperty("class", "filter-btn")
            btn.setCheckable(True)
            if cat == "All":
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, c=cat, b=btn: self.select_category(c, b))
            cat_layout.addWidget(btn)
            self.category_btns.append(btn)
        cat_layout.addStretch()

        # Cards Scroll Container
        self.cards_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(12)
        self.cards_widget.setLayout(self.grid_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.cards_widget)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header_label = QLabel("🤖 ALL AI Hub - Built-in Top 20+ AI Platforms")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #c084fc;")

        layout.addWidget(header_label)
        layout.addWidget(self.search_input)
        layout.addLayout(cat_layout)
        layout.addWidget(scroll, stretch=1)

        self.setLayout(layout)

        self.selected_cat = "All"
        self.render_cards(AI_TOOLS)

    def select_category(self, category_name, clicked_btn):
        self.selected_cat = category_name
        for btn in self.category_btns:
            btn.setChecked(btn == clicked_btn)
        self.filter_tools()

    def filter_tools(self):
        query = self.search_input.text().strip().lower()
        filtered = []

        for tool in AI_TOOLS:
            matches_cat = (self.selected_cat == "All") or (tool["category"] == self.selected_cat)
            matches_query = (not query) or (query in tool["name"].lower()) or (query in tool["desc"].lower())
            if matches_cat and matches_query:
                filtered.append(tool)

        self.render_cards(filtered)

    def render_cards(self, tools_list):
        # Clear existing grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        columns = 3
        for idx, tool in enumerate(tools_list):
            card = QFrame()
            card.setProperty("class", "ai-card")
            
            c_layout = QVBoxLayout()
            c_layout.setContentsMargins(10, 10, 10, 10)
            c_layout.setSpacing(6)

            title_lbl = QLabel(f"{tool['icon']} {tool['name']}")
            title_lbl.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")

            cat_lbl = QLabel(tool['category'])
            cat_lbl.setStyleSheet("font-size: 11px; color: #a855f7; font-weight: 600;")

            desc_lbl = QLabel(tool['desc'])
            desc_lbl.setWordWrap(True)
            desc_lbl.setStyleSheet("font-size: 12px; color: #b8a2d1;")

            launch_btn = QPushButton("Launch 🚀")
            launch_btn.setProperty("class", "launch-btn")
            launch_btn.clicked.connect(lambda checked, url=tool['url']: self.launch_ai(url))

            c_layout.addWidget(title_lbl)
            c_layout.addWidget(cat_lbl)
            c_layout.addWidget(desc_lbl, stretch=1)
            c_layout.addWidget(launch_btn)

            card.setLayout(c_layout)
            row = idx // columns
            col = idx % columns
            self.grid_layout.addWidget(card, row, col)

    def launch_ai(self, url):
        if self.main_window:
            self.main_window.add_new_tab(url=url)
            self.close()
