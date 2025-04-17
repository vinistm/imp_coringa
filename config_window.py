import json
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QMessageBox, QListWidget,
                           QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login de Configuração")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Campos de login
        form_layout = QFormLayout()
        
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        
        form_layout.addRow("Usuário:", self.username)
        form_layout.addRow("Senha:", self.password)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons = QHBoxLayout()
        self.login_btn = QPushButton("Login", self)
        self.cancel_btn = QPushButton("Cancelar", self)
        
        self.login_btn.clicked.connect(self.check_credentials)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(self.login_btn)
        buttons.addWidget(self.cancel_btn)
        
        layout.addLayout(buttons)
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                min-width: 300px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #eee;
                border-radius: 8px;
                margin: 5px;
            }
            QPushButton {
                padding: 8px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1E88E5);
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1E88E5, stop:1 #1976D2);
            }
        """)
    
    def check_credentials(self):
        if self.username.text() == "sa" and self.password.text() == "3864":
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos!")

class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurações")
        self.setModal(True)
        

        self.config = self.load_config()
        
        layout = QVBoxLayout(self)
        
        server_group = QGroupBox("Configurações do Servidor")
        server_layout = QFormLayout()
        
        self.host = QLineEdit(self.config["server"]["host"])
        self.port = QLineEdit(self.config["server"]["port"])
        self.database = QLineEdit(self.config["server"]["database"])
        self.username = QLineEdit(self.config["server"]["username"])
        self.password = QLineEdit(self.config["server"]["password"])
        
        server_layout.addRow("Host:", self.host)
        server_layout.addRow("Porta:", self.port)
        server_layout.addRow("Banco de Dados:", self.database)
        server_layout.addRow("Usuário:", self.username)
        server_layout.addRow("Senha:", self.password)
        
        server_group.setLayout(server_layout)
        layout.addWidget(server_group)
        
        # Grupo de Configurações da Filial
        filial_group = QGroupBox("Configurações da Filial")
        filial_layout = QVBoxLayout()
        
        # Lista de filiais
        self.filiais_list = QListWidget()
        self.filiais_list.addItems(self.config["filiais_disponiveis"])
        
        # Botões para gerenciar filiais
        filial_buttons = QHBoxLayout()
        self.add_filial_btn = QPushButton("Adicionar Filial")
        self.remove_filial_btn = QPushButton("Remover Filial")
        self.set_default_btn = QPushButton("Definir como Padrão")
        
        self.add_filial_btn.clicked.connect(self.add_filial)
        self.remove_filial_btn.clicked.connect(self.remove_filial)
        self.set_default_btn.clicked.connect(self.set_default_filial)
        
        filial_buttons.addWidget(self.add_filial_btn)
        filial_buttons.addWidget(self.remove_filial_btn)
        filial_buttons.addWidget(self.set_default_btn)
        
        filial_layout.addWidget(QLabel("Filiais Disponíveis:"))
        filial_layout.addWidget(self.filiais_list)
        filial_layout.addLayout(filial_buttons)
        
        filial_group.setLayout(filial_layout)
        layout.addWidget(filial_group)
        

        buttons = QHBoxLayout()
        self.save_btn = QPushButton("Salvar")
        self.cancel_btn = QPushButton("Cancelar")
        
        self.save_btn.clicked.connect(self.save_config)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)
        
        layout.addLayout(buttons)
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                min-width: 500px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #eee;
                border-radius: 8px;
                margin: 5px;
            }
            QPushButton {
                padding: 8px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1E88E5);
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                min-width: 100px;
                margin: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1E88E5, stop:1 #1976D2);
            }
            QGroupBox {
                border: 2px solid #eee;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
            }
            QListWidget {
                border: 2px solid #eee;
                border-radius: 8px;
                padding: 5px;
                min-height: 150px;
            }
        """)
    
    @staticmethod
    def load_config():
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                return json.load(f)
        return {
            "server": {
                "driver": "SQL Server",
                "host": "",
                "port": "",
                "database": "",
                "username": "",
                "password": ""
            },
            "filial_padrao": "",
            "filiais_disponiveis": []
        }
    
    def add_filial(self):
        filial = QLineEdit()
        filial.setPlaceholderText("Digite o nome da filial")
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Adicionar Filial")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Nome da Filial:"))
        layout.addWidget(filial)
        
        buttons = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancelar")
        
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)
        
        if dialog.exec_() == QDialog.Accepted and filial.text().strip():
            self.filiais_list.addItem(filial.text().strip())
    
    def remove_filial(self):
        current = self.filiais_list.currentItem()
        if current:
            self.filiais_list.takeItem(self.filiais_list.row(current))
    
    def set_default_filial(self):
        current = self.filiais_list.currentItem()
        if current:
            self.config["filial_padrao"] = current.text()
            QMessageBox.information(self, "Sucesso", f"'{current.text()}' definida como filial padrão!")
    
    def save_config(self):
        # Atualizar configurações do servidor
        self.config["server"]["host"] = self.host.text()
        self.config["server"]["port"] = self.port.text()
        self.config["server"]["database"] = self.database.text()
        self.config["server"]["username"] = self.username.text()
        self.config["server"]["password"] = self.password.text()
        
        # Atualizar lista de filiais
        filiais = []
        for i in range(self.filiais_list.count()):
            filiais.append(self.filiais_list.item(i).text())
        self.config["filiais_disponiveis"] = filiais
        
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)
        
        QMessageBox.information(self, "Sucesso", "Configurações salvas com sucesso!")
        self.accept() 