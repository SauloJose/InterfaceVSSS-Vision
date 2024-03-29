#Definindo constantes.
#Modos de utilização da câmera
import numpy as np

#Modo de carregar imagens
MODE_DEFAULT:int = 1
MODE_USB_CAM: int= 2
MODE_VIDEO_CAM:int = 3
MODE_IMAGE:int = 4

#Modo de execução do Emulador
MODE_EMULATE_COLOR:int = 5

#Modo de execução da interface
MODE_INTER_EMULATE_DEFAULT: int = 0
MODE_INTER_EMULATE_CALIBRATION: int = 1
MODE_INTER_EMULATE_ADJUST: int = 2



#Definição de array de cores (dark, light)
orange = np.array([[4,100,128], [21,255,255]]) #bola
yellow = np.array([[23,70,120], [30,255,255]]) #aliados
purple = np.array([[120,100,100], [170,255,255]]) #inimigos

#Variáveis das cores inferiores


#Variáveis das cores superiores


#Caminho para a configuração de cores.

if __name__ == "__main__":
    print("Módulo sendo executado como funcao principal")
    
