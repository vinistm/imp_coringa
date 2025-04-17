from PIL import Image

# Abrir a imagem
img = Image.open('assets/logo.png')

# Converter para o formato .ico
img.save('assets/logo.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]) 