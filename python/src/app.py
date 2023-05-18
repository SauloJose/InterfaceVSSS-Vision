#========================================================
    #INTERFACE GUI para DEBUGAR o algorítmo.
    # PinBOT Vision SYSTEM  (PVS)
    # Versão 1.0
    # Autores: Saulo José
    #           --
    #           --
#========================================================
#Importando módulos
from modulos import *
from TreeMenu import TreeMenu
from viewer import MyViewer
from Emulador import Emulator

#Variável de controle para decidir se foi ou não a primeira vez que o programa foi executado
execution = False

#Criando aplicação com o tkinter
class App():
    #Definindo construtor
    def __init__(self):
        #criando raiz
        root=Tk()
        self.root = root
        self.menu = None # criando a variável de instância aqui
        #chamando janela
        self.window()

        #configurando espaços
        self.frame_window()
        self.frame_config()
        
        #Adicionando Widgets
        self.widgets_image_frame()
        self.widgets_config_frame()
        self.widgets_emulate_frame()

        #Adicionando menu
        self.Menu()
        
        #Gerando Emulador
        #Configurando Viewer
        self.viewer  = MyViewer(self.aba1)  
        
        #Criando emulador
        self.Emulador = Emulator(self.menu, self.viewer, 0, self.btn_run, self.btn_stop)
        
        #executando looping
        root.mainloop()

    #Definindo janela
    def window(self):
        self.root.title("VSSS Vision - PINBOT")
        self.root.configure(background="#dfe3ee")
        self.root.geometry("1100x750")
        self.root.resizable(False, False)
    
    #Função para definir os frames
    def frame_window(self):
        #Setando janela de configurações
        self.config_frame = Frame(self.root, bg="white")
        self.config_frame.place(relx=0.01,rely=0.015, relwidth=0.29,relheight=0.97)
        #Gerando três subframes dentro 
        #Setando frame para imagem
        self.image_frame = Frame(self.root,bg="white")
        self.image_frame.place(relx=0.31,rely=0.015, relwidth=0.68,relheight=0.68)

        #Setando frame com coordenadas dos robôs
        self.bots_frame = Frame(self.root, bg="white")
        self.bots_frame.place(relx=0.31,rely=0.72, relwidth=0.68,relheight=0.265)

    #definindo entradas
    def frame_config(self):
        #frame de ação das 
        self.action_frame=Frame(self.config_frame, bg="white")
        self.action_frame.place(relx=0,rely=0, relwidth=1,relheight=0.90)

        #frame para emular
        self.emulate_frame=Frame(self.config_frame, bg="red")
        self.emulate_frame.place(relx=0,rely=0.90, relwidth=1,relheight=0.10)
    
    #Configurando os widgets do frame de imagem
    def widgets_image_frame(self):
        #Criando as abas
        self.abas = ttk.Notebook(self.image_frame)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        #Configuração das abas
        self.aba1.configure(background="black")
        self.aba2.configure(background="black")

        self.abas.add(self.aba1, text="View")
        self.abas.add(self.aba2, text="Debug")

        self.abas.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    #Adicionando widgets do config frame
    def widgets_config_frame(self):
        #Gerando treeview
        self.exec = execution
        # Define o estilo para o Treeview
        self.menu = TreeMenu(self.action_frame)
        self.menu.pack(fill=BOTH, expand=True)
        #Sistema de visão - PAI GERAL
        if(self.exec):
            print('Configurações de Fábrica')
            self.build_tree_menu()

            #Modificando o valor para contabilizar como nova execução
            self.exec = False
            #Salvando as configurações em arquivo Json
            try:
                self.menu.save_to_json('config')
            except:
                print('por algum motivo, não foi possível salvar o json')
        else:
            try:
                print('Carregando arquivo da memoria')
                self.menu.load_from_json_file('config.json')
                print("carregadas sucesso.")
            except:
                print("Não foi possível puxar o arquivo da memória. Será reiniciado o sistema")
                #Rechamando a função
                self.build_tree_menu()
                self.exec = True
                print('Configurações de Fábrica')
                self.menu.save_to_json('config')


        #Adicionando evento de duplo clique

        self.save_label = Label(self.action_frame, text="Salvar as configurações")
        self.save_label.place(relx=0.1, rely=0.85, relwidth=0.8, relheight=0.05)
        self.save_label.config(fg="black",bg="white")
        self.save_button = Button(self.action_frame, text='Salvar', command=self.save_config)
        self.save_button.place(relx=0.3, rely=0.90, relwidth=0.4, relheight=0.05)

    #Adicionando funcionalidades da emulação
    def widgets_emulate_frame(self):
        #Aqui é o frame para iniciar a emulação, com base nos dados.
        self.Label_run_emulate = Label(self.emulate_frame,text="Estado da Emulação")
        self.Label_run_emulate.pack(fill=BOTH, expand=1)
        self.btn_run = Button(self.emulate_frame, text="Run", width=2,height=1,bg="darkgray",command=self.init_emulate)
        self.btn_run.pack(fill=BOTH, expand=1)
        self.btn_stop= Button(self.emulate_frame, text="Stop", width=2,height=1,bg="darkgray",command=self.stop_emulate)
        self.btn_stop.pack_forget()
        
        #Medida de segurança para manter a variável sempre bem definida.
        self.menu.att_node_id('I01F','Parado')
        self.menu.save_to_json('config')
        
    
    #definindo menu
    def Menu(self):
        self.menubar= Menu(self.root)
        self.root.config(menu=self.menubar)
        self.filemenu1 = Menu(self.menubar)
        self.filemenu2 = Menu(self.menubar)

        def quit_app() -> None:
            self.root.destroy()

        def reset_app() -> None:
            print("[APP] retornando a configuração de fábrica")
            self.stop_emulate()
            self.menu.clear_tree()
            self.menu.load_from_json_file('src/data/reset.json')
            self.menu.save_to_json('config')


        #Adicionando um menu
        self.menubar.add_cascade(label="Opções",menu=self.filemenu1)
        self.menubar.add_cascade(label="Sobre", menu=self.filemenu2)

        #Adicionando comandos no menu
        #Comando de reiniciar todas as configurações para a de fábrica.
        self.filemenu1.add_command(label= 'Retornar ao Padrão', command= reset_app)
        self.filemenu1.add_command(label = "Sair", command= quit_app)
    
    # Função para salvar configurações num json
    def save_config(self):
        # Obtém os dados da TreeView
        self.data = self.menu.get_tree_data()
        # Salva os dados em um arquivo JSON
        with open('config.json', 'w',encoding="utf-8") as f:
            json.dump(self.data, f,ensure_ascii=False)
        print('[APP] config salvas com sucesso!')

    #Função base para construír a árvore padrão
    def build_tree_menu(self):
        SysVision = self.menu.add_node('','SysVisPinbot','Sistema de Visão', value='')
        #Entrada de dados - FILHO DO SYS
        EntryData=self.menu.add_node(SysVision,'EntryData','Entrada de dados', value='')
        self.menu.add_node(EntryData,'CamPth','Câmera USB', value='---')
        self.menu.add_node(EntryData,'ImagePath','Imagem Path', value='---')
        self.menu.add_node(EntryData,'VideoPath','Vídeo Path', value='---')
        self.menu.add_node(EntryData,'UseMode','Modo de Uso', value='Camera')
        #Calibração do algorítmo de reconhecimento
        AlgRec = self.menu.add_node(SysVision,'Algoritm','Calibração do algorítmo',value='')
        self.menu.add_node(AlgRec,'offsetW','Borda da janela', value='10')
        self.menu.add_node(AlgRec,'offSetErode','offSet da Erosão', value='3')
        self.menu.add_node(AlgRec,'Threshold','Binarização Threshold', value='245')
        self.menu.add_node(AlgRec,'DimMatrx','Dim. Matriz TOPHAT', value='25')
        self.menu.add_node(AlgRec,'DebugAlg','Debug do Algorítmo', value='False')     
        #Calibração da câmera - FILHO DO SYS
        CalCamera=self.menu.add_node(SysVision,'CamCalibration','Calibração da Câmera', value='')
        self.menu.add_node(CalCamera,'FieldVertices','Extremos do Campo', value='- , -, -, -')
        self.menu.add_node(CalCamera,'CampDeforms','Deformações', value='N°,3')
        #Calibração das Cores - FILHO DO SYS
        CalColor=self.menu.add_node(SysVision,'ColorCalibration','Calibração das Cores', value='')
        self.menu.add_node(CalColor,'Color','Cor', value='Azul')
        #Configuração dos times - FILHO DO SYS 
        ConfigTeam=self.menu.add_node(SysVision,'TeamConfigs','Configurações dos Times', value='')
        Team1= self.menu.add_node(ConfigTeam,'Team1','Time 1', value='')
        self.menu.add_node(Team1,'Team1Color','Cor Principal T1',value='Azul')
        self.menu.add_node(Team1,'T1Bot1','T1_robo 1',value='roxo')
        self.menu.add_node(Team1,'T1Bot2','T1_robo 2',value='Verde')
        self.menu.add_node(Team1,'T1Bot3','T1_robo 3',value='Vermelho')
        Team2= self.menu.add_node(ConfigTeam,'Team2','Time 2', value='')
        self.menu.add_node(Team2,'Team2Color','Cor Principal T2',value='Amarelo')
        self.menu.add_node(Team2,'T2Bot1','T2_robo 1',value='Verde')
        self.menu.add_node(Team2,'T2Bot2','T2_robo 2',value='Roxo')
        self.menu.add_node(Team2,'T2Bot3','T2_robo 3',value='Rosa')
        
        #Configurações do Emulador - FILHO DO SYS
        ConfigEmulator=self.menu.add_node(SysVision,'EmulatorConfig','Configurações do Emulador', value='')
        self.menu.add_node(ConfigEmulator,'Debug','Debug', value='False')
        self.menu.add_node(ConfigEmulator,'ExectState','Estado de Execução', value='Parado')

        self.DataIDs=[SysVision, EntryData, CalCamera, CalColor, ConfigTeam, Team1,Team2,ConfigEmulator]

    def reset_fabric_menu(self):
        #Gerando treeview
        self.exec = execution
        self.config_frame.destroy()
        # Define o estilo para o Treeview
        self.menu = TreeMenu(self.action_frame)
        self.menu.pack(fill=BOTH, expand=True)
        #Sistema de visão - PAI GERAL

        try:
            print('[RESET] - Resetando configurações')
            self.menu.load_from_json_file('reset.json')
            print("carregadas sucesso.")
        except:
            print("[RESET]- Não foi possível puxar o arquivo da memória. Será reiniciado o sistema")
            #Rechamando a função
            self.build_tree_menu()
            self.exec = True
            print('[RESET] - Configurações de Fábrica')
            self.menu.save_to_json('config')

        
        #Adicionando evento de duplo clique
        self.save_label = Label(self.action_frame, text="Salvar as configurações")
        self.save_label.place(relx=0.1, rely=0.85, relwidth=0.8, relheight=0.05)
        self.save_label.config(fg="black",bg="white")
        self.save_button = Button(self.action_frame, text='Salvar', command=self.save_config)
        self.save_button.place(relx=0.3, rely=0.90, relwidth=0.4, relheight=0.05)

    #MISSÃO ATUAL -> BOTÃO DE RUN E STOP.
    def init_emulate(self):
        #Iniciando Emulação
        print("[APP] Emulação Iniciada")
        self.Emulador.load_vars()
        self.Emulador.show_variables()
        
        #Puxa variáveis que estão na árvore
        self.menu.save_to_json('config') #Salvando os dados antes de iniciar a coleta de dados.

        #Gerando o Emulador e dando início a ele.    
        self.Emulador.init() #Inicializa o emulador
        self.menu.att_node_id('I019','Em execução.')
        self.menu.save_to_json('config')

    def stop_emulate(self):
        self.Emulador.stop()
        #self.viewer.destroy_viewer()
        self.btn_stop.pack_forget() # torna o botão "run" invisível
        self.btn_run.pack(fill=BOTH, expand=1) # torna o botão "stop" visível
        
        self.menu.att_node_id('I01F','Parado')
        self.menu.save_to_json('config')

    #Função para carregar os dados da árvore em conjuntos chave/valor
    def load_variables_tree(self):
        #Carregando os dados
        data = self.menu.get_tree_data()
        return data
        
#Chamando aplicação
if __name__ == "__main__":
    print("[APP] Módulo sendo executado como funcao principal")
