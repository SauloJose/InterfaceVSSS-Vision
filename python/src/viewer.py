from modulos import *

#Classe de player para o aplicativo
class MyViewer:
    def __init__(self, window: Frame):
        print("[VIEWER] Viewer criado")
        #Frame que irá ser utilizado
        self.window = window

    #Método para configurar o viewer para a função definida
    def config(self):
        print("[VIEWER] Viewer em modo de configuração")
        #Configurand o o canvas
        self.canvas = Canvas(self.window, width=780, height=510)
        self.canvas.place(relx=0, rely=0)
        self.canvas.create_rectangle(0, 0, 748, 510, fill="black")

        
    #Resetando as configurações do viewer para forma padrão
    def resetConfig(self):
        print("[VIEWER] Resetando configuração de exibição")
        #Retornado ao modo padrão
        self.default_mode()
    
    #Método de [VIEWER]viewer padrão sem exibir
    def default_mode(self):
        print("[VIEWER] Viewer não configurado")
        self.canvas = Canvas(self.window, width=780, height=480)
        self.canvas.place(relx=0, rely=0)
        self.canvas.create_rectangle(0, 0, 748, 510, fill="black")
    
    def show(self, image):
        cv2Img = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        pilImage = Image.fromarray(cv2Img)
        
        # Obter as dimensões atuais da imagem
        width, height = pilImage.size
        
        # Definir o tamanho máximo desejado
        max_width = 748
        max_height = 510
        
        # Calcular a porcentagem de redução com base nas dimensões atuais
        percent_reduction = min(max_width / width, max_height / height)
        
        # Calcular o novo tamanho da imagem
        new_width = int(width * percent_reduction)
        new_height = int(height * percent_reduction)
        
        # Redimensionar a imagem
        resized = pilImage.resize((new_width, new_height), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image=resized)
        
        # Calcular as coordenadas para centralizar a imagem
        x = (max_width - new_width) // 2
        y = (max_height - new_height) // 2
    
        self.canvas.create_image(x,y, anchor=NW, image=self.image)
    
    
    #definindo o
#Chamando aplicação
if __name__ == "__main__":
    print("[VIEWER] Módulo sendo executado como funcao principal")

