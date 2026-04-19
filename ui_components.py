from PyQt6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget

class NavigationBar(QWidget): # අපි දැන් මේවා එකට එකතු කරලා "Bar" එකක් හදමු
    def __init__(self, browser_engine):
        super().__init__()
        self.engine = browser_engine

        # බොත්තම් සෑදීම
        self.back_btn = QPushButton("<")
        self.forward_btn = QPushButton(">")
        self.reload_btn = QPushButton("R")
        self.address_bar = QLineEdit()

        # බොත්තම් වලට වැඩ පැවරීම (Signals & Slots)
        self.back_btn.clicked.connect(self.engine.back)
        self.forward_btn.clicked.connect(self.engine.forward)
        self.reload_btn.clicked.connect(self.engine.reload)
        self.address_bar.returnPressed.connect(self.navigate)

        # Layout එක සැකසීම (බොත්තම් පේළියට තැබීම)
        layout = QHBoxLayout()
        layout.addWidget(self.back_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.reload_btn)
        layout.addWidget(self.address_bar)
        
        self.setLayout(layout)

    def navigate(self):
        url = self.address_bar.text()
        self.engine.load_new_url(url)