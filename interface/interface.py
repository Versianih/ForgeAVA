from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QHBoxLayout, QStackedWidget, QLabel
)
from PySide6.QtCore import Qt

from interface.ava_activity import AvaActivityInterface
from interface.prompt_generator import PromptGeneratorInterface
from interface.generated_files import GeneratedFilesInterface
from interface.settings import SettingsInterface
from interface.help import HelpInterface
from interface.styles import Styles


class Interface(QMainWindow, Styles):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ForgeAVA")
        self.setGeometry(100, 100, 1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        self.sidebar = QVBoxLayout()
        self.sidebar.setAlignment(Qt.AlignTop)

        self.btn1 = QPushButton("Gerar código de atividade AVA")
        self.btn2 = QPushButton("Gerar código por prompt")
        self.btn3 = QPushButton("Códigos Gerados")
        self.btn4 = QPushButton("Configurações")
        self.btn5 = QPushButton("Ajuda")
        self.btn_exit = QPushButton("Sair")

        for b in [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn_exit]:
            b.setObjectName("sidebarButton")

        self.sidebar.addWidget(self.btn1)
        self.sidebar.addWidget(self.btn2)
        self.sidebar.addWidget(self.btn3)
        self.sidebar.addWidget(self.btn4)
        self.sidebar.addWidget(self.btn5)
        self.sidebar.addStretch()
        self.sidebar.addWidget(QLabel('ForgeAVA'))
        self.sidebar.addWidget(self.btn_exit)

        self.stack = QStackedWidget()
        self.stack.addWidget(AvaActivityInterface())
        self.stack.addWidget(PromptGeneratorInterface())
        self.stack.addWidget(GeneratedFilesInterface())
        self.stack.addWidget(SettingsInterface())
        self.stack.addWidget(HelpInterface())

        layout.addLayout(self.sidebar, 1)
        layout.addWidget(self.stack, 4)

        self.btn1.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn2.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn3.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn4.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        self.btn5.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        self.btn_exit.clicked.connect(self.close)