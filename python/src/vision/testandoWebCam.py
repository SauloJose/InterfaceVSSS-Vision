import cv2
from PIL import Image, ImageTk
import tkinter as tk

class MyViewer:
    def __init__(self, window, cap):
        self.window = window
        self.cap = cap

        self.canvas = tk.Canvas(window, width=680, height=480)
        self.canvas.pack()

        #Variável para pausar o player
        self.pause = False


        self.delay = 15 # milliseconds
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
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        self.window.after(self.delay, self.update)

    # Define a função de pausa
    def pause_video(self):
        self.pause = True

    def return_video(self):
        self.pause=False

cap = cv2.VideoCapture(0)
root = tk.Tk()
app = MyViewer(root, cap)

root.mainloop()
