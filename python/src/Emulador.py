from modulos import *
from TreeMenu import *
from viewer import MyViewer
#Classe para o emulador, com base nos dados carregados...
#Carrego a treeView, e tiro os dados dela, assim posso iniciar variáveis da emulação.
class Emulator:
    def __init__(self, TreeMenu: TreeMenu,Viewer: MyViewer, IdCap: int, btn_run: Button, btn_stop: Button):
        #Recuperando as variáveis do emulador, considerando que é uma treeview
        #Carregando como valores internos do Emulador.
        self.TreeMain = TreeMenu
        self.Viewer = Viewer
        self.IdCap = IdCap
        self.btn_run = btn_run
        self.btn_stop = btn_stop


        #Carregando variáveis de configuração
        self.load_vars()
        
    #Método para carregar as variáveis internas que foram salvas no arquivo config.json
    def load_vars(self):
        #Carregando os valores que eu quero da árvore.
        self.CamUSB = self.TreeMain.tree.item('I003','value')[0]
        self.ImgPath = self.TreeMain.tree.item('I004','value')[0]
        self.VideoPath = self.TreeMain.tree.item('I005','value')[0]
        self.UseMode = self.TreeMain.tree.item('I006','value')[0]
        self.VertField =self.TreeMain.tree.item('I008','value')[0]
        self.DefCam = self.TreeMain.tree.item('I009','value')[0]
        self.CalColor = self.TreeMain.tree.item('I00B','value')[0]
        self.PrincColorT1 = self.TreeMain.tree.item('I00E','value')[0]
        self.R1color1 = self.TreeMain.tree.item('I00F','value')[0]
        self.R1color2 = self.TreeMain.tree.item('I010','value')[0]
        self.R1color3 = self.TreeMain.tree.item('I011','value')[0]
        self.PrincColorT2 = self.TreeMain.tree.item('I013','value')[0]
        self.R2color1 = self.TreeMain.tree.item('I014','value')[0]
        self.R2color2 = self.TreeMain.tree.item('I015','value')[0]
        self.R2color3 = self.TreeMain.tree.item('I016','value')[0]
        self.DEBUG = self.TreeMain.tree.item('I018','value')[0]
        self.EXECMode = self.TreeMain.tree.item('I019','value')[0]
    
    #Método apenas para ver quais variáveis está no emulador.
    def show_variables(self):
        msg=f"""====Emulador===
        CamUSB: {self.CamUSB}
        ImgPath: {self.ImgPath}
        VideoPath: {self.VideoPath}
        UseMode: {self.UseMode}
        VertField: {self.VertField}
        DefCam: {self.DefCam}
        CalColor: {self.CalColor}
        PrincColorT1: {self.PrincColorT1}
        R1color1: {self.R1color1}
        R1color2: {self.R1color2}
        R1color3: {self.R1color3}
        PrincColorT2: {self.PrincColorT2}
        R2color1: {self.R2color1}
        R2color2: {self.R2color2}
        R2color3: {self.R2color3}
        DEBUG: {self.DEBUG}
        EXECMode: {self.EXECMode}
        """.encode('utf-8')

        print(msg.decode('utf-8', errors='replace'))

    #Método para o emulador exibir as imagens
    def init(self):
        print("Emulador iniciado")
        cap = cv2.VideoCapture(self.IdCap)


    #Método para pausar o Emulador
    def pause(self):
        print('Emulador Pausado')

    #Método para Parar a Emulação.
    def stop(self):
        print('Emulador parado')


#SEGURANÇA
if __name__ == "__main__":
    print("Módulo sendo executado como funcao principal")

