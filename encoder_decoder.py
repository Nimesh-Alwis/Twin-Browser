import urllib.parse
import base64
import html
import hashlib
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QLabel, QComboBox, QMessageBox)

class EncoderDecoderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TwinBrowser: Cyber Encoding & Hashing Utility")
        self.resize(720, 520)

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
                font-size: 13px;
            }
            QPushButton.action-btn {
                background-color: #23143c;
                border: 1px solid rgba(192, 132, 252, 0.35);
                border-radius: 8px;
                padding: 8px 18px;
                color: #e9d5ff;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton.action-btn:hover {
                background-color: #3b1d66;
                border: 1px solid #c084fc;
                color: #ffffff;
            }
            QPushButton.encode-btn {
                background-color: #6b21a8;
                color: #ffffff;
            }
            QPushButton.decode-btn {
                background-color: #0369a1;
                color: #ffffff;
            }
            QLabel {
                color: #c084fc;
                font-weight: 600;
            }
        """)

        self.format_combo = QComboBox()
        self.format_combo.addItems([
            "Base64",
            "URL Encoding",
            "HTML Entities",
            "Hexadecimal",
            "Hash: MD5",
            "Hash: SHA-1",
            "Hash: SHA-256",
            "Hash: SHA-512"
        ])
        self.format_combo.currentTextChanged.connect(self.on_format_changed)

        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText("Enter text or payload to encode/decode...")

        self.output_edit = QTextEdit()
        self.output_edit.setPlaceholderText("Result will appear here automatically...")
        self.output_edit.setReadOnly(True)

        self.encode_btn = QPushButton("🔒 ENCODE")
        self.encode_btn.setProperty("class", "action-btn encode-btn")
        self.decode_btn = QPushButton("🔓 DECODE")
        self.decode_btn.setProperty("class", "action-btn decode-btn")
        self.swap_btn = QPushButton("⇄ Swap Input / Output")
        self.swap_btn.setProperty("class", "action-btn")

        self.encode_btn.clicked.connect(self.do_encode)
        self.decode_btn.clicked.connect(self.do_decode)
        self.swap_btn.clicked.connect(self.swap_input_output)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addWidget(self.encode_btn)
        btn_layout.addWidget(self.decode_btn)
        btn_layout.addWidget(self.swap_btn)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Select Encoding Format / Algorithm:"))
        layout.addWidget(self.format_combo)
        layout.addWidget(QLabel("Input Data:"))
        layout.addWidget(self.input_edit, stretch=1)
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("Output Result:"))
        layout.addWidget(self.output_edit, stretch=1)

        self.setLayout(layout)

        # Realtime encoding on text change
        self.input_edit.textChanged.connect(self.do_encode)

    def on_format_changed(self, fmt):
        is_hash = fmt.startswith("Hash:")
        self.decode_btn.setEnabled(not is_hash)
        if is_hash:
            self.decode_btn.setToolTip("Hashes are one-way encryption and cannot be decoded directly.")
        else:
            self.decode_btn.setToolTip("Decode input data")
        self.do_encode()

    def do_encode(self):
        text = self.input_edit.toPlainText()
        if not text:
            self.output_edit.clear()
            return

        fmt = self.format_combo.currentText()
        try:
            if fmt == "Base64":
                res = base64.b64encode(text.encode("utf-8")).decode("utf-8")
            elif fmt == "URL Encoding":
                res = urllib.parse.quote(text)
            elif fmt == "HTML Entities":
                res = html.escape(text)
            elif fmt == "Hexadecimal":
                res = text.encode("utf-8").hex()
            elif fmt == "Hash: MD5":
                res = hashlib.md5(text.encode("utf-8")).hexdigest()
            elif fmt == "Hash: SHA-1":
                res = hashlib.sha1(text.encode("utf-8")).hexdigest()
            elif fmt == "Hash: SHA-256":
                res = hashlib.sha256(text.encode("utf-8")).hexdigest()
            elif fmt == "Hash: SHA-512":
                res = hashlib.sha512(text.encode("utf-8")).hexdigest()
            else:
                res = text

            self.output_edit.setPlainText(res)
        except Exception as e:
            self.output_edit.setPlainText(f"[Encode Error]: {str(e)}")

    def do_decode(self):
        text = self.input_edit.toPlainText().strip()
        if not text:
            self.output_edit.clear()
            return

        fmt = self.format_combo.currentText()
        try:
            if fmt == "Base64":
                # Fix missing Base64 padding automatically
                missing_padding = len(text) % 4
                if missing_padding:
                    text += '=' * (4 - missing_padding)
                res = base64.b64decode(text.encode("utf-8")).decode("utf-8", errors="ignore")

            elif fmt == "URL Encoding":
                res = urllib.parse.unquote(text)

            elif fmt == "HTML Entities":
                res = html.unescape(text)

            elif fmt == "Hexadecimal":
                # Remove spaces and prefixes like 0x
                clean_hex = text.replace(" ", "").replace("0x", "").replace("\\x", "")
                res = bytes.fromhex(clean_hex).decode("utf-8", errors="ignore")

            elif fmt.startswith("Hash:"):
                res = "[Notice]: Hashes are one-way mathematical functions and cannot be decoded directly. (Use Rainbow Tables or Crackstation)."

            else:
                res = text

            self.output_edit.setPlainText(res)
        except Exception as e:
            self.output_edit.setPlainText(f"[Decode Error]: Could not decode data with {fmt}.\nDetails: {str(e)}")

    def swap_input_output(self):
        out_text = self.output_edit.toPlainText()
        if out_text and not out_text.startswith("[Error]") and not out_text.startswith("[Notice]"):
            self.input_edit.blockSignals(True)
            self.input_edit.setPlainText(out_text)
            self.input_edit.blockSignals(False)
            self.output_edit.clear()
