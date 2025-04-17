import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from main import ProdutoApp
from omni_app import OmniApp

class TelaInicial(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Coringa")
        self.setMinimumSize(800, 600)
        
        # Configurar ícone da janela
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logo.ico')
        if not os.path.exists(icon_path):
            # Se não encontrar no caminho absoluto, tenta no diretório atual
            icon_path = os.path.join('assets', 'logo.ico')
        self.setWindowIcon(QIcon(icon_path))
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        
        # Título
        titulo = QLabel("RFID")
        titulo.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 50px;
        """)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Botões
        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(50)
        botoes_layout.setAlignment(Qt.AlignCenter)
        
        # Botão Impressão Coringa
        self.btn_coringa = QPushButton("Impressão Coringa")
        self.btn_coringa.setMinimumSize(200, 100)
        self.btn_coringa.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1976D2, stop:1 #1565C0);
                
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1565C0, stop:1 #0D47A1);
            }
        """)
        self.btn_coringa.clicked.connect(self.abrir_coringa)
        
        # Botão Omni
        self.btn_omni = QPushButton("Omni")
        self.btn_omni.setMinimumSize(200, 100)
        self.btn_omni.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #45A049);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #45A049, stop:1 #3D8B40);
                
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3D8B40, stop:1 #2E7D32);
            }
        """)
        self.btn_omni.clicked.connect(self.abrir_omni)
        
        botoes_layout.addWidget(self.btn_coringa)
        botoes_layout.addWidget(self.btn_omni)
        
        layout.addLayout(botoes_layout)
        
        # Estilo da janela
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
        """)
    
    def abrir_coringa(self):
        self.coringa_app = ProdutoApp()
        self.coringa_app.show()
        self.hide()
    
    def abrir_omni(self):
        self.omni_app = OmniApp()
        self.omni_app.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TelaInicial()
    window.show()
    sys.exit(app.exec_()) 