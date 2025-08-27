from PySide6.QtWidgets import QApplication

class Styles:
    @staticmethod
    def apply(app: QApplication):
        app.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #f0f0f0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }

            QVBoxLayout, QHBoxLayout {
                background-color: transparent;
            }

            QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {
                background-color: #2a2a3d;
                border: 1px solid #3a3a5c;
                border-radius: 6px;
                padding: 6px;
                color: #f0f0f0;
            }

            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {
                border: 1px solid #5c7cfa;
                outline: none;
            }

            QPushButton {
                background-color: #2a2a3d;
                border: 1px solid #3a3a5c;
                border-radius: 8px;
                padding: 8px 12px;
                text-align: center;
            }

            QPushButton:hover {
                background-color: #3a3a5c;
            }

            QPushButton:pressed {
                background-color: #5c7cfa;
            }

            QPushButton#sidebarButton {
                background-color: #252538;
                border: none;
                text-align: left;
                padding: 12px;
            }

            QPushButton#sidebarButton:hover {
                background-color: #3a3a5c;
            }

            QListWidget {
                background-color: #2a2a3d;
                border: 1px solid #3a3a5c;
                border-radius: 6px;
                padding: 6px;
            }

            QListWidget::item:selected {
                background-color: #5c7cfa;
                color: white;
            }
        """)
