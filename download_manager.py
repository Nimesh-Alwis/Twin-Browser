import os
import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, 
                             QPushButton, QLabel, QProgressBar, QMessageBox, QFileDialog)
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from path_utils import get_data_path

HISTORY_FILE = get_data_path("downloads_history.json")

class DownloadManagerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TwinBrowser: Download Manager")
        self.resize(650, 420)

        self.setStyleSheet("""
            QWidget {
                background-color: #140b24;
                color: #f3e8ff;
                font-family: 'Segoe UI', sans-serif;
            }
            QListWidget {
                background-color: #201138;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 10px;
                padding: 8px;
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

        self.downloads_list = QListWidget()
        
        self.open_folder_btn = QPushButton("📁 Open Downloads Folder")
        self.open_file_btn = QPushButton("▶ Open Selected File")
        self.clear_btn = QPushButton("🗑 Clear History")

        self.open_folder_btn.clicked.connect(self.open_downloads_folder)
        self.open_file_btn.clicked.connect(self.open_selected_file)
        self.clear_btn.clicked.connect(self.clear_history)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.open_folder_btn)
        btn_layout.addWidget(self.open_file_btn)
        btn_layout.addWidget(self.clear_btn)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("📦 Downloads History & Tasks:"))
        layout.addWidget(self.downloads_list)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_history()

    def load_history(self):
        self.downloads_list.clear()
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        text = f"[{item.get('status', 'Done')}] {item.get('name', 'Unknown')} - {item.get('url', '')}"
                        w_item = QListWidgetItem(text)
                        w_item.setData(32, item.get('path', ''))
                        self.downloads_list.addItem(w_item)
            except Exception as e:
                print(f"Error loading download history: {e}")

    def add_record(self, name, url, file_path, status="Completed"):
        records = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    records = json.load(f)
            except Exception:
                records = []

        records.insert(0, {
            "name": name,
            "url": url,
            "path": file_path,
            "status": status
        })

        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=4)
        except Exception as e:
            print(f"Error saving download record: {e}")

        self.load_history()

    def open_downloads_folder(self):
        folder = get_data_path("downloads")
        if not os.path.exists(folder):
            os.makedirs(folder)
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

    def open_selected_file(self):
        current_item = self.downloads_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Select Item", "Please select a download item from the list first.")
            return
        
        path = current_item.data(32)
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        else:
            QMessageBox.warning(self, "File Not Found", f"File does not exist at: {path}")

    def clear_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                os.remove(HISTORY_FILE)
            except Exception:
                pass
        self.downloads_list.clear()
