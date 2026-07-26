from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QLabel, QComboBox, QMessageBox)

PRESET_SCRIPTS = {
    "Force Dark Mode (CSS)": {
        "type": "css",
        "code": "html, body { background-color: #121212 !important; color: #e0e0e0 !important; } img, video { filter: brightness(0.85); }"
    },
    "High Contrast Dark Filter (CSS)": {
        "type": "css",
        "code": "html { filter: invert(0.9) hue-rotate(180deg) !important; } img, video, canvas { filter: invert(1.1) hue-rotate(180deg) !important; }"
    },
    "Highlight All Links (CSS)": {
        "type": "css",
        "code": "a { background-color: #ffeb3b !important; color: #000000 !important; font-weight: bold !important; border: 1px solid #f57f17 !important; }"
    },
    "Show Image URLs (JS)": {
        "type": "js",
        "code": "document.querySelectorAll('img').forEach(img => { console.log(img.src); alert('Found Image: ' + img.src); });"
    },
    "Disable Anti-Copy & Select (JS)": {
        "type": "js",
        "code": "document.oncontextmenu = null; document.onselectstart = null; document.ondragstart = null; document.onmousedown = null; document.body.style.userSelect = 'auto';"
    }
}

class ScriptInjectorWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("TwinBrowser: Custom CSS / JS Injector")
        self.resize(550, 420)

        self.setStyleSheet("""
            QWidget {
                background-color: #140b24;
                color: #f3e8ff;
                font-family: 'Segoe UI', sans-serif;
            }
            QTextEdit, QComboBox {
                background-color: #201138;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 10px;
                padding: 8px;
                color: #f3e8ff;
            }
            QPushButton {
                background-color: #23143c;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 8px;
                padding: 6px 14px;
                color: #e9d5ff;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3b1d66;
                border: 1px solid #c084fc;
                color: #ffffff;
            }
            QLabel {
                color: #c084fc;
                font-weight: 600;
            }
        """)

        self.preset_combo = QComboBox()
        self.preset_combo.addItems(list(PRESET_SCRIPTS.keys()) + ["Custom Code..."])
        self.preset_combo.currentTextChanged.connect(self.on_preset_changed)

        self.code_edit = QTextEdit()
        self.code_edit.setPlaceholderText("Enter CSS style rules or JavaScript code here...")

        self.inject_css_btn = QPushButton("🎨 Inject CSS Style")
        self.inject_js_btn = QPushButton("⚡ Execute JavaScript")

        self.inject_css_btn.clicked.connect(self.inject_css)
        self.inject_js_btn.clicked.connect(self.execute_js)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.inject_css_btn)
        btn_layout.addWidget(self.inject_js_btn)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Preset Script / Styling:"))
        layout.addWidget(self.preset_combo)
        layout.addWidget(QLabel("Script Editor:"))
        layout.addWidget(self.code_edit)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.on_preset_changed(self.preset_combo.currentText())

    def on_preset_changed(self, text):
        preset = PRESET_SCRIPTS.get(text)
        if preset:
            self.code_edit.setPlainText(preset["code"])
        elif text == "Custom Code...":
            self.code_edit.clear()

    def get_current_engine(self):
        if self.main_window:
            return self.main_window.current_engine()
        return None

    def inject_css(self):
        engine = self.get_current_engine()
        if not engine:
            QMessageBox.warning(self, "No Active Page", "Please navigate to a webpage first.")
            return

        raw_css = self.code_edit.toPlainText().replace('`', '\\`').replace('\n', ' ')
        js_wrapper = f"""
        (function() {{
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = `{raw_css}`;
            document.head.appendChild(style);
        }})();
        """
        engine.page().runJavaScript(js_wrapper)
        QMessageBox.information(self, "Success", "CSS Style Injected successfully!")

    def execute_js(self):
        engine = self.get_current_engine()
        if not engine:
            QMessageBox.warning(self, "No Active Page", "Please navigate to a webpage first.")
            return

        js_code = self.code_edit.toPlainText()
        engine.page().runJavaScript(js_code)
        QMessageBox.information(self, "Executed", "JavaScript Executed on current webpage!")
