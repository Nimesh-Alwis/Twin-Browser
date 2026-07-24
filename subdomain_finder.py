import requests
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QApplication)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

class SubdomainThread(QThread):
    finished_signal = pyqtSignal(str, list)
    error_signal = pyqtSignal(str)

    def __init__(self, domain):
        super().__init__()
        self.domain = domain

    def run(self):
        try:
            # Domain string cleanup (e.g., extract root domain)
            clean_domain = self.domain.replace('https://', '').replace('http://', '').split('/')[0].split(':')[0]
            if clean_domain.startswith('www.'):
                clean_domain = clean_domain[4:]

            url = f"https://crt.sh/?q=%.{clean_domain}&output=json"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) TwinBrowser/2.0'}
            
            response = requests.get(url, headers=headers, timeout=12)
            if response.status_code != 200:
                self.error_signal.emit(f"crt.sh returned status code {response.status_code}")
                return

            data = response.json()
            subdomains = set()

            for entry in data:
                name_value = entry.get('name_value', '')
                lines = name_value.split('\n')
                for line in lines:
                    sub = line.strip().lower()
                    if sub.startswith('*.'):
                        sub = sub[2:]
                    if sub and not sub.startswith('*'):
                        subdomains.add(sub)

            sorted_subs = sorted(list(subdomains))
            self.finished_signal.emit(clean_domain, sorted_subs)
        except Exception as e:
            self.error_signal.emit(f"Error fetching subdomains: {str(e)}")


class SubdomainDialog(QWidget):
    def __init__(self, target_domain):
        super().__init__()
        self.target_domain = target_domain
        self.subdomains_cache = []

        self.setWindowTitle(f"Subdomain Finder - {target_domain}")
        self.resize(550, 520)

        # Vivaldi Purple Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #140b24;
                color: #f3e8ff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit {
                background-color: #261642;
                border: 1px solid rgba(192, 132, 252, 0.35);
                border-radius: 12px;
                padding: 6px 12px;
                color: #f5e6ff;
            }
            QLineEdit:focus {
                border: 1.5px solid #c084fc;
            }
            QListWidget {
                background-color: #201138;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 10px;
                padding: 6px;
                color: #f3e8ff;
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 5px 8px;
                border-radius: 6px;
            }
            QListWidget::item:hover {
                background-color: #351a5c;
            }
            QListWidget::item:selected {
                background-color: #a855f7;
                color: #140b24;
                font-weight: bold;
            }
            QPushButton {
                background-color: #2b1747;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 8px;
                padding: 7px 14px;
                color: #e9d5ff;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3d1c69;
                border: 1px solid #c084fc;
                color: #ffffff;
            }
            QLabel {
                color: #c084fc;
                font-weight: 600;
            }
        """)

        # UI Components
        self.header_label = QLabel(f"🕵️ Subdomains for: {target_domain}")
        self.header_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("🔍 Filter subdomains...")
        self.filter_input.textChanged.connect(self.filter_list)

        self.list_widget = QListWidget()

        self.status_label = QLabel("Status: Querying crt.sh logs...")
        self.status_label.setStyleSheet("color: #b8a2d1; font-size: 12px;")

        self.copy_btn = QPushButton("📋 Copy All")
        self.copy_btn.clicked.connect(self.copy_all)

        self.export_btn = QPushButton("💾 Export to TXT")
        self.export_btn.clicked.connect(self.export_txt)

        self.refresh_btn = QPushButton("↻ Refresh")
        self.refresh_btn.clicked.connect(self.start_scan)

        # Layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.refresh_btn)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        layout.addWidget(self.header_label)
        layout.addWidget(self.filter_input)
        layout.addWidget(self.list_widget, stretch=1)
        layout.addWidget(self.status_label)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Start Scan
        self.start_scan()

    def start_scan(self):
        self.list_widget.clear()
        self.status_label.setText("Status: Fetching logs from crt.sh...")
        self.worker = SubdomainThread(self.target_domain)
        self.worker.finished_signal.connect(self.on_scan_finished)
        self.worker.error_signal.connect(self.on_scan_error)
        self.worker.start()

    def on_scan_finished(self, domain, subdomains):
        self.subdomains_cache = subdomains
        self.list_widget.clear()

        for sub in subdomains:
            self.list_widget.addItem(sub)

        count = len(subdomains)
        self.status_label.setText(f"Status: Found {count} unique subdomains for {domain}")
        if count == 0:
            self.list_widget.addItem("No subdomains found.")

    def on_scan_error(self, err_msg):
        self.status_label.setText(f"Status: {err_msg}")
        QMessageBox.warning(self, "Subdomain Finder Error", err_msg)

    def filter_list(self, text):
        query = text.strip().lower()
        self.list_widget.clear()
        for sub in self.subdomains_cache:
            if query in sub:
                self.list_widget.addItem(sub)

    def copy_all(self):
        if self.subdomains_cache:
            text = "\n".join(self.subdomains_cache)
            QApplication.clipboard().setText(text)
            QMessageBox.information(self, "Success", f"Copied {len(self.subdomains_cache)} subdomains to clipboard!")

    def export_txt(self):
        if not self.subdomains_cache:
            QMessageBox.warning(self, "Export Warning", "No subdomains to export.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Export Subdomains", f"{self.target_domain}_subdomains.txt", "Text Files (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.subdomains_cache))
            QMessageBox.information(self, "Export Success", f"Saved subdomains to {path}")
