import sys
import pyodbc
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                           QTableWidget, QTableWidgetItem, QMessageBox,
                           QSizePolicy, QDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import json
import os
from PyQt5.QtGui import QColor, QFont
import uuid
import time
from datetime import datetime

class OmniApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Omni")
        self.setMinimumSize(800, 600)
        
        # Configurar ícone da janela
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logo.ico')
        if not os.path.exists(icon_path):
            # Se não encontrar no caminho absoluto, tenta no diretório atual
            icon_path = os.path.join('assets', 'logo.ico')
        self.setWindowIcon(QIcon(icon_path))
        
        # Carregar configurações
        self.load_config()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        titulo = QLabel("Omni")
        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 20px;
        """)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Botão de configurações
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
        
        # Botão Voltar
        voltar_button = QPushButton("← Voltar")
        voltar_button.setFixedWidth(120)
        voltar_button.clicked.connect(self.voltar_tela_inicial)
        voltar_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #757575, stop:1 #616161);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px;
                min-height: 30px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #616161, stop:1 #424242);
           
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #424242, stop:1 #212121);
            }
        """)
        
        # Adicionar os botões ao layout principal
        title_layout = QHBoxLayout()
        title_layout.addWidget(voltar_button)
        title_layout.addStretch()
        title_layout.addWidget(config_button)
        layout.insertLayout(0, title_layout)
        
        # Adicionar um espaçamento antes do botão
        layout.addSpacing(20)
        
        # Grupo de busca
        grupo_busca = QWidget()
        grupo_busca_layout = QVBoxLayout(grupo_busca)  # Mudado para QVBoxLayout
        grupo_busca_layout.setSpacing(15)  # Espaçamento entre as linhas
        
        # Primeira linha: Pedido e botão buscar
        linha_pedido = QHBoxLayout()
        linha_pedido.setSpacing(10)
        
        # Campo de pedido
        pedido_layout = QVBoxLayout()
        pedido_label = QLabel("Número do Pedido*")
        self.pedido_input = QLineEdit()
        self.pedido_input.setPlaceholderText("Digite o número do pedido")
        self.pedido_input.setMinimumWidth(200)
        self.pedido_input.setMinimumHeight(40)
        self.pedido_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        pedido_layout.addWidget(pedido_label)
        pedido_layout.addWidget(self.pedido_input)
        linha_pedido.addLayout(pedido_layout)
        
        # Botão de busca
        buscar_button = QPushButton("Buscar")
        buscar_button.setFixedWidth(120)
        buscar_button.setMinimumHeight(40)  # Alinhar altura com o input
        buscar_button.clicked.connect(self.buscar_pedido)
        buscar_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #45A049);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 12px;
                padding: 4px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #45A049, stop:1 #3D8B40);
         
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3D8B40, stop:1 #2E7D32);
            }
        """)
        linha_pedido.addWidget(buscar_button, alignment=Qt.AlignBottom)
        
        # Segunda linha: Campo RFID
        linha_rfid = QHBoxLayout()
        linha_rfid.setSpacing(10)
        
        rfid_layout = QVBoxLayout()
        rfid_label = QLabel("Leitor RFID")
        self.rfid_input = QLineEdit()
        self.rfid_input.setPlaceholderText("Aguardando leitura RFID...")
        self.rfid_input.setMinimumWidth(200)
        self.rfid_input.setMinimumHeight(40)
        self.rfid_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.rfid_input.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        rfid_layout.addWidget(rfid_label)
        rfid_layout.addWidget(self.rfid_input)
        linha_rfid.addLayout(rfid_layout)
        
        # Adicionar as linhas ao grupo de busca
        grupo_busca_layout.addLayout(linha_pedido)
        grupo_busca_layout.addLayout(linha_rfid)
        
        layout.addWidget(grupo_busca)
        
        # Tabela de resultados
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)  # Adicionando uma coluna para o ícone
        self.tabela.setHorizontalHeaderLabels(["", "Pedido", "Ticket", "Descrição do Produto", "Cor do Produto", "Codigo de Barra"])
        
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, header.Fixed)  # Coluna do status
        self.tabela.setColumnWidth(0, 40)  # Largura fixa para a coluna de status
        header.setSectionResizeMode(1, header.ResizeToContents)  # Pedido
        header.setSectionResizeMode(2, header.ResizeToContents)  # Ticket
        header.setSectionResizeMode(3, header.Stretch)  # Descrição
        header.setSectionResizeMode(4, header.ResizeToContents)  # Cor
        header.setSectionResizeMode(5, header.ResizeToContents)  # Código de Barras
        
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
        
        layout.addWidget(self.tabela)
        
        # Botão Validar Omni
        self.validar_button = QPushButton("Validar Omni")
        self.validar_button.setFixedWidth(150)  # Aumentado para ficar mais visível
        self.validar_button.setFixedHeight(50)  # Altura maior para destaque
        self.validar_button.setEnabled(False)  # Inicialmente desabilitado
        self.validar_button.clicked.connect(self.validar_omni)
        self.validar_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #45A049);
                color: white;
                border: none;
                border-radius: 25px;
                font-weight: bold;
                font-size: 14px;
                padding: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #45A049, stop:1 #3D8B40);
            }
            QPushButton:disabled {
                background: #cccccc;
                color: #666666;
            }
        """)
        
        # Adicionar o botão Validar Omni ao final do layout principal
        layout.addStretch()  # Adiciona espaço flexível para empurrar o botão para baixo
        layout.addWidget(self.validar_button, alignment=Qt.AlignRight)
        layout.addSpacing(20)  # Adiciona um pequeno espaço na parte inferior
        
        # Estilo da janela
        self.setStyleSheet("""
            QMainWindow {
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
        """)
        
        # Dicionário para armazenar os RFIDs já lidos
        self.rfids_lidos = set()
        self.produtos_validados = {}
    
    def load_config(self):
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    
                    # Configurar string de conexão
                    server_config = config['server']
                    self.conn_str = (
                        f"DRIVER={{{server_config['driver']}}};"
                        f"SERVER={server_config['host']}"
                    )
                    
                    # Adicionar porta apenas se existir
                    if 'port' in server_config and server_config['port']:
                        self.conn_str += f",{server_config['port']}"
                    
                    # Completar string de conexão
                    self.conn_str += (
                        f";DATABASE={server_config['database']};"
                        f"UID={server_config['username']};"
                        f"PWD={server_config['password']}"
                    )
                    
                    # Guardar a filial configurada
                    self.filial_padrao = config.get('filial_padrao', '')
                    
                    return True
            return False
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar configurações: {str(e)}")
            return False
    
    def buscar_pedido(self):
        try:
            if not self.pedido_input.text().strip():
                QMessageBox.warning(self, "Aviso", "Por favor, informe o número do pedido!")
                return
            
            if not hasattr(self, 'filial_padrao') or not self.filial_padrao:
                QMessageBox.warning(self, "Aviso", "Por favor, configure a filial padrão nas configurações!")
                return
            
            print("Tentando conectar ao banco de dados...")
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            
            # Primeiro, obter o código da filial
            query_filial = """
            SELECT CODIGO_FILIAL 
            FROM LOJAS_VAREJO 
            WHERE FILIAL = ?
            """
            
            cursor.execute(query_filial, (self.filial_padrao,))
            resultado_filial = cursor.fetchone()
            
            if not resultado_filial:
                QMessageBox.warning(self, "Aviso", f"Filial '{self.filial_padrao}' não encontrada!")
                return
            
            codigo_filial = resultado_filial[0]
            print(f"Código da filial {self.filial_padrao}: {codigo_filial}")
            
            numero_pedido = self.pedido_input.text().strip()
            
            query = """
            SELECT 
                NUMERO_TITULO, a.TICKET, DESC_PRODUTO, e.DESC_COR_PRODUTO, c.CODIGO_BARRA
            from loja_venda a 
            join LOJA_VENDA_PARCELAS b on a.LANCAMENTO_CAIXA=b.LANCAMENTO_CAIXA 
                and a.CODIGO_FILIAL=b.CODIGO_FILIAL 
                and a.TERMINAL=b.TERMINAL
            join LOJA_VENDA_PRODUTO c on c.TICKET=a.TICKET 
                and c.CODIGO_FILIAL=a.CODIGO_FILIAL 
                and a.CODIGO_FILIAL=b.CODIGO_FILIAL
            join PRODUTOS d on d.PRODUTO=c.PRODUTO
            join PRODUTO_CORES e on e.COR_PRODUTO=c.COR_PRODUTO 
                and e.PRODUTO=d.PRODUTO 
                and e.PRODUTO=c.PRODUTO
            where NUMERO_TITULO = '#' + ?
            and a.CODIGO_FILIAL = ?
            """
            
            print(f"Buscando pedido {numero_pedido} na filial {self.filial_padrao} (código: {codigo_filial})")
            cursor.execute(query, (numero_pedido, codigo_filial))
            
            resultados = cursor.fetchall()
            print(f"Número de resultados encontrados: {len(resultados)}")
            
            if len(resultados) == 0:
                QMessageBox.information(self, "Informação", 
                    f"Nenhum resultado encontrado para o pedido {numero_pedido} na filial {self.filial_padrao}.")
                return
            
            self.tabela.setRowCount(len(resultados))
            for i, row in enumerate(resultados):
                # Coluna Status começa vazia
                self.tabela.setItem(i, 0, QTableWidgetItem(""))
                self.tabela.setItem(i, 1, QTableWidgetItem(str(row[0])))  # NUMERO_TITULO
                self.tabela.setItem(i, 2, QTableWidgetItem(str(row[1])))  # TICKET
                self.tabela.setItem(i, 3, QTableWidgetItem(str(row[2])))  # DESC_PRODUTO
                self.tabela.setItem(i, 4, QTableWidgetItem(str(row[3])))  # DESC_COR_PRODUTO
                self.tabela.setItem(i, 5, QTableWidgetItem(str(row[4])))  # CODIGO_BARRA

            conn.close()
            
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", 
                               f"Erro ao conectar ou consultar o banco de dados: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar pedido: {str(e)}")
    
    def show_config(self):
        from config_window import LoginDialog, ConfigWindow
        login = LoginDialog(self)
        if login.exec_() == LoginDialog.Accepted:
            config = ConfigWindow(self)
            if config.exec_() == ConfigWindow.Accepted:
                self.load_config()
                QMessageBox.information(self, "Sucesso", "Configurações atualizadas com sucesso!")

    def voltar_tela_inicial(self):
        from tela_inicial import TelaInicial
        self.tela_inicial = TelaInicial()
        self.tela_inicial.show()
        self.close()

    def verificar_rfid(self, rfid):
        conn = None
        try:
            print("\n=== Iniciando verificação de RFID ===")
            print(f"RFID lido: {rfid}")
            
            # Verificar se o RFID já foi lido
            if rfid in self.rfids_lidos:
                print("RFID já foi lido anteriormente!")
                QMessageBox.warning(self, "Aviso", "Este RFID já foi lido anteriormente!")
                return False
            
            # Estabelecer conexão
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            
            # Primeira consulta - Verificar EAN13 e obter EPC
            print("\nConsultando EAN13 do RFID...")
            query_ean13 = """
            SELECT a.EAN13, b.EPC, a.ID_EPC
            FROM MEGA_EPC_DETALHE a 
            JOIN MEGA_EPC b ON a.ID_EPC = b.ID_EPC  
            WHERE b.EPC = ?
            """
            
            cursor.execute(query_ean13, (rfid,))
            resultado_ean13 = cursor.fetchone()
            
            if resultado_ean13:
                ean13 = resultado_ean13[0].strip() if resultado_ean13[0] else ""
                id_epc = resultado_ean13[2]
                print(f"EAN13 encontrado (tipo 3): '{ean13}'")
                
                for row in range(self.tabela.rowCount()):
                    codigo_barra_pedido = self.tabela.item(row, 5).text().strip()
                    print(f"\nVerificando linha {row + 1}:")
                    print(f"Código de barras do pedido (tipo 4): '{codigo_barra_pedido}'")
                    
                    query_produto = """
                    SELECT RTRIM(A.CODIGO_BARRA) as CODIGO_BARRA, A.PRODUTO, A.COR_PRODUTO, A.TAMANHO
                    FROM PRODUTOS_BARRA A
                    CROSS APPLY (
                        SELECT PRODUTO, COR_PRODUTO, TAMANHO 
                        FROM PRODUTOS_BARRA 
                        WHERE CODIGO_BARRA = ?
                    ) B
                    WHERE A.PRODUTO = B.PRODUTO
                      AND A.COR_PRODUTO = B.COR_PRODUTO
                      AND A.TAMANHO = B.TAMANHO
                      AND A.TIPO_COD_BAR IN ('3', '4')
                    """
                    
                    cursor.execute(query_produto, (codigo_barra_pedido,))
                    resultados = cursor.fetchall()
                    codigos_encontrados = [r[0].strip() if r[0] else "" for r in resultados]
                    print(f"Códigos encontrados (sem espaços): {codigos_encontrados}")
                    
                    if ean13 in codigos_encontrados and codigo_barra_pedido in codigos_encontrados:
                        print("Match encontrado! Atualizando interface...")
                        
                        # Armazenar informações do produto para uso posterior
                        produto_info = resultados[0]
                        self.produtos_validados[row] = {
                            'id_epc': id_epc,
                            'produto': produto_info[1],
                            'cor_produto': produto_info[2],
                            'tamanho': produto_info[3],
                            'ean13': ean13
                        }
                        
                        # Primeiro, guardar todos os valores originais
                        valores_originais = []
                        for col in range(self.tabela.columnCount()):
                            item = self.tabela.item(row, col)
                            valores_originais.append(item.text() if item else "")
                        
                        # Agora, atualizar cada célula mantendo o texto original
                        for col in range(self.tabela.columnCount()):
                            novo_item = QTableWidgetItem()
                            if col == 0:
                                novo_item.setText("✅")  
                                novo_item.setTextAlignment(Qt.AlignCenter)
                               
                                novo_item.setBackground(QColor('#4CAF50')) 
                                novo_item.setForeground(QColor('white'))  
                                novo_item.setFont(QFont('Segoe UI', 12, QFont.Bold))  
                                # Definir tamanho da célula
                                self.tabela.setRowHeight(row, 30)  # Altura fixa para a linha
                               
                                novo_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                            else:
                                novo_item.setText(valores_originais[col])
                                # Definir cores para as outras células
                                novo_item.setBackground(QColor(76, 175, 80, 30))  
                                novo_item.setForeground(QColor(0, 0, 0))  
                            
                            # Aplicar o item à tabela
                            self.tabela.setItem(row, col, novo_item)
                        
                        # Forçar atualização visual
                        self.tabela.viewport().update()
                        self.tabela.update()
                        QApplication.processEvents()  # Forçar processamento de eventos
                        
                        # Adicionar o RFID à lista de RFIDs lidos
                        self.rfids_lidos.add(rfid)
                        
                        # Verificar se todos os itens foram validados
                        self.verificar_validacao_completa()
                        
                        print("RFID registrado com sucesso!")
                        QMessageBox.information(self, "Sucesso", "RFID vinculado com sucesso!")
                        return True
                    else:
                        print("Códigos não correspondem")
            else:
                print("Nenhum EAN13 encontrado para este RFID")
            
            print("\nNenhuma correspondência encontrada para este RFID")
            QMessageBox.warning(self, "Aviso", "RFID não encontrado ou não vinculado a nenhum produto!")
            return False
            
        except Exception as e:
            print(f"\nERRO: {str(e)}")
            QMessageBox.critical(self, "Erro", f"Erro ao verificar RFID: {str(e)}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass
            print("\n=== Fim da verificação de RFID ===\n")

    def verificar_validacao_completa(self):
        """Verifica se todos os itens foram validados e ativa o botão Validar Omni"""
        total_itens = self.tabela.rowCount()
        itens_validados = len(self.produtos_validados)
        
        if total_itens > 0 and total_itens == itens_validados:
            self.validar_button.setEnabled(True)
        else:
            self.validar_button.setEnabled(False)

    def validar_omni(self):
        """Processa a validação final e faz os inserts no banco"""
        try:
            print("\n=== Iniciando validação Omni ===")
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            
            # Buscar o código da filial correto
            print(f"\nBuscando código da filial para: {self.filial_padrao}")
            cursor.execute("""
                SELECT a.COD_FILIAL 
                FROM FILIAIS a 
                JOIN LOJAS_VAREJO b ON a.FILIAL = b.FILIAL 
                WHERE a.FILIAL = ?
            """, (self.filial_padrao,))
            resultado_filial = cursor.fetchone()
            if not resultado_filial:
                raise Exception(f"Código da filial não encontrado para: {self.filial_padrao}")
            codigo_filial = resultado_filial[0]
            print(f"Código da filial obtido: {codigo_filial}")

            # Obter data atual e gerar UUID
            data_atual = datetime.now()
            id_origem = str(uuid.uuid4()).upper()
            print(f"\nID_ORIGEM gerado: {id_origem}")
            print(f"Data atual: {data_atual}")

            # Definir o ticket a partir da tabela
            if self.tabela.rowCount() > 0:
                self.ticket = self.tabela.item(0, 2).text().strip()
                print(f"Ticket obtido: {self.ticket}")
            else:
                raise Exception("Nenhum ticket encontrado na tabela.")

            # Montar chave para MEGA_EPC_MOV
            chave = f"DATA_VENDA=[{data_atual.strftime('%Y%m%d')}] AND CODIGO_FILIAL=[{codigo_filial}] AND TICKET=[{self.ticket}]"
            print(f"\nChave montada: {chave}")

            # Primeiro insert - MEGA_EPC_MOV
            insert_mov_query = f"""
                INSERT INTO MEGA_EPC_MOV 
                (TIPO, ID_ORIGEM, TRANSACAO, TABELA_PAI, CHAVE, DATA_MOV, ATUALIZACAO, COD_FILIAL, NAO_ATUALIZA_TIPO)
                VALUES ('S', '{id_origem}', 'sale', 'LOJA_VENDA', '{chave}', '{data_atual.strftime("%Y-%m-%d %H:%M:%S")}', 
                        '{data_atual.strftime("%Y-%m-%d %H:%M:%S")}', '{codigo_filial}', '0')
            """
            print(f"\nExecutando insert MEGA_EPC_MOV:\n{insert_mov_query}")
            
            try:
                cursor.execute(insert_mov_query)
                print("Insert MEGA_EPC_MOV executado com sucesso!")
            except Exception as e:
                print(f"Erro ao executar insert MEGA_EPC_MOV: {str(e)}")
                raise e

            # Aguardar 1 segundo
            print("\nAguardando 1 segundo antes de continuar...")
            time.sleep(1)

            # Atualizar MEGA_EPC_DETALHE
            print("\nIniciando atualizações na MEGA_EPC_DETALHE")
            for row, produto in self.produtos_validados.items():
                print(f"\nAtualizando produto {row + 1} de {len(self.produtos_validados)}")
                print(f"ID_EPC: {produto['id_epc']}")
                
                update_query = f"""
                    UPDATE MEGA_EPC_DETALHE 
                    SET ATUALIZACAO = GETDATE(),
                        COD_FILIAL = '{codigo_filial}',
                        ULTIMO_TIPO_MOV = 'S'
                    WHERE ID_EPC = '{produto['id_epc']}'
                """
                print(f"Executando query:\n{update_query}")
                
                try:
                    cursor.execute(update_query)
                    print("Update executado com sucesso!")
                except Exception as e:
                    print(f"Erro ao executar update: {str(e)}")
                    raise e

            conn.commit()
            print("\nTodas as operações foram commitadas com sucesso!")
            
            # Mostrar animação de sucesso
            self.mostrar_animacao_sucesso()
            
        except Exception as e:
            print(f"\nERRO: {str(e)}")
            QMessageBox.critical(self, "Erro", f"Erro ao validar Omni: {str(e)}")
        finally:
            if conn:
                conn.close()
            print("\n=== Fim da validação Omni ===\n")

    def mostrar_animacao_sucesso(self):
        """Mostra uma mensagem de sucesso e limpa a tela"""
        # Criar uma janela de mensagem
        mensagem = QDialog(self)
        mensagem.setWindowTitle("Sucesso")
        mensagem.setFixedSize(300, 150)
        mensagem.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout(mensagem)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Texto principal
        label_texto = QLabel("RFID Vinculado com sucesso!")
        label_texto.setAlignment(Qt.AlignCenter)
        label_texto.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        layout.addWidget(label_texto)
        
        # Botão OK
        botao_ok = QPushButton("OK")
        botao_ok.setFixedWidth(100)
        botao_ok.setFixedHeight(30)
        botao_ok.clicked.connect(lambda: self.finalizar_validacao(mensagem))
        botao_ok.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background: #45A049;
            }
        """)
        
        layout.addWidget(botao_ok, alignment=Qt.AlignCenter)
        
        # Mostrar a mensagem
        mensagem.exec_()

    def finalizar_validacao(self, animacao):
        """Finaliza a validação e limpa a tela"""
        animacao.accept()
        self.pedido_input.clear()
        self.tabela.setRowCount(0)
        self.produtos_validados.clear()
        self.rfids_lidos.clear()
        self.validar_button.setEnabled(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.rfid_input.hasFocus():
                rfid = self.rfid_input.text().strip()
                if rfid:
                    self.verificar_rfid(rfid)
                    # Limpar o campo após a leitura
                    self.rfid_input.clear()
                    # Voltar o foco para o campo RFID
                    self.rfid_input.setFocus()
            elif self.pedido_input.hasFocus():
                self.buscar_pedido() 