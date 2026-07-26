import os
import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
                             QPushButton, QLabel, QLineEdit, QMessageBox, QHeaderView)
from path_utils import get_data_path

SHORTCUTS_FILE = get_data_path("user_shortcuts.json")

DEFAULT_SHORTCUTS = {
    "Open ALL AI Hub": "Ctrl+Shift+A",
    "Open Shortcut Manager": "Ctrl+K",
    "New Tab": "Ctrl+T",
    "Close Current Tab": "Ctrl+W",
    "New Incognito Tab": "Ctrl+Shift+N",
    "Reload Page": "Ctrl+R",
    "Add Bookmark": "Ctrl+D",
    "Open Download Manager": "Ctrl+J",
    "Open Split Screen": "Ctrl+Alt+S",
    "Open Script Injector": "Ctrl+Shift+I",
    "Open Payload Notes": "Ctrl+N",
    "Open Traffic Monitor": "Ctrl+Shift+M"
}

class ShortcutManagerWidget(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("TwinBrowser: Custom Shortcuts Manager")
        self.resize(580, 450)

        self.setStyleSheet("""
            QWidget {
                background-color: #140b24;
                color: #f3e8ff;
                font-family: 'Segoe UI', sans-serif;
            }
            QTableWidget {
                background-color: #201138;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 10px;
                gridline-color: rgba(192, 132, 252, 0.15);
            }
            QTableWidget::item {
                padding: 6px;
            }
            QLineEdit {
                background-color: #261642;
                border: 1px solid #c084fc;
                border-radius: 6px;
                padding: 4px 8px;
                color: #ffffff;
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

        self.shortcuts = self.load_shortcuts()

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Action", "Keyboard Shortcut (e.g. Ctrl+Shift+A)"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.save_btn = QPushButton("💾 Save & Apply Shortcuts")
        self.reset_btn = QPushButton("↺ Reset to Defaults")

        self.save_btn.clicked.connect(self.save_shortcuts)
        self.reset_btn.clicked.connect(self.reset_defaults)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.reset_btn)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        layout.addWidget(QLabel("⌨️ Customize Keyboard Shortcuts:"))
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.populate_table()

    def load_shortcuts(self):
        shortcuts = dict(DEFAULT_SHORTCUTS)
        if os.path.exists(SHORTCUTS_FILE):
            try:
                with open(SHORTCUTS_FILE, "r", encoding="utf-8") as f:
                    user_saved = json.load(f)
                    shortcuts.update(user_saved)
            except Exception as e:
                print(f"Error loading shortcuts: {e}")
        return shortcuts

    def populate_table(self):
        self.table.setRowCount(len(self.shortcuts))
        for row, (action, key_combo) in enumerate(self.shortcuts.items()):
            action_item = QTableWidgetItem(action)
            action_item.setFlags(action_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            input_field = QLineEdit(key_combo)
            self.table.setItem(row, 0, action_item)
            self.table.setCellWidget(row, 1, input_field)

    def save_shortcuts(self):
        updated = {}
        for row in range(self.table.rowCount()):
            action = self.table.item(row, 0).text()
            widget = self.table.cellWidget(row, 1)
            if isinstance(widget, QLineEdit):
                updated[action] = widget.text().strip()

        self.shortcuts = updated
        try:
            with open(SHORTCUTS_FILE, "w", encoding="utf-8") as f:
                json.dump(updated, f, indent=4)
            QMessageBox.information(self, "Success", "Keyboard Shortcuts updated and saved successfully!")
            if self.main_window:
                self.main_window.setup_keyboard_shortcuts()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save shortcuts: {e}")

    def reset_defaults(self):
        self.shortcuts = dict(DEFAULT_SHORTCUTS)
        self.populate_table()
