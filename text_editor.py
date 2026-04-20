from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QPushButton, QFileDialog

class SimpleEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twin-Notes Editor")
        self.resize(500, 400)

        self.text_area = QTextEdit()
        self.save_btn = QPushButton("Save Note")
        self.save_btn.clicked.connect(self.save_file)

        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Note", "", "Text Files (*.txt)")
        if path:
            with open(path, "w") as f:
                f.write(self.text_area.toPlainText())