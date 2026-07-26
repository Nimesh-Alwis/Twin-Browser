import time
import requests
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QTextEdit, QPushButton, QLabel, QComboBox, 
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal

class RequestWorker(QThread):
    finished_signal = pyqtSignal(dict)

    def __init__(self, method, url, headers, body):
        super().__init__()
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    def run(self):
        start_time = time.time()
        try:
            resp = requests.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                data=self.body.encode("utf-8") if self.body else None,
                timeout=12,
                verify=False
            )
            elapsed = round((time.time() - start_time) * 1000, 2)
            
            headers_dict = dict(resp.headers)
            headers_str = "\n".join([f"{k}: {v}" for k, v in headers_dict.items()])

            self.finished_signal.emit({
                "status_code": resp.status_code,
                "status_text": resp.reason,
                "time_ms": elapsed,
                "headers": headers_str,
                "body": resp.text
            })
        except Exception as e:
            elapsed = round((time.time() - start_time) * 1000, 2)
            self.finished_signal.emit({
                "status_code": 0,
                "status_text": "Connection Error",
                "time_ms": elapsed,
                "headers": "Error fetching response",
                "body": f"[Error]: {str(e)}"
            })

class RequestRepeaterWidget(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("TwinBrowser: HTTP Request Repeater")
        self.resize(800, 560)

        self.setStyleSheet("""
            QWidget {
                background-color: #140b24;
                color: #f3e8ff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #201138;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 8px;
                padding: 6px 10px;
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
            QPushButton.send-btn {
                background-color: #7e22ce;
                color: #ffffff;
                font-weight: bold;
                border: 1.5px solid #c084fc;
            }
            QLabel {
                color: #c084fc;
                font-weight: 600;
            }
        """)

        # Method & URL bar
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter Target Request URL (e.g. https://httpbin.org/post)...")

        self.send_btn = QPushButton("🚀 Send Request")
        self.send_btn.setProperty("class", "send-btn")
        self.send_btn.clicked.connect(self.send_request)

        url_layout = QHBoxLayout()
        url_layout.addWidget(self.method_combo)
        url_layout.addWidget(self.url_input, stretch=1)
        url_layout.addWidget(self.send_btn)

        # Request Tabs (Headers, Body)
        self.req_tabs = QTabWidget()
        self.headers_edit = QTextEdit()
        self.headers_edit.setPlaceholderText("User-Agent: TwinBrowser-Repeater/1.0\nAccept: */*\nContent-Type: application/json")
        self.headers_edit.setPlainText("User-Agent: TwinBrowser-Repeater/1.0\nAccept: */*")

        self.body_edit = QTextEdit()
        self.body_edit.setPlaceholderText("Enter POST/PUT Payload Data (JSON, Form Data, Raw Text)...")

        self.req_tabs.addTab(self.headers_edit, "Headers")
        self.req_tabs.addTab(self.body_edit, "Body Payload")

        # Response Section
        self.status_label = QLabel("Status: Ready")
        self.resp_tabs = QTabWidget()

        self.resp_body_edit = QTextEdit()
        self.resp_body_edit.setReadOnly(True)
        self.resp_body_edit.setPlaceholderText("Response Body will appear here...")

        self.resp_headers_edit = QTextEdit()
        self.resp_headers_edit.setReadOnly(True)
        self.resp_headers_edit.setPlaceholderText("Response Headers will appear here...")

        self.resp_tabs.addTab(self.resp_body_edit, "Response Body")
        self.resp_tabs.addTab(self.resp_headers_edit, "Response Headers")

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        layout.addLayout(url_layout)
        layout.addWidget(QLabel("Request Options:"))
        layout.addWidget(self.req_tabs, stretch=1)
        layout.addWidget(self.status_label)
        layout.addWidget(QLabel("Response Inspection:"))
        layout.addWidget(self.resp_tabs, stretch=1)

        self.setLayout(layout)

    def set_target_url(self, url):
        if url and not url.startswith("twin://"):
            self.url_input.setText(url)

    def send_request(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a target URL first!")
            return

        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
            self.url_input.setText(url)

        method = self.method_combo.currentText()
        raw_headers = self.headers_edit.toPlainText().strip()
        body = self.body_edit.toPlainText()

        headers = {}
        if raw_headers:
            for line in raw_headers.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    headers[k.strip()] = v.strip()

        self.send_btn.setEnabled(False)
        self.status_label.setText("Status: Sending Request...")

        self.worker = RequestWorker(method, url, headers, body)
        self.worker.finished_signal.connect(self.on_request_finished)
        self.worker.start()

    def on_request_finished(self, data):
        self.send_btn.setEnabled(True)
        code = data["status_code"]
        reason = data["status_text"]
        time_ms = data["time_ms"]

        if code != 0:
            self.status_label.setText(f"Status: {code} {reason} | Time: {time_ms} ms")
        else:
            self.status_label.setText(f"Status: Connection Error | Time: {time_ms} ms")

        self.resp_headers_edit.setPlainText(data["headers"])
        self.resp_body_edit.setPlainText(data["body"])
