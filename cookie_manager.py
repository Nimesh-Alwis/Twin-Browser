from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QLineEdit, 
                             QMessageBox, QHeaderView, QDialog, QFormLayout)
from PyQt6.QtCore import Qt, QByteArray
from PyQt6.QtNetwork import QNetworkCookie

class CookieManagerWidget(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("TwinBrowser: Cookie & Session Manager")
        self.resize(700, 480)

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

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Value", "Domain", "Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.refresh_btn = QPushButton("↻ Refresh Cookies")
        self.add_btn = QPushButton("➕ Add Cookie")
        self.delete_btn = QPushButton("🗑 Delete Selected")
        self.clear_all_btn = QPushButton("⚠️ Clear All Cookies")

        self.refresh_btn.clicked.connect(self.load_cookies)
        self.add_btn.clicked.connect(self.open_add_dialog)
        self.delete_btn.clicked.connect(self.delete_selected_cookie)
        self.clear_all_btn.clicked.connect(self.clear_all_cookies)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_all_btn)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        layout.addWidget(QLabel("🍪 Active Site Cookies & Session Data:"))
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.current_cookies = []

    def get_cookie_store(self):
        if self.main_window:
            engine = self.main_window.current_engine()
            if engine:
                return engine.page().profile().cookieStore()
        return None

    def load_cookies(self):
        self.table.setRowCount(0)
        self.current_cookies.clear()
        store = self.get_cookie_store()
        if store:
            store.cookieAdded.connect(self.on_cookie_added)
            store.loadAllCookies()

    def on_cookie_added(self, cookie):
        name = cookie.name().data().decode("utf-8", errors="ignore")
        value = cookie.value().data().decode("utf-8", errors="ignore")
        domain = cookie.domain()
        path = cookie.path()

        self.current_cookies.append(cookie)
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(value))
        self.table.setItem(row, 2, QTableWidgetItem(domain))
        self.table.setItem(row, 3, QTableWidgetItem(path))

    def open_add_dialog(self):
        store = self.get_cookie_store()
        if not store:
            QMessageBox.warning(self, "Error", "No active browser page found.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Add Custom Cookie")
        dialog.resize(350, 220)

        name_in = QLineEdit()
        val_in = QLineEdit()
        dom_in = QLineEdit(".example.com")
        path_in = QLineEdit("/")

        form = QFormLayout()
        form.addRow("Name:", name_in)
        form.addRow("Value:", val_in)
        form.addRow("Domain:", dom_in)
        form.addRow("Path:", path_in)

        save_btn = QPushButton("Save Cookie")
        
        def save():
            c = QNetworkCookie(QByteArray(name_in.text().encode()), QByteArray(val_in.text().encode()))
            c.setDomain(dom_in.text())
            c.setPath(path_in.text())
            store.setCookie(c)
            QMessageBox.information(self, "Added", "Cookie added successfully!")
            dialog.accept()
            self.load_cookies()

        save_btn.clicked.connect(save)
        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(save_btn)
        dialog.setLayout(layout)
        dialog.exec()

    def delete_selected_cookie(self):
        row = self.table.currentRow()
        if row >= 0 and row < len(self.current_cookies):
            cookie = self.current_cookies[row]
            store = self.get_cookie_store()
            if store:
                store.deleteCookie(cookie)
                self.table.removeRow(row)
                QMessageBox.information(self, "Deleted", "Cookie deleted!")
        else:
            QMessageBox.warning(self, "Select Row", "Please select a cookie row from table.")

    def clear_all_cookies(self):
        store = self.get_cookie_store()
        if store:
            store.deleteAllCookies()
            self.table.setRowCount(0)
            self.current_cookies.clear()
            QMessageBox.information(self, "Cleared", "All cookies cleared!")
