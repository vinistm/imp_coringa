import json
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QMessageBox, QListWidget,
                           QGroupBox, QFormLayout, QInputDialog)
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
        self.setWindowTitle("Configurações do Servidor")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        # Grupo de Configurações do Servidor
        server_group = QGroupBox("Configurações do Servidor")
        server_layout = QVBoxLayout()
        
        # Driver
        driver_layout = QVBoxLayout()
        driver_label = QLabel("Driver*")
        self.driver_input = QLineEdit()
        self.driver_input.setPlaceholderText("Ex: SQL Server")
        driver_layout.addWidget(driver_label)
        driver_layout.addWidget(self.driver_input)
        server_layout.addLayout(driver_layout)
        
        # Host
        host_layout = QVBoxLayout()
        host_label = QLabel("Host*")
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Ex: localhost")
        host_layout.addWidget(host_label)
        host_layout.addWidget(self.host_input)
        server_layout.addLayout(host_layout)
        
        # Porta (opcional)
        porta_layout = QVBoxLayout()
        porta_label = QLabel("Porta (opcional)")
        self.porta_input = QLineEdit()
        self.porta_input.setPlaceholderText("Ex: 1433")
        porta_layout.addWidget(porta_label)
        porta_layout.addWidget(self.porta_input)
        server_layout.addLayout(porta_layout)
        
        # Database
        database_layout = QVBoxLayout()
        database_label = QLabel("Database*")
        self.database_input = QLineEdit()
        self.database_input.setPlaceholderText("Ex: nome_banco")
        database_layout.addWidget(database_label)
        database_layout.addWidget(self.database_input)
        server_layout.addLayout(database_layout)
        
        # Username
        username_layout = QVBoxLayout()
        username_label = QLabel("Username*")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ex: sa")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        server_layout.addLayout(username_layout)
        
        # Password
        password_layout = QVBoxLayout()
        password_label = QLabel("Password*")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Digite a senha")
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        server_layout.addLayout(password_layout)
        
        server_group.setLayout(server_layout)
        layout.addWidget(server_group)
        
        # Grupo de Configurações da Filial
        filial_group = QGroupBox("Configurações da Filial")
        filial_layout = QVBoxLayout()
        
        # Lista de filiais
        self.filiais_list = QListWidget()
        self.filiais_list.setMinimumHeight(150)
        
        # Botões para gerenciar filiais
        filial_buttons = QHBoxLayout()
        
        self.add_filial_btn = QPushButton("Adicionar Filial")
        self.add_filial_btn.clicked.connect(self.add_filial)
        self.add_filial_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px;
                min-height: 30px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1976D2, stop:1 #1565C0);
                cursor: pointer;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1565C0, stop:1 #0D47A1);
            }
        """)
        
        self.remove_filial_btn = QPushButton("Remover Filial")
        self.remove_filial_btn.clicked.connect(self.remove_filial)
        self.remove_filial_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f44336, stop:1 #d32f2f);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px;
                min-height: 30px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d32f2f, stop:1 #b71c1c);
                cursor: pointer;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b71c1c, stop:1 #7f0000);
            }
        """)
        
        self.set_default_btn = QPushButton("Definir como Padrão")
        self.set_default_btn.clicked.connect(self.set_default_filial)
        self.set_default_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #45A049);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px;
                min-height: 30px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #45A049, stop:1 #3D8B40);
                cursor: pointer;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3D8B40, stop:1 #2E7D32);
            }
        """)
        
        filial_buttons.addWidget(self.add_filial_btn)
        filial_buttons.addWidget(self.remove_filial_btn)
        filial_buttons.addWidget(self.set_default_btn)
        
        filial_layout.addWidget(QLabel("Filiais Disponíveis:"))
        filial_layout.addWidget(self.filiais_list)
        filial_layout.addLayout(filial_buttons)
        
        filial_group.setLayout(filial_layout)
        layout.addWidget(filial_group)
        
        # Botões
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Salvar")
        save_button.clicked.connect(self.save_config)
        save_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #45A049);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px;
                min-height: 30px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #45A049, stop:1 #3D8B40);
                cursor: pointer;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3D8B40, stop:1 #2E7D32);
            }
        """)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f44336, stop:1 #d32f2f);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px;
                min-height: 30px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d32f2f, stop:1 #b71c1c);
                cursor: pointer;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b71c1c, stop:1 #7f0000);
            }
        """)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        # Carregar configurações existentes
        self.load_config()
        
        # Estilo
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
                color: #666;
                margin-bottom: 4px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #eee;
                border-radius: 8px;
                background-color: white;
                color: #333;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #999;
            }
            QGroupBox {
                border: 2px solid #eee;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
            }
            QGroupBox::title {
                color: #666;
                font-weight: bold;
            }
            QListWidget {
                border: 2px solid #eee;
                border-radius: 8px;
                padding: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #333;
            }
        """)
    
    def load_config(self):
        try:
            # Inicializar configuração padrão
            self.config = {
                "server": {
                    "driver": "",
                    "host": "",
                    "port": "",
                    "database": "",
                    "username": "",
                    "password": ""
                },
                "filial_padrao": "",
                "filiais_disponiveis": []
            }
            
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    self.config = config
                    self.driver_input.setText(config['server']['driver'])
                    self.host_input.setText(config['server']['host'])
                    self.porta_input.setText(str(config['server'].get('port', '')))
                    self.database_input.setText(config['server']['database'])
                    self.username_input.setText(config['server']['username'])
                    self.password_input.setText(config['server']['password'])
                    
                    # Carregar filiais
                    self.filiais_list.clear()
                    self.filiais_list.addItems(config.get('filiais_disponiveis', []))
                    
                    # Marcar filial padrão se existir
                    filial_padrao = config.get('filial_padrao', '')
                    if filial_padrao:
                        items = self.filiais_list.findItems(filial_padrao, Qt.MatchExactly)
                        if items:
                            self.filiais_list.setCurrentItem(items[0])
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar configurações: {str(e)}")
    
    def save_config(self):
        try:
            # Validar campos obrigatórios
            if not self.driver_input.text().strip():
                QMessageBox.warning(self, "Aviso", "Por favor, informe o driver!")
                return
            if not self.host_input.text().strip():
                QMessageBox.warning(self, "Aviso", "Por favor, informe o host!")
                return
            if not self.database_input.text().strip():
                QMessageBox.warning(self, "Aviso", "Por favor, informe o database!")
                return
            if not self.username_input.text().strip():
                QMessageBox.warning(self, "Aviso", "Por favor, informe o username!")
                return
            if not self.password_input.text().strip():
                QMessageBox.warning(self, "Aviso", "Por favor, informe a senha!")
                return
            
            # Criar objeto de configuração
            config = {
                'server': {
                    'driver': self.driver_input.text().strip(),
                    'host': self.host_input.text().strip(),
                    'database': self.database_input.text().strip(),
                    'username': self.username_input.text().strip(),
                    'password': self.password_input.text().strip()
                }
            }
            
            # Adicionar porta apenas se informada
            porta = self.porta_input.text().strip()
            if porta:
                config['server']['port'] = porta
            
            # Adicionar filiais
            filiais = []
            for i in range(self.filiais_list.count()):
                filiais.append(self.filiais_list.item(i).text())
            config['filiais_disponiveis'] = filiais
            
            # Adicionar filial padrão
            current = self.filiais_list.currentItem()
            if current:
                config['filial_padrao'] = current.text()
            
            # Salvar configuração
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar configurações: {str(e)}")
    
    def add_filial(self):
        filial, ok = QInputDialog.getText(self, "Adicionar Filial", "Digite o nome da filial:")
        if ok and filial.strip():
            if filial.strip() not in [self.filiais_list.item(i).text() for i in range(self.filiais_list.count())]:
                self.filiais_list.addItem(filial.strip())
            else:
                QMessageBox.warning(self, "Aviso", "Esta filial já existe!")
    
    def remove_filial(self):
        current = self.filiais_list.currentItem()
        if current:
            self.filiais_list.takeItem(self.filiais_list.row(current))
    
    def set_default_filial(self):
        current = self.filiais_list.currentItem()
        if current:
            self.config["filial_padrao"] = current.text()
            QMessageBox.information(self, "Sucesso", f"'{current.text()}' definida como filial padrão!") 