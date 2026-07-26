import urllib.parse
import requests
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QTextEdit, QProgressBar, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal

class FuzzWorker(QThread):
    finished_signal = pyqtSignal(dict)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        parsed = urllib.parse.urlparse(self.url)
        params = urllib.parse.parse_qs(parsed.query)

        if not params:
            self.finished_signal.emit({
                "success": False,
                "error": "No GET parameters found in URL. Example of URL with params: http://example.com/page.php?id=1&search=test"
            })
            return

        findings = []
        base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

        # 1. Test Reflected XSS
        xss_payload = "twinxss'<script>alert(1)</script>"
        for param in params.keys():
            test_params = dict(params)
            test_params[param] = xss_payload
            try:
                r = requests.get(base_url, params=test_params, timeout=8, verify=False)
                if xss_payload in r.text:
                    findings.append(f"[HIGH] Potential Reflected XSS in parameter '{param}'!")
            except Exception:
                pass

        # 2. Test LFI (Local File Inclusion)
        lfi_payload = "../../../../etc/passwd"
        lfi_sig = "root:x:0:0:"
        for param in params.keys():
            test_params = dict(params)
            test_params[param] = lfi_payload
            try:
                r = requests.get(base_url, params=test_params, timeout=8, verify=False)
                if lfi_sig in r.text:
                    findings.append(f"[CRITICAL] Potential LFI (Local File Inclusion) in parameter '{param}'!")
            except Exception:
                pass

        # 3. Test Open Redirect
        redirect_payload = "https://example.com"
        for param in params.keys():
            test_params = dict(params)
            test_params[param] = redirect_payload
            try:
                r = requests.get(base_url, params=test_params, timeout=8, allow_redirects=False, verify=False)
                if r.status_code in [301, 302, 303, 307, 308]:
                    loc = r.headers.get("Location", "")
                    if "example.com" in loc:
                        findings.append(f"[MEDIUM] Potential Open Redirect in parameter '{param}' -> Location: {loc}")
            except Exception:
                pass

        self.finished_signal.emit({
            "success": True,
            "params_count": len(params),
            "findings": findings
        })

class VulnFuzzerWidget(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("TwinBrowser: Parameter Fuzzer & Vuln Checker")
        self.resize(680, 500)

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
        self.url_input.setPlaceholderText("Enter Target URL with parameters (e.g. http://example.com/item.php?id=1&q=test)...")

        self.fuzz_btn = QPushButton("🎯 Start Parameter Fuzzing")
        self.fuzz_btn.clicked.connect(self.start_fuzzing)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.url_input, stretch=1)
        top_layout.addWidget(self.fuzz_btn)

        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        self.result_edit.setPlaceholderText("Vulnerability Fuzzing findings will be listed here...")

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        layout.addLayout(top_layout)
        layout.addWidget(QLabel("Security Fuzzing Results & Vulnerability Checks:"))
        layout.addWidget(self.result_edit, stretch=1)

        self.setLayout(layout)

    def set_target_url(self, url):
        if url and not url.startswith("twin://"):
            self.url_input.setText(url)

    def start_fuzzing(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a target URL first!")
            return

        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
            self.url_input.setText(url)

        self.fuzz_btn.setEnabled(False)
        self.result_edit.setPlainText("Fuzzing parameters for XSS, LFI, and Open Redirect vulnerabilities...")

        self.worker = FuzzWorker(url)
        self.worker.finished_signal.connect(self.on_fuzz_finished)
        self.worker.start()

    def on_fuzz_finished(self, res):
        self.fuzz_btn.setEnabled(True)
        if not res["success"]:
            self.result_edit.setPlainText(f"[Notice]: {res['error']}")
            return

        lines = [f"=== Parameter Fuzzing Scan Report for {self.url_input.text()} ===", ""]
        lines.append(f"Parameters Tested: {res['params_count']}")
        lines.append("-" * 55)

        findings = res["findings"]
        if findings:
            for item in findings:
                lines.append(f"⚠️  {item}")
        else:
            lines.append("✅ No immediate Reflected XSS, LFI, or Open Redirect vulnerabilities detected.")

        self.result_edit.setPlainText("\n".join(lines))
