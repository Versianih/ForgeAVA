from sys import argv

from modules.tools import Tools

from PySide6.QtWidgets import QApplication
from interface.interface import Interface
from interface.styles import Styles

if __name__ == "__main__":    
    if len(argv) > 1:
        Tools()
    else:
        app = QApplication(argv)
        Styles.apply(app)

        window = Interface()
        window.show()
        exit(app.exec())