from PIL import Image
import os

def create_ico():
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    png_path = os.path.join('assets', 'logo.png')
    if not os.path.exists(png_path):
        print(f"Erro: Arquivo {png_path} não encontrado!")
        return False
    
    try:
        img = Image.open(png_path)
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        sizes = [(16,16), (20,20), (24,24), (32,32), (48,48), (64,64), (128,128), (256,256)]
        
        icon_images = []
        
        for size in sizes:
            resized_img = img.copy()
            resized_img.thumbnail(size, Image.Resampling.LANCZOS)
            
            final_img = Image.new('RGBA', size, (0, 0, 0, 0))
            
            paste_x = (size[0] - resized_img.size[0]) // 2
            paste_y = (size[1] - resized_img.size[1]) // 2
            
            final_img.paste(resized_img, (paste_x, paste_y), resized_img)
            
            icon_images.append(final_img)
        
        ico_path = os.path.join('assets', 'logo.ico')
        icon_images[0].save(ico_path, format='ICO', sizes=[(img.size) for img in icon_images], append_images=icon_images[1:])
        
        print(f"Arquivo ICO criado com sucesso em {ico_path}!")
        return True
        
    except Exception as e:
        print(f"Erro ao criar arquivo ICO: {str(e)}")
        return False

if __name__ == '__main__':
    create_ico() 