from PyQt6.QtNetwork import QNetworkProxy
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QDialog)

class ProxyManager:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.is_enabled = False

    def enable_proxy(self):
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.ProxyType.HttpProxy)
        proxy.setHostName(self.host)
        proxy.setPort(self.port)
        QNetworkProxy.setApplicationProxy(proxy)
        self.is_enabled = True

    def disable_proxy(self):
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.ProxyType.NoProxy)
        QNetworkProxy.setApplicationProxy(proxy)
        self.is_enabled = False

    def toggle_proxy(self):
        if self.is_enabled:
            self.disable_proxy()
        else:
            self.enable_proxy()
        return self.is_enabled


class ProxyConfigDialog(QDialog):
    def __init__(self, proxy_manager, parent=None):
        super().__init__(parent)
        self.proxy_manager = proxy_manager
        self.setWindowTitle("TwinBrowser: Proxy Settings (Burp / ZAP)")
        self.resize(380, 220)

        self.setStyleSheet("""
            QDialog {
                background-color: #140b24;
                color: #f3e8ff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit {
                background-color: #201138;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 8px;
                padding: 6px 12px;
                color: #ffffff;
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

        self.host_input = QLineEdit(self.proxy_manager.host)
        self.port_input = QLineEdit(str(self.proxy_manager.port))

        self.save_btn = QPushButton("💾 Save Configuration")
        self.save_btn.clicked.connect(self.save_config)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        layout.addWidget(QLabel("HTTP / HTTPS Proxy Settings:"))
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Host:"))
        h_layout.addWidget(self.host_input)
        layout.addLayout(h_layout)

        p_layout = QHBoxLayout()
        p_layout.addWidget(QLabel("Port:"))
        p_layout.addWidget(self.port_input)
        layout.addLayout(p_layout)

        layout.addWidget(self.save_btn)
        self.setLayout(layout)

    def save_config(self):
        host = self.host_input.text().strip()
        port_str = self.port_input.text().strip()

        if not host or not port_str.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter a valid Host IP and numeric Port!")
            return

        self.proxy_manager.host = host
        self.proxy_manager.port = int(port_str)

        if self.proxy_manager.is_enabled:
            self.proxy_manager.enable_proxy()

        QMessageBox.information(self, "Success", f"Proxy configuration updated to {host}:{port_str}!")
        self.accept()
