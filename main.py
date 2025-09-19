from sys import argv
from PySide6.QtWidgets import QApplication

from interface.interface import Interface
from interface.styles import Styles

from modules.file_manager import FileManager
from modules.env_manager import EnvManager
from modules.tools import Tools

if __name__ == "__main__":
    FileManager.create_output_or_pass()
    EnvManager.create_env_or_pass()
    if argv:
        Tools()
    else:
        app = QApplication(argv)
        Styles.apply(app)

        window = Interface()
        window.show()
        exit(app.exec())