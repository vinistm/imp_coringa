# Consulta de Produtos

Aplicação para consulta de produtos no banco de dados Linx Lafort.

## Requisitos

- Python 3.8 ou superior
- SQL Server Driver instalado
- Dependências listadas em requirements.txt

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
pip install PyQt5==5.15.9
pip install pyodbc==5.0.1
pip install python-barcode==0.15.1
pip install Pillow==10.2.0
```

2. Certifique-se de que o SQL Server Driver está instalado no sistema

## Uso

Execute o arquivo main.py:
```bash
python main.py
```

## Funcionalidades

- Consulta de produtos por:
  - Produto
  - Cor do Produto
  - Tamanho
  - Filial

- Exibe informações como:
  - Descrição do Produto
  - Filial
  - Quantidade
  - SKU 