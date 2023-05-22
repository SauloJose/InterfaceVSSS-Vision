from modulos import *
from TreeMenu import *
from viewer import MyViewer

#Classe para o emulador, com base nos dados carregados...
#Carrego a treeView, e tiro os dados dela, assim posso iniciar variáveis da emulação.
class Emulator:
    def __init__(self, TreeMenu: TreeMenu, Viewer: MyViewer, DebugViewer: MyViewer, ResulViewer: MyViewer, IdCap: int, btn_run: Button, btn_stop: Button):
        #Recuperando as variáveis do emulador, considerando que é uma treeview
        #Carregando como valores internos do Emulador.
        print('[EMULADOR] Emulador foi construído')
        self.TreeMain = TreeMenu
        self.Viewer = Viewer
        self.DebugViewer = DebugViewer
        self.ResulViewer= ResulViewer
        self.IdCap = IdCap
        self.btn_run = btn_run
        self.btn_stop = btn_stop
        self.Mode = MODE_DEFAULT
        self.isRuningCam = False #Variável para thread do vídeo
        self.DEBUGA = False
        self.thread = None
        self.capture = None
        self.delay = 14 #ms
        #configurando o viewer
        self.Viewer.config()
        self.DebugViewer.config()
        self.ResulViewer.config()
        
    #Método para carregar as variáveis internas que foram salvas no arquivo config.json
    def load_vars(self):
        #Carregando os valores que eu quero da árvore.
        self.CamUSB = self.TreeMain.tree.item('I003','value')[0]
        self.ImgPath = self.TreeMain.tree.item('I004','value')[0]
        self.VideoPath = self.TreeMain.tree.item('I005','value')[0]
        self.UseMode = self.TreeMain.tree.item('I006','value')[0]
        self.OffSetBord = int(self.TreeMain.tree.item('I008','value')[0])
        self.OffSetErode = int(self.TreeMain.tree.item('I009','value')[0])
        self.BINThresh = int(self.TreeMain.tree.item('I00A','value')[0])
        self.MatrixTop = int(self.TreeMain.tree.item('I00B','value')[0])
        self.DEBUGalg = self.TreeMain.tree.item('I00C','value')[0]
        self.VertField =self.TreeMain.tree.item('I00E','value')[0]
        self.DefCam = self.TreeMain.tree.item('I00F','value')[0]
        self.CalColor = self.TreeMain.tree.item('I011','value')[0]
        self.PrincColorT1 = self.TreeMain.tree.item('I014','value')[0]
        self.R1color1 = self.TreeMain.tree.item('I015','value')[0]
        self.R1color2 = self.TreeMain.tree.item('I016','value')[0]
        self.R1color3 = self.TreeMain.tree.item('I017','value')[0]
        self.PrincColorT2 = self.TreeMain.tree.item('I019','value')[0]
        self.R2color1 = self.TreeMain.tree.item('I01A','value')[0]
        self.R2color2 = self.TreeMain.tree.item('I01B','value')[0]
        self.R2color3 = self.TreeMain.tree.item('I01C','value')[0]
        self.DEBUG = self.TreeMain.tree.item('I01E','value')[0]
        self.EXECMode = self.TreeMain.tree.item('I01F','value')[0]
        
        
        #Configurando as entradas para a forma mais genêrica
        self.UseMode = self.format_var(self.UseMode)
        self.CalColor = self.format_var(self.CalColor)
        self.PrincColorT1 = self.format_var(self.PrincColorT1)
        self.R1color1 = self.format_var(self.R1color1)
        self.R1color2 = self.format_var(self.R1color2)
        self.R1color3 = self.format_var(self.R1color3)
        self.PrincColorT2 = self.format_var(self.PrincColorT2)
        self.R2color1 = self.format_var(self.R2color1)
        self.R2color2 = self.format_var(self.R2color2)
        self.R2color3 = self.format_var(self.R2color3)
        self.EXECMode = self.format_var(self.EXECMode)
        self.DEBUG = self.format_var(self.DEBUG)
        self.DEBUGalg = self.format_var(self.DEBUGalg)
        
        #Tratando as strings
        #Observando Debug
        if(self.DEBUGalg == 'true'):
            self.DEBUGA = True
        elif(self.DEBUGalg == 'false'):
            self.DEBUGA = False
        else:
            self.DEBUGA = False
        
        
        #Observa qual modo o emulador foi configurado.
        if(self.UseMode== 'camera'): #Modo camera
            self.Mode = MODE_USB_CAM
            
        elif(self.UseMode == 'imagem'): #Modo Imagem
            self.Mode = MODE_IMAGE
            
        elif(self.UseMode == 'video'):
            self.Mode = MODE_VIDEO_CAM
            
        else:
            print('[EMULADOR] Valor inválido')
            self.Mode = MODE_DEFAULT
            self.stop() #Para o emulador.
            
        #CÂMERA => camera
    #Método apenas para ver quais variáveis está no emulador.
    def show_variables(self):
        msg=f"""
        [EMULADOR]
        ====Emulador===
        CamUSB: {self.CamUSB}
        ImgPath: {self.ImgPath}
        VideoPath: {self.VideoPath}
        UseMode: {self.UseMode}
        
        OffSetBord: {self.OffSetBord}
        OffSetErode: {self.OffSetErode}
        BINThresh: {self.BINThresh}
        MatrixTop: {self.MatrixTop}
        DEBUGalg: {self.DEBUGalg}
        
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
        print("[EMULADOR] Configurando variaveis")
        self.Viewer.config()
        self.DebugViewer.config()
        
        #Inicializa o viewer
        if(self.Mode== MODE_USB_CAM): #Modo camera
            print('[EMULADOR] Emulador em modo de processamento de imagem da Camera USB')
            #Configurando Viewer para modo de exibição de câmera            
            #Entrada do vídeo
            self.capture = cv2.VideoCapture(self.IdCap)
            self.btn_run.pack_forget() # torna o botão "run" invisível
            self.btn_stop.pack(fill=BOTH, expand=1) # torna o botão "stop" visível
            self.isRuningCam = True #Camera Não pausada
            self.delay = 14 #14ms
            self.processUSB()
            
            
        elif(self.Mode ==  MODE_IMAGE): #Modo Imagem
            print('[EMULADOR] Emulador em modo de processamento de Imagem')
            #Configurar viewer para modo de exibição imagem
            #Entrada do vídeo
            self.btn_stop.pack_forget() # torna o botão "run" invisível
            self.btn_run.pack(fill=BOTH, expand=1) # torna o botão "stop" visível
            self.processImage()
            
        elif(self.Mode == MODE_VIDEO_CAM):
            print('[EMULADOR] Emulador em modo de processamento de Video')
            #configurar viewer para modo de exibição de vídeo
            self.btn_stop.pack_forget() # torna o botão "run" invisível
            self.btn_run.pack(fill=BOTH, expand=1) # torna o botão "stop" visível
            self.processVideo()
            
        else:
            self.Mode == MODE_DEFAULT
            print('[EMULADOR] Entrada inválida')
            self.btn_stop.pack_forget() # torna o botão "run" invisível
            self.btn_run.pack(fill=BOTH, expand=1) # torna o botão "stop" visível
            self.stop() #Para o emulador.
        
    
    #Método para Parar a Emulação.
    def stop(self):
        print('[EMULADOR] Emulador teve sua execução parada.')
        #Inicializa o viewer
        if(self.Mode== MODE_USB_CAM): #Modo camera
            #Configurando Viewer para modo de exibição de câmera
            #Entrada do vídeo
            self.isRuningCam = False #Camera Não pausada
            self.capture.release() #Libera a câmera
            self.btn_run.pack_forget() # torna o botão "run" invisível
            self.btn_stop.pack(fill=BOTH, expand=1) # torna o botão "stop" 
            
        elif(self.Mode ==  MODE_IMAGE): #Modo Imagem
            #Configurar viewer para modo de exibição imagem
            #Entrada do vídeo
            self.btn_stop.pack_forget() # torna o botão "run" invisível
            self.btn_run.pack(fill=BOTH, expand=1) # torna o botão "stop" visível
            
        elif(self.Mode == MODE_VIDEO_CAM):
            #configurar viewer para modo de exibição de vídeo
            self.btn_stop.pack_forget() # torna o botão "run" invisível
            self.btn_run.pack(fill=BOTH, expand=1) # torna o botão "stop" visível
            
        else:
            self.Mode = MODE_DEFAULT
            self.btn_stop.pack_forget() # torna o botão "run" invisível
            self.btn_run.pack(fill=BOTH, expand=1) # torna o botão "stop" visível
        
        #Configurando para base novamente
        self.Mode = MODE_DEFAULT
        self.Viewer.default_mode()
        self.DebugViewer.default_mode()

    #Formatando valores para o caso mínimo
    def format_var(self, var):
        var = unidecode.unidecode(var)
        var = var.lower()
        return var
    
    #Definindo processos do emulador
    #processo para Camera
    def processUSB(self):
        print(self.DEBUGA)
        ret, self.frame = self.capture.read()
        if self.isRuningCam and ret:
        #Apenas detectar o campo por via de dúvidas
            binary_treat, frame, rect_vertices, frame_reduce = detect_field(self.frame, self.DEBUGA,self.OffSetBord,self.OffSetErode, self.MatrixTop, self.BINThresh)
            self.Viewer.show(frame)
            self.DebugViewer.show(binary_treat)
            self.ResulViewer.show(frame_reduce)

        self.Viewer.window.after(self.delay, self.processUSB)
        
    #Processo para imagem
    def processImage(self):
        print("[EMULADOR] Processando imagem: ",self.ImgPath)

        #Chama o algorítmo
        '''
        try:
            self.img = load_image(self.ImgPath)
            try:
                #Detectando Campo
        
                binary_treat, frame, rect_vertices = detect_field(self.img, False,self.OffSetBord,self.OffSetErode, self.MatrixTop, self.BINThresh)
                try:
                    #Detectando bola
                    img, ball, binaryBall = detect_ball(frame, orange, True)
                    try:
                        #Detectando players
                        imgDebug, binaryPlayer, playersCount, AlliesCount, EnemiesCount = detect_players(img, binaryBall, yellow, purple, True)
                        #Exibindo
                        self.Viewer.show(imgDebug)
                        self.DebugViewer.show(binaryPlayer)
                    except:
                        print("Ocorreu um problema em detectar os jogadores")
                        self.Viewer.default_mode()
                        self.DebugViewer.default_mode()
                except:
                    print("Ocorreu um problema em detectar a bola")
                    self.Viewer.default_mode()
                    self.DebugViewer.default_mode()
            except:
                print("Ocorreu um problema em detectar o campo")
                self.Viewer.default_mode()
                self.DebugViewer.default_mode()                    
        except:
            print("Ocorreu um problema em carregar a imagem. ")
            
            self.Viewer.default_mode()
            self.DebugViewer.default_mode()
        '''
        self.img = load_image(self.ImgPath)
        #Apenas detectar o campo por via de dúvidas
        binary_treat, frame, rect_vertices, frame_reduce = detect_field(self.img, self.DEBUGA,self.OffSetBord,self.OffSetErode, self.MatrixTop, self.BINThresh)
        self.Viewer.show(frame)
        self.DebugViewer.show(binary_treat)
        self.ResulViewer.show(frame_reduce)

    #Processo para vídeo
    def processVideo(self):
        print(self.VideoPath)
        print("[EMULADOR] Processando vídeo")  
        
    
    
    #Definição de threads para exibição do processamento
    def startCameraThread(self):
        try:
            self.isRuningCam = True
            self.capture = cv2.VideoCapture(self.IdCap)
            self.thread = threading.Thread(target=self.processUSB)
            self.thread.start()
        except:
            print("Tem erro nessa linha")
    
    #parar a thread da camera
    def stopCameraThread(self):
        self.is_running = False 
        
#SEGURANÇA
if __name__ == "__main__":
    print("[EMULADOR] Módulo sendo executado como funcao principal")

