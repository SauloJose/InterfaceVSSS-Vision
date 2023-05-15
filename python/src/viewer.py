from modulos import *

#Classe de player para o aplicativo
class MyViewer:
    def __init__(self, window: Frame, cap: int):
        #Frame que irá ser utilizado
        self.window = window

        #Fonte que irá receber os dados.
        self.cap = cap
        self.pause = False

        self.canvas = Canvas(window, width=780, height=480)
        self.canvas.place(relx=0, rely=0)

        self.delay = 14# milliseconds
        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if not self.pause and ret:
            #Aplicar o algorítmo na iamgem capturada pela webcam
            #Exibir imagem.
            #Converte para RGBA
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            #Transforma num array para exibir em um canvas
            pilImage = Image.fromarray(cv2image)

            #Cria uma variável interna para visualizar.
            self.image = ImageTk.PhotoImage(image=pilImage)
            self.canvas.create_rectangle(0, 0, 748, 480, fill="black")
            self.canvas.create_image(0, 0, anchor=NW, image=self.image)
        self.window.after(self.delay, self.update)
    
    def destroy_viewer(self):
        self.cap.release()
        self.canvas.create_rectangle(0, 0, 748, 480, fill="black")

#Chamando aplicação
if __name__ == "__main__":
    print("Módulo sendo executado como funcao principal")

