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
        self.resize(680, 460)

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
                padding: 8px 16px;
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

        self.operation_combo = QComboBox()
        self.operation_combo.addItems([
            "URL Encode", "URL Decode",
            "Base64 Encode", "Base64 Decode",
            "HTML Entity Encode", "HTML Entity Decode",
            "Hex Encode", "Hex Decode",
            "Hash: MD5", "Hash: SHA-1", "Hash: SHA-256", "Hash: SHA-512"
        ])

        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText("Enter input text or payload here...")

        self.output_edit = QTextEdit()
        self.output_edit.setPlaceholderText("Converted output will appear here...")
        self.output_edit.setReadOnly(True)

        self.convert_btn = QPushButton("⚡ Process Operation")
        self.convert_btn.clicked.connect(self.process_conversion)

        self.swap_btn = QPushButton("⇄ Copy Output to Input")
        self.swap_btn.clicked.connect(self.copy_output_to_input)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.convert_btn)
        btn_layout.addWidget(self.swap_btn)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        layout.addWidget(QLabel("Select Converter / Hasher:"))
        layout.addWidget(self.operation_combo)
        layout.addWidget(QLabel("Input Data:"))
        layout.addWidget(self.input_edit)
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("Output Result:"))
        layout.addWidget(self.output_edit)

        self.setLayout(layout)

    def process_conversion(self):
        op = self.operation_combo.currentText()
        text = self.input_edit.toPlainText()

        if not text:
            self.output_edit.clear()
            return

        try:
            if op == "URL Encode":
                res = urllib.parse.quote(text)
            elif op == "URL Decode":
                res = urllib.parse.unquote(text)
            elif op == "Base64 Encode":
                res = base64.b64encode(text.encode("utf-8")).decode("utf-8")
            elif op == "Base64 Decode":
                res = base64.b64decode(text.encode("utf-8")).decode("utf-8")
            elif op == "HTML Entity Encode":
                res = html.escape(text)
            elif op == "HTML Entity Decode":
                res = html.unescape(text)
            elif op == "Hex Encode":
                res = text.encode("utf-8").hex()
            elif op == "Hex Decode":
                res = bytes.fromhex(text.strip()).decode("utf-8")
            elif op == "Hash: MD5":
                res = hashlib.md5(text.encode("utf-8")).hexdigest()
            elif op == "Hash: SHA-1":
                res = hashlib.sha1(text.encode("utf-8")).hexdigest()
            elif op == "Hash: SHA-256":
                res = hashlib.sha256(text.encode("utf-8")).hexdigest()
            elif op == "Hash: SHA-512":
                res = hashlib.sha512(text.encode("utf-8")).hexdigest()
            else:
                res = text

            self.output_edit.setPlainText(res)
        except Exception as e:
            self.output_edit.setPlainText(f"Error executing {op}: {str(e)}")

    def copy_output_to_input(self):
        out_text = self.output_edit.toPlainText()
        if out_text:
            self.input_edit.setPlainText(out_text)
            self.output_edit.clear()
