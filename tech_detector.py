import requests
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QTextEdit, QProgressBar, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal

SIGNATURES = {
    "CMS": {
        "WordPress": ["wp-content", "wp-includes", "wp-json"],
        "Joomla": ["/components/com_", "Joomla!"],
        "Drupal": ["Drupal", "sites/all/themes"],
        "Shopify": ["cdn.shopify.com", "Shopify.theme"]
    },
    "Backend & Frameworks": {
        "Laravel": ["laravel_session", "X-SRF-TOKEN"],
        "Django": ["csrftoken", "Django"],
        "Express / Node.js": ["X-Powered-By: Express", "express"],
        "ASP.NET": ["X-Powered-By: ASP.NET", "ASP.NET_SessionId"],
        "Spring": ["JSESSIONID", "Spring"]
    },
    "Web Server": {
        "Nginx": ["server: nginx"],
        "Apache": ["server: apache"],
        "Microsoft-IIS": ["server: microsoft-iis"],
        "Cloudflare": ["server: cloudflare", "cf-ray"]
    },
    "WAF & CDN": {
        "Cloudflare WAF": ["__cfduid", "cf-ray", "server: cloudflare"],
        "Akamai": ["akamai", "X-Akamai"],
        "Incapsula / Imperva": ["incap_ses", "visid_incap"],
        "Sucuri": ["sucuri_cloudproxy"]
    }
}

class ScanWorker(QThread):
    finished_signal = pyqtSignal(dict)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            resp = requests.get(self.url, timeout=10, verify=False)
            headers_str = "\n".join([f"{k}: {v}" for k, v in resp.headers.items()]).lower()
            body_str = resp.text.lower()
            combined = headers_str + "\n" + body_str

            detected = {}
            for cat, items in SIGNATURES.items():
                detected[cat] = []
                for name, sigs in items.items():
                    for sig in sigs:
                        if sig.lower() in combined:
                            detected[cat].append(name)
                            break

            self.finished_signal.emit({
                "success": True,
                "status_code": resp.status_code,
                "detected": detected,
                "headers": resp.headers
            })
        except Exception as e:
            self.finished_signal.emit({
                "success": False,
                "error": str(e)
            })

class TechDetectorWidget(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("TwinBrowser: Technology Stack & WAF Detector")
        self.resize(650, 480)

        self.setStyleSheet("""
            QWidget {
                background-color: #140b24;
                color: #f3e8ff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit, QTextEdit {
                background-color: #201138;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 8px;
                padding: 6px 12px;
                color: #f3e8ff;
            }
            QPushButton {
                background-color: #23143c;
                border: 1px solid rgba(192, 132, 252, 0.35);
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

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter Target URL to Scan Tech Stack & WAF...")

        self.scan_btn = QPushButton("🔍 Scan Tech Stack")
        self.scan_btn.clicked.connect(self.start_scan)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.url_input, stretch=1)
        top_layout.addWidget(self.scan_btn)

        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        self.result_edit.setPlaceholderText("Scan results will appear here...")

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        layout.addLayout(top_layout)
        layout.addWidget(QLabel("Detected Technologies & WAF Findings:"))
        layout.addWidget(self.result_edit, stretch=1)

        self.setLayout(layout)

    def set_target_url(self, url):
        if url and not url.startswith("twin://"):
            self.url_input.setText(url)

    def start_scan(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a target URL first!")
            return

        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
            self.url_input.setText(url)

        self.scan_btn.setEnabled(False)
        self.result_edit.setPlainText("Scanning target tech stack, web server, and WAF signatures...")

        self.worker = ScanWorker(url)
        self.worker.finished_signal.connect(self.on_scan_finished)
        self.worker.start()

    def on_scan_finished(self, res):
        self.scan_btn.setEnabled(True)
        if not res["success"]:
            self.result_edit.setPlainText(f"[Error]: Failed to scan target.\nDetails: {res['error']}")
            return

        lines = [f"=== Technology Stack & WAF Report for {self.url_input.text()} ===", ""]
        lines.append(f"HTTP Response Status: {res['status_code']}")
        lines.append("-" * 50)

        detected = res["detected"]
        found_any = False
        for cat, items in detected.items():
            if items:
                found_any = True
                lines.append(f"📌 {cat}: {', '.join(items)}")
            else:
                lines.append(f"📌 {cat}: None Detected")

        lines.append("-" * 50)
        lines.append("Server Headers Found:")
        for k, v in res["headers"].items():
            if k.lower() in ["server", "x-powered-by", "set-cookie", "via", "cf-ray"]:
                lines.append(f"  • {k}: {v}")

        self.result_edit.setPlainText("\n".join(lines))
