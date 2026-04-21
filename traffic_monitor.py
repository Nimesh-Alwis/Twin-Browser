from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

class TrafficMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twin-Browser: Network Traffic Monitor")
        self.resize(800, 400)

        # 1. Style එක Class එක ඇතුළේදී apply කිරීම
        self.setStyleSheet("""
            QTableWidget {
                background-color: #0d0d0d;
                color: #00ff41;
                gridline-color: #ff00ff;
                border: 1px solid #00ffff;
                font-family: 'Courier New', monospace;
            }
            QHeaderView::section {
                background-color: #1a1a1a;
                color: #ff00ff;
                padding: 5px;
                border: 1px solid #00ffff;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #ff00ff;
                color: #000000;
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