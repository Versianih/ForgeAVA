from sys import argv
from PySide6.QtWidgets import QApplication

from interface.interface import Interface
from interface.styles import Styles

if __name__ == "__main__":
    app = QApplication(argv)
    Styles.apply(app)

    window = Interface()
    window.show()
    exit(app.exec())