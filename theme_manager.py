import os
import json
import shutil
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QComboBox, QFileDialog, QColorDialog, QMessageBox, QApplication)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor
from path_utils import get_data_path

CONFIG_FILE = get_data_path("theme_config.json")

PRESETS = {
    "Vivaldi Sunset (Default)": {
        "bg": "#140b24",
        "card": "#23143c",
        "input": "#261642",
        "accent": "#a855f7",
        "highlight": "#c084fc",
        "text": "#f3e8ff",
        "wallpaper": "purple_sunset_wallpaper.png"
    },
    "Cyberpunk Blue": {
        "bg": "#0b132b",
        "card": "#1c2541",
        "input": "#243256",
        "accent": "#00f5d4",
        "highlight": "#4cc9f0",
        "text": "#e0fbfc",
        "wallpaper": "cyber"
    },
    "Emerald Hacker": {
        "bg": "#06140e",
        "card": "#0f291e",
        "input": "#173c2c",
        "accent": "#10b981",
        "highlight": "#34d399",
        "text": "#d1fae5",
        "wallpaper": "aurora"
    },
    "Sunset Rose Gold": {
        "bg": "#1c0d18",
        "card": "#2e1528",
        "input": "#3e1d37",
        "accent": "#f43f5e",
        "highlight": "#fb7185",
        "text": "#ffe4e6",
        "wallpaper": "purple_sunset_wallpaper.png"
    }
}

class ThemeManager:
    @staticmethod
    def load_config():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return PRESETS["Vivaldi Sunset (Default)"]

    @staticmethod
    def save_config(config_data):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(config_data, f, indent=4)
        except Exception as e:
            print(f"Error saving theme config: {e}")

    @staticmethod
    def generate_qss(config):
        bg = config.get("bg", "#140b24")
        card = config.get("card", "#23143c")
        input_bg = config.get("input", "#261642")
        accent = config.get("accent", "#a855f7")
        highlight = config.get("highlight", "#c084fc")
        text = config.get("text", "#f3e8ff")

        return f"""
QMainWindow {{
    background-color: {bg};
}}

QWidget {{
    background-color: {bg};
    color: {text};
    font-family: 'Segoe UI', 'Segoe UI Emoji', sans-serif;
    font-size: 13px;
}}

/* Tab Widget & Tab Bar */
QTabWidget::pane {{
    border: none;
    background-color: {bg};
}}

QTabBar::tab {{
    background-color: {card};
    color: {text};
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: none;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 7px 16px;
    min-width: 110px;
    max-width: 220px;
    margin-right: 3px;
    font-weight: 500;
}}

QTabBar::tab:selected {{
    background-color: {input_bg};
    color: #ffffff;
    font-weight: 600;
    border: 1px solid {highlight};
    border-bottom: 2.5px solid {accent};
}}

QTabBar::tab:hover:!selected {{
    background-color: {card};
    color: {text};
}}

/* Address Bar / Input Fields */
QLineEdit {{
    background-color: {input_bg};
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 7px 16px;
    color: {text};
    selection-background-color: {accent};
    font-size: 13px;
}}

QLineEdit:focus {{
    border: 1.5px solid {highlight};
    background-color: {card};
}}

/* Navigation & Action Buttons */
QPushButton {{
    background-color: {card};
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    padding: 6px 14px;
    color: {text};
    font-weight: 600;
}}

QPushButton:hover {{
    background-color: {input_bg};
    border: 1px solid {highlight};
    color: #ffffff;
}}

QPushButton:pressed {{
    background-color: {accent};
    color: {bg};
}}

/* ComboBox Styling */
QComboBox {{
    background-color: {card};
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    padding: 6px 12px;
    color: {text};
    font-weight: 500;
}}

QComboBox:hover {{
    border: 1px solid {highlight};
}}

QComboBox QAbstractItemView {{
    background-color: {card};
    border: 1px solid {highlight};
    selection-background-color: {accent};
    color: {text};
    padding: 4px;
    border-radius: 8px;
}}

/* Progress Bar */
QProgressBar {{
    background-color: {card};
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    text-align: center;
    color: {text};
    height: 16px;
}}

QProgressBar::chunk {{
    background-color: {accent};
    border-radius: 7px;
}}

/* Scrollbars */
QScrollBar:vertical {{
    background: {bg};
    width: 10px;
    margin: 0px;
}}
QScrollBar::handle:vertical {{
    background: {card};
    min-height: 20px;
    border-radius: 5px;
}}
QScrollBar::handle:vertical:hover {{
    background: {accent};
}}
"""


class ThemeDialog(QWidget):
    theme_updated_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 Custom Theme & Wallpaper Customizer")
        self.resize(520, 560)

        self.current_config = ThemeManager.load_config()

        # UI Components
        self.preset_label = QLabel("🎨 Select Theme Preset:")
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(list(PRESETS.keys()))
        self.preset_combo.currentTextChanged.connect(self.apply_preset)

        # Custom Colors Section
        self.color_sec_label = QLabel("🛠️ Custom Color Controls:")
        
        self.bg_btn = QPushButton("Change Background Color")
        self.bg_btn.clicked.connect(lambda: self.pick_color("bg"))

        self.card_btn = QPushButton("Change Card / Control Color")
        self.card_btn.clicked.connect(lambda: self.pick_color("card"))

        self.accent_btn = QPushButton("Change Accent Highlight Color")
        self.accent_btn.clicked.connect(lambda: self.pick_color("accent"))

        # Wallpaper Section
        self.wp_sec_label = QLabel("🖼️ Startpage Wallpaper Customization:")
        self.wp_path_label = QLabel(f"Current: {os.path.basename(self.current_config.get('wallpaper', 'Default'))}")
        self.wp_path_label.setStyleSheet("color: #b8a2d1; font-size: 11px;")

        self.browse_wp_btn = QPushButton("📁 Browse Local Drive Wallpaper")
        self.browse_wp_btn.clicked.connect(self.browse_wallpaper)

        # Save Button
        self.save_btn = QPushButton("💾 Save & Apply Theme")
        self.save_btn.setStyleSheet("background-color: #a855f7; color: #ffffff; font-size: 14px; font-weight: bold; padding: 10px;")
        self.save_btn.clicked.connect(self.save_and_apply)

        # Apply Styling to Dialog
        self.setStyleSheet("""
            QWidget {
                background-color: #140b24;
                color: #f3e8ff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-weight: 600;
                font-size: 13px;
                color: #c084fc;
            }
            QPushButton {
                background-color: #251442;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 10px;
                padding: 9px 14px;
                color: #f3e8ff;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #381c63;
                border: 1px solid #c084fc;
            }
            QComboBox {
                background-color: #251442;
                border: 1px solid rgba(192, 132, 252, 0.3);
                border-radius: 10px;
                padding: 8px 12px;
            }
        """)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        layout.addWidget(self.preset_label)
        layout.addWidget(self.preset_combo)

        layout.addSpacing(10)
        layout.addWidget(self.color_sec_label)
        layout.addWidget(self.bg_btn)
        layout.addWidget(self.card_btn)
        layout.addWidget(self.accent_btn)

        layout.addSpacing(10)
        layout.addWidget(self.wp_sec_label)
        layout.addWidget(self.wp_path_label)
        layout.addWidget(self.browse_wp_btn)

        layout.addStretch()
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def apply_preset(self, preset_name):
        if preset_name in PRESETS:
            self.current_config = PRESETS[preset_name].copy()
            self.wp_path_label.setText(f"Current: {os.path.basename(self.current_config.get('wallpaper', 'Default'))}")

    def pick_color(self, key):
        current_hex = self.current_config.get(key, "#140b24")
        color = QColorDialog.getColor(QColor(current_hex), self, f"Select {key.upper()} Color")
        if color.isValid():
            self.current_config[key] = color.name()
            if key == "accent":
                self.current_config["highlight"] = color.lighter(120).name()
            elif key == "bg":
                self.current_config["input"] = color.lighter(130).name()

    def browse_wallpaper(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Local Wallpaper Image", 
            "", 
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )
        if file_path:
            # Copy wallpaper to workspace for reliable loading
            ext = os.path.splitext(file_path)[1]
            dest_name = f"custom_wallpaper{ext}"
            dest_path = get_data_path(dest_name)
            try:
                shutil.copy(file_path, dest_path)
                self.current_config["wallpaper"] = dest_path
                self.wp_path_label.setText(f"Current Local Wallpaper: {os.path.basename(file_path)}")
                QMessageBox.information(self, "Wallpaper Updated", f"Selected local wallpaper: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to set wallpaper: {e}")

    def save_and_apply(self):
        ThemeManager.save_config(self.current_config)
        self.theme_updated_signal.emit(self.current_config)
        QMessageBox.information(self, "Success", "Theme and Wallpaper saved successfully!")
