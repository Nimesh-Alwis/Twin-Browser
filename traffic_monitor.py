from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

class TrafficMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twin-Browser: Network Traffic Monitor")
        self.resize(800, 400)

        # 1. Futuristic Vivaldi Purple Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #140b24;
                color: #f3e8ff;
                font-family: 'Consolas', 'Segoe UI Monospace', monospace;
            }
            QTableWidget {
                background-color: #1a0e30;
                color: #e9d5ff;
                gridline-color: rgba(192, 132, 252, 0.15);
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #251442;
                color: #c084fc;
                padding: 6px;
                border: 1px solid rgba(192, 132, 252, 0.2);
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #a855f7;
                color: #140b24;
            }
        """)

        # දත්ත පෙන්වීමට Table එකක් සකසමු
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Method", "Status", "URL"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def add_log(self, method, status, url):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(method))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(status)))
        self.table.setItem(row_position, 2, QTableWidgetItem(url))
        
        # අලුත්ම log එක පේන විදිහට පල්ලෙහාට scroll කිරීම
        self.table.scrollToBottom()