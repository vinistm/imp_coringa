import sys
import pyodbc
import uuid
import time
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QTableWidget, QTableWidgetItem, QMessageBox, QComboBox,
                           QGroupBox, QStackedWidget, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from config_window import LoginDialog, ConfigWindow

class ProdutoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RFID Coringa")
        self.setMinimumSize(1024, 860) 
        
        # Carregar configurações
        self.load_config()
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
                color: #666;
                margin-bottom: 4px;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 2px solid #eee;
                border-radius: 8px;
                background-color: white;
                color: #333;
                min-width: 180px;
                max-width: 300px;
                font-size: 12px;
                margin-bottom: 8px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #2196F3;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #999;
            }
            QComboBox {
                padding-right: 20px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(down-arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #eee;
                border-radius: 8px;
                padding: 5px;
                background-color: white;
                selection-background-color: #e3f2fd;
                selection-color: #333;
            }
            QComboBox QAbstractItemView::item {
                padding: 5px;
                min-height: 20px;
            }
            QPushButton {
                padding: 8px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1E88E5);
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                font-size: 12px;
                min-width: 120px;
                max-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1E88E5, stop:1 #1976D2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1976D2, stop:1 #1565C0);
            }
            QTableWidget {
                border: 2px solid #eee;
                border-radius: 8px;
                background-color: white;
                color: #333;
                gridline-color: #eee;
                min-height: 200px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #eee;
                color: #666;
                font-weight: bold;
                font-size: 12px;
            }
            QGroupBox {
                border: 2px solid #eee;
                border-radius: 12px;
                margin-top: 15px;
                padding: 15px;
                background-color: white;
                color: #333;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                color: #666;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        
        config_button = QPushButton("⚙️ Configurações")
        config_button.setFixedWidth(120)
        config_button.clicked.connect(self.show_config)
        config_button.setStyleSheet("""
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
               
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1565C0, stop:1 #0D47A1);
            }
        """)
        
        # Adicionar o botão ao layout principal
        title_layout = QHBoxLayout()
        title_layout.addStretch()
        title_layout.addWidget(config_button)
        layout.insertLayout(0, title_layout)
        
        titulo = QLabel("Impressão coringa")
        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 20px;
            font-family: 'Segoe UI', sans-serif;
        """)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        self.stacked_widget = QStackedWidget()
        
        busca_simples = QWidget()
        busca_simples_layout = QVBoxLayout(busca_simples)
        busca_simples_layout.setSpacing(10)
        
        grupo_simples = QGroupBox("Busca por Código de Barras")
        grupo_simples_layout = QVBoxLayout(grupo_simples)
        grupo_simples_layout.setSpacing(10)
        
        campos_widget = QWidget()
        campos_layout = QHBoxLayout(campos_widget)
        campos_layout.setSpacing(10)
        campos_layout.setContentsMargins(0, 0, 0, 0)
        
        # Código de Barras
        codigo_layout = QVBoxLayout()
        codigo_label = QLabel("Código de Barras*")
        self.codigo_input = QLineEdit()
        self.codigo_input.setPlaceholderText("Digite ou leia o código de barras")
        self.codigo_input.setMinimumWidth(200)
        self.codigo_input.setMinimumHeight(40)
        self.codigo_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        codigo_layout.addWidget(codigo_label)
        codigo_layout.addWidget(self.codigo_input)
        campos_layout.addLayout(codigo_layout)
        
        # Caso precise alterar alguma filial ou adicionar
        filial_layout = QVBoxLayout()
        filial_label = QLabel("Filial*")
        self.filial_combo = QComboBox()
        self.filial_combo.setMinimumWidth(200)
        self.filial_combo.setMinimumHeight(40)
        self.filial_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.filial_combo.addItems(self.filiais)
        filial_layout.addWidget(filial_label)
        filial_layout.addWidget(self.filial_combo)
        campos_layout.addLayout(filial_layout)
        
        grupo_simples_layout.addWidget(campos_widget)
        
        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(10)
        botoes_layout.setAlignment(Qt.AlignCenter)
        
        self.buscar_simples_button = QPushButton("Buscar")
        self.buscar_simples_button.clicked.connect(self.buscar_por_codigo)
        botoes_layout.addWidget(self.buscar_simples_button)
        
        grupo_simples_layout.addLayout(botoes_layout)
        busca_simples_layout.addWidget(grupo_simples)
        
        grupo_rfid = QGroupBox("Vinculação RFID")
        grupo_rfid_layout = QVBoxLayout(grupo_rfid)
        grupo_rfid_layout.setSpacing(10)
        
        rfid_container = QWidget()
        rfid_container_layout = QHBoxLayout(rfid_container)
        rfid_container_layout.setContentsMargins(0, 0, 0, 0)
        
        rfid_layout = QVBoxLayout()
        rfid_label = QLabel("Código RFID*")
        self.rfid_input = QLineEdit()
        self.rfid_input.setPlaceholderText("Digite ou leia o código RFID")
        self.rfid_input.setMinimumHeight(40)
        rfid_layout.addWidget(rfid_label)
        rfid_layout.addWidget(self.rfid_input)
        rfid_container_layout.addLayout(rfid_layout)
        
        grupo_rfid_layout.addWidget(rfid_container)
        
        rfid_button_layout = QHBoxLayout()
        rfid_button_layout.setAlignment(Qt.AlignCenter)
        self.vincular_rfid_button = QPushButton("Vincular RFID")
        self.vincular_rfid_button.clicked.connect(self.vincular_rfid)
        self.vincular_rfid_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #45A049);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #45A049, stop:1 #3D8B40);
            }
        """)
        rfid_button_layout.addWidget(self.vincular_rfid_button)
        grupo_rfid_layout.addLayout(rfid_button_layout)
        
        busca_simples_layout.addWidget(grupo_rfid)
        
        busca_avancada = QWidget()
        busca_avancada_layout = QVBoxLayout(busca_avancada)
        busca_avancada_layout.setSpacing(15)
        
        grupo_avancado = QGroupBox("Busca Avançada")
        grupo_avancado_layout = QVBoxLayout(grupo_avancado)
        grupo_avancado_layout.setSpacing(15)
        
        form_avancado = QHBoxLayout()
        form_avancado.setSpacing(20)
        
        # Produto
        produto_layout = QVBoxLayout()
        produto_label = QLabel("Produto*")
        self.produto_input = QLineEdit()
        self.produto_input.setMinimumWidth(200)
        self.produto_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        produto_layout.addWidget(produto_label)
        produto_layout.addWidget(self.produto_input)
        form_avancado.addLayout(produto_layout)
        
        # Cor Produto
        cor_layout = QVBoxLayout()
        cor_label = QLabel("Cor Produto")
        self.cor_input = QLineEdit()
        self.cor_input.setMinimumWidth(200)
        self.cor_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        cor_layout.addWidget(cor_label)
        cor_layout.addWidget(self.cor_input)
        form_avancado.addLayout(cor_layout)
        
        # Tamanho
        tamanho_layout = QVBoxLayout()
        tamanho_label = QLabel("Tamanho")
        self.tamanho_input = QLineEdit()
        self.tamanho_input.setMinimumWidth(200)
        self.tamanho_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        tamanho_layout.addWidget(tamanho_label)
        tamanho_layout.addWidget(self.tamanho_input)
        form_avancado.addLayout(tamanho_layout)
        
        # Filial (na busca avançada)
        filial_avancada_layout = QVBoxLayout()
        filial_avancada_label = QLabel("Filial*")
        self.filial_avancada_combo = QComboBox()
        self.filial_avancada_combo.setMinimumWidth(200)
        self.filial_avancada_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.filial_avancada_combo.addItems(self.filiais)
        filial_avancada_layout.addWidget(filial_avancada_label)
        filial_avancada_layout.addWidget(self.filial_avancada_combo)
        form_avancado.addLayout(filial_avancada_layout)
        
        grupo_avancado_layout.addLayout(form_avancado)
        
        self.buscar_avancada_button = QPushButton("Buscar")
        self.buscar_avancada_button.clicked.connect(self.buscar_avancada)
        grupo_avancado_layout.addWidget(self.buscar_avancada_button)
        
        busca_avancada_layout.addWidget(grupo_avancado)
        
        self.stacked_widget.addWidget(busca_simples)
        self.stacked_widget.addWidget(busca_avancada)
        
        # Botão para trocar tipo de busca
        self.trocar_busca_button = QPushButton("Alternar para Busca Avançada")
        self.trocar_busca_button.clicked.connect(self.trocar_tipo_busca)
        self.trocar_busca_button.setStyleSheet("background-color: #4CAF50;")
        
        layout.addWidget(self.stacked_widget)
        layout.addWidget(self.trocar_busca_button)
        
        grupo_resultados = QGroupBox("Resultados")
        resultados_layout = QVBoxLayout(grupo_resultados)
        
        # Tabela de resultados
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Descrição", "Filial", "Estoque", "SKU"])
        
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)  
        
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, header.ResizeToContents) 
        header.setMinimumSectionSize(300)  
        header.setSectionResizeMode(1, header.Fixed)  # Filial
        header.setSectionResizeMode(2, header.Fixed)  # Quantidade
        header.setSectionResizeMode(3, header.Fixed)  # SKU
        
        self.tabela.setColumnWidth(1, 150)  # Filial
        self.tabela.setColumnWidth(2, 100)  # Quantidade
        self.tabela.setColumnWidth(3, 150)  # SKU
        
        self.tabela.setWordWrap(True)
        self.tabela.setTextElideMode(Qt.ElideNone)
        
        self.tabela.verticalHeader().setSectionResizeMode(header.ResizeToContents)
        
        self.tabela.setStyleSheet("""
            QTableWidget {
                border: 2px solid #eee;
                border-radius: 8px;
                background-color: white;
                color: #333;
                gridline-color: #eee;
                min-height: 200px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
                min-height: 30px;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #333;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #eee;
                color: #666;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        
        resultados_layout.addWidget(self.tabela)
        layout.addWidget(grupo_resultados)
        
        self.produto_atual = None
        self.cor_atual = None
        self.tamanho_atual = None
        self.codigo_barra_atual = None
        
    def trocar_tipo_busca(self):
        if self.stacked_widget.currentIndex() == 0:
            self.stacked_widget.setCurrentIndex(1)
            self.trocar_busca_button.setText("Voltar para Busca Simples")
            self.trocar_busca_button.setStyleSheet("background-color: #2196F3;")
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.trocar_busca_button.setText("Alternar para Busca Avançada")
            self.trocar_busca_button.setStyleSheet("background-color: #4CAF50;")
    
    def buscar_por_codigo(self):
        try:
            self.tabela.setRowCount(0)
            
            if not self.codigo_input.text().strip():
                QMessageBox.warning(self, "Aviso", "Por favor, informe o código de barras!")
                return
            
            print("Tentando conectar ao banco de dados...")
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            
            codigo = self.codigo_input.text().strip()
            filial = self.filial_combo.currentText()
            
            print(f"Valores da consulta: Código={codigo}, Filial={filial}")
            
            query = """
            SELECT 
                pb.CODIGO_BARRA,
                pb.PRODUTO,
                c.DESC_PRODUTO,
                pb.COR_PRODUTO,
                pb.TAMANHO,
                pb.GRADE,
                ep.FILIAL,
                CASE 
                    WHEN pb.TAMANHO = 1 THEN ep.ES1
                    WHEN pb.TAMANHO = 2 THEN ep.ES2
                    WHEN pb.TAMANHO = 3 THEN ep.ES3
                    WHEN pb.TAMANHO = 4 THEN ep.ES4
                    WHEN pb.TAMANHO = 5 THEN ep.ES5
                    WHEN pb.TAMANHO = 6 THEN ep.ES6
                    WHEN pb.TAMANHO = 7 THEN ep.ES7
                    ELSE NULL
                END AS ESTOQUE_TAMANHO,
                pb.CODIGO_BARRA_PADRAO
            FROM produtos_barra pb
            JOIN estoque_produtos ep ON pb.PRODUTO = ep.PRODUTO AND pb.COR_PRODUTO = ep.COR_PRODUTO
            JOIN PRODUTOS c ON c.PRODUTO = pb.PRODUTO AND c.PRODUTO = ep.PRODUTO
            WHERE TIPO_COD_BAR = '4'
            AND pb.CODIGO_BARRA = ?
            AND ep.FILIAL = ?
            """
            
            print("Executando a consulta...")
            cursor.execute(query, (codigo, filial))
            
            resultados = cursor.fetchall()
            print(f"Número de resultados encontrados: {len(resultados)}")
            
            if len(resultados) == 0:
                QMessageBox.information(self, "Informação", "Nenhum resultado encontrado para os critérios informados.")
                return
            
            self.produto_atual = resultados[0][1]  # PRODUTO
            self.cor_atual = resultados[0][3]      # COR_PRODUTO
            self.tamanho_atual = resultados[0][4]   # TAMANHO
            self.codigo_barra_atual = resultados[0][0]  # CODIGO_BARRA
            
            self.tabela.setRowCount(len(resultados))
            for i, row in enumerate(resultados):
                self.tabela.setItem(i, 0, QTableWidgetItem(str(row[2])))  # DESC_PRODUTO
                self.tabela.setItem(i, 1, QTableWidgetItem(str(row[6])))  # FILIAL
                self.tabela.setItem(i, 2, QTableWidgetItem(str(row[7])))  # ESTOQUE_TAMANHO
                self.tabela.setItem(i, 3, QTableWidgetItem(str(row[0])))  # CODIGO_BARRA
            
            conn.close()
            
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", 
                               f"Erro ao conectar ou consultar o banco de dados: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar produto: {str(e)}")
    
    def vincular_rfid(self):
        try:
            if not self.rfid_input.text().strip():
                QMessageBox.warning(self, "Aviso", "Por favor, informe o código RFID!")
                return
            
            print("Tentando conectar ao banco de dados...")
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            
            novo_uuid = str(uuid.uuid4()).upper()
            print(f"UUID gerado: {novo_uuid}")
            
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print(f"Data atual: {data_atual}")
            
            filial = self.filial_combo.currentText()
            cursor.execute("SELECT codigo_filial FROM lojas_varejo WHERE filial = ?", (filial,))
            resultado = cursor.fetchone()
            
            if not resultado:
                raise Exception(f"Código da filial não encontrado para: {filial}")
                
            codigo_filial = resultado[0]
            print(f"Código da filial: {codigo_filial}")
            
            chave = f"ORDEM_PRODUCAO=[{self.rfid_input.text().strip()}] FILIAL=[{filial}] Usuario: CORINGA"
            print(f"Chave montada: {chave}")
            
            try:
                # 1. Inserir na tabela MEGA_EPC_MOV
                print("\n1. Inserindo na tabela MEGA_EPC_MOV...")
                cursor.execute("""
                    INSERT INTO MEGA_EPC_MOV 
                    (TIPO, ID_ORIGEM, TRANSACAO, TABELA_PAI, CHAVE, DATA_MOV, ATUALIZACAO, COD_FILIAL, NAO_ATUALIZA_TIPO)
                    VALUES ('I', ?, 'MEG002', 'IMPRESSAO', ?, ?, ?, ?, '0')
                """, (novo_uuid, chave, data_atual, data_atual, codigo_filial))
                
                conn.commit()
                print("✓ Insert na MEGA_EPC_MOV realizado com sucesso!")
                
                # Aguardar 1 segundo
                time.sleep(1)
                
                try:
                    # 2. Inserir na tabela MEGA_EPC
                    print("\n2. Inserindo na tabela MEGA_EPC...")
                    epc_valor = self.rfid_input.text().strip()
                    print(f"Valor do EPC a ser inserido: {epc_valor}")
                    
                    # Primeiro busca o próximo ID disponível
                    cursor.execute("SELECT ISNULL(MAX(ID_EPC), 0) + 1 FROM MEGA_EPC")
                    proximo_id = cursor.fetchval()
                    
                    # Faz o insert com ID_EPC e EPC
                    cursor.execute("INSERT INTO MEGA_EPC (ID_EPC, EPC) VALUES (?, ?)", 
                                 (proximo_id, epc_valor))
                    conn.commit()
                    
                    novo_id_epc = proximo_id
                    print(f"✓ Insert na MEGA_EPC realizado com sucesso! ID_EPC gerado: {novo_id_epc}")

                    if novo_id_epc is None:
                        raise Exception("Erro: ID_EPC não foi gerado corretamente")
                    
                    # Aguardar 1 segundo
                    time.sleep(1)
                    
                    try:
                        # 3. Inserir na tabela MEGA_EPC_MOV_ITEM
                        print("\n3. Inserindo na tabela MEGA_EPC_MOV_ITEM...")
                        cursor.execute("""
                            INSERT INTO MEGA_EPC_MOV_ITEM (ID_EPC, ID_ORIGEM)
                            VALUES (?, ?)
                        """, (novo_id_epc, novo_uuid))
                        
                        conn.commit()
                        print("✓ Insert na MEGA_EPC_MOV_ITEM realizado com sucesso!")
                        
                        # Aguardar 1 segundo
                        time.sleep(1)
                        
                        try:
                            # 4. Inserir na tabela MEGA_EPC_DETALHE
                            print("\n4. Inserindo na tabela MEGA_EPC_DETALHE...")
                            
                            # Buscar o código de barras padrão
                            cursor.execute("""
                                SELECT CODIGO_BARRA 
                                FROM produtos_barra 
                                WHERE PRODUTO = ? 
                                AND COR_PRODUTO = ? 
                                AND TAMANHO = ?
                                AND TIPO_COD_BAR = ?
                            """, (self.produto_atual, self.cor_atual, self.tamanho_atual, 
                                 '3' if any(c.isalpha() for c in self.codigo_barra_atual) else '4'))
                            
                            resultado = cursor.fetchone()
                            
                            if not resultado:
                                raise Exception(f"Código de barras padrão não encontrado para: Produto={self.produto_atual}, Cor={self.cor_atual}, Tamanho={self.tamanho_atual}")
                                
                            codigo_barra_padrao = resultado[0]
                            print(f"Código de barras padrão encontrado: {codigo_barra_padrao}")
                            
                            cursor.execute("""
                                INSERT INTO MEGA_EPC_DETALHE 
                                (ID_EPC, PRODUTO, COR_PRODUTO, TAMANHO, MATERIAL, COR_MATERIAL, 
                                 EAN13, SERIAL, ATUALIZACAO, COD_FILIAL, ULTIMO_TIPO_MOV, INATIVO)
                                VALUES (?, ?, ?, ?, NULL, NULL, ?, '1', ?, ?, 'I', '0')
                            """, (novo_id_epc, self.produto_atual, self.cor_atual, self.tamanho_atual, 
                                 codigo_barra_padrao, data_atual, codigo_filial))
                            
                            conn.commit()
                            print("✓ Insert na MEGA_EPC_DETALHE realizado com sucesso!")
                            
                        except Exception as e:
                            print(f"Erro no quarto insert (MEGA_EPC_DETALHE): {str(e)}")
                            raise e
                            
                    except Exception as e:
                        print(f"Erro no terceiro insert (MEGA_EPC_MOV_ITEM): {str(e)}")
                        raise e
                        
                except Exception as e:
                    print(f"Erro no segundo insert (MEGA_EPC): {str(e)}")
                    raise e
                    
            except Exception as e:
                print(f"Erro no primeiro insert (MEGA_EPC_MOV): {str(e)}")
                raise e
            
            conn.close()
            
            QMessageBox.information(self, "Sucesso", "RFID registrado com sucesso!")
            self.rfid_input.clear()
            
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", 
                               f"Erro ao conectar ou consultar o banco de dados: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao vincular RFID: {str(e)}")
    
    def buscar_avancada(self):
        try:
            # Limpar a tabela antes de uma nova busca
            self.tabela.setRowCount(0)
            
            # Verificar campos obrigatórios
            if not self.produto_input.text().strip():
                QMessageBox.warning(self, "Aviso", "Por favor, informe o produto!")
                return
            
            print("Tentando conectar ao banco de dados...")
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            
            # Valores para a consulta
            produto = self.produto_input.text().strip()
            cor_produto = self.cor_input.text().strip()
            tamanho = self.tamanho_input.text().strip()
            filial = self.filial_avancada_combo.currentText()
            
            print(f"Valores da consulta: Produto={produto}, Cor={cor_produto}, Tamanho={tamanho}, Filial={filial}")
            
            
            query = """
            SELECT 
                pb.CODIGO_BARRA,
                pb.PRODUTO,
                c.DESC_PRODUTO,
                pb.COR_PRODUTO,
                pb.TAMANHO,
                pb.GRADE,
                ep.FILIAL,
                CASE 
                    WHEN pb.TAMANHO = 1 THEN ep.ES1
                    WHEN pb.TAMANHO = 2 THEN ep.ES2
                    WHEN pb.TAMANHO = 3 THEN ep.ES3
                    WHEN pb.TAMANHO = 4 THEN ep.ES4
                    WHEN pb.TAMANHO = 5 THEN ep.ES5
                    WHEN pb.TAMANHO = 6 THEN ep.ES6
                    WHEN pb.TAMANHO = 7 THEN ep.ES7
                    ELSE NULL
                END AS ESTOQUE_TAMANHO,
                pb.CODIGO_BARRA_PADRAO
            FROM produtos_barra pb
            JOIN estoque_produtos ep ON pb.PRODUTO = ep.PRODUTO AND pb.COR_PRODUTO = ep.COR_PRODUTO
            JOIN PRODUTOS c ON c.PRODUTO = pb.PRODUTO AND c.PRODUTO = ep.PRODUTO
            WHERE TIPO_COD_BAR = '4'
            AND pb.CODIGO_BARRA = ?
            AND ep.FILIAL = ?
            """
            params = [produto, filial]
            
            if cor_produto:
                query += " AND RES1.COR_PRODUTO = ?"
                params.append(cor_produto)
            
            if tamanho:
                query += " AND tam.TAMANHO = ?"
                params.append(tamanho)
            
            print("Executando a consulta...")
            cursor.execute(query, params)
            
            resultados = cursor.fetchall()
            print(f"Número de resultados encontrados: {len(resultados)}")
            
            if len(resultados) == 0:
                QMessageBox.information(self, "Informação", "Nenhum resultado encontrado para os critérios informados.")
                return
            
            # Armazenar dados do produto selecionado
            self.produto_atual = resultados[0][2]  # PRODUTO
            self.cor_atual = resultados[0][3]      # COR_PRODUTO
            self.tamanho_atual = resultados[0][4]   # TAMANHO
            self.codigo_barra_atual = resultados[0][0]  # CODIGO_BARRA
            
            self.tabela.setRowCount(len(resultados))
            for i, row in enumerate(resultados):
                self.tabela.setItem(i, 0, QTableWidgetItem(str(row[3])))  # DESC_PRODUTO
                self.tabela.setItem(i, 1, QTableWidgetItem(str(row[1])))  # FILIAL
                self.tabela.setItem(i, 2, QTableWidgetItem(str(row[6])))  # QTDE
                self.tabela.setItem(i, 3, QTableWidgetItem(str(row[0])))  # CODIGO_BARRA
            
            conn.close()
            
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", 
                               f"Erro ao conectar ou consultar o banco de dados: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar produto: {str(e)}")

    def load_config(self):
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    
                    # Configurar string de conexão
                    self.conn_str = (
                        f"DRIVER={{{config['server']['driver']}}};"
                        f"SERVER={config['server']['host']},{config['server']['port']};"
                        f"DATABASE={config['server']['database']};"
                        f"UID={config['server']['username']};"
                        f"PWD={config['server']['password']}"
                    )
                    
                    # Atualizar lista de filiais
                    self.filiais = config['filiais_disponiveis']
                    self.filial_padrao = config.get('filial_padrao', self.filiais[0] if self.filiais else '')
                    
                    return True
            return False
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar configurações: {str(e)}")
            return False
    
    def show_config(self):
        login = LoginDialog(self)
        if login.exec_() == LoginDialog.Accepted:
            config = ConfigWindow(self)
            if config.exec_() == ConfigWindow.Accepted:
                # Recarregar configurações
                if self.load_config():
                    # Atualizar ComboBoxes
                    self.filial_combo.clear()
                    self.filial_combo.addItems(self.filiais)
                    self.filial_avancada_combo.clear()
                    self.filial_avancada_combo.addItems(self.filiais)
                    
                    # Definir filial padrão
                    if self.filial_padrao:
                        index = self.filial_combo.findText(self.filial_padrao)
                        if index >= 0:
                            self.filial_combo.setCurrentIndex(index)
                        index = self.filial_avancada_combo.findText(self.filial_padrao)
                        if index >= 0:
                            self.filial_avancada_combo.setCurrentIndex(index)
                    
                    QMessageBox.information(self, "Sucesso", "Configurações atualizadas com sucesso!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProdutoApp()
    window.show()
    sys.exit(app.exec_()) 