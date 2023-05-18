# ==========================================================================================
# MÓDULO DE FUNÇÕES PARA ALGORÍTMO DE DETECÇÃO VSS
# Versão 2.0
# Ultima modificação: 18/05/2023
#===========================================================================================
'''
    Obs: O módulo é divido em três tipos de funções de identificação, em ordem de Hierarquia:
    1- Funções Principais;
    2- Funções Modulares;
    3- Funções Auxiliares.
    
    Funções principais são construídas à partir de funções modulares que são construídas com
    Funções auxiliares (o grau mais baixo).
    
    Funções principais executam tarefas gerais em específico, como identificar todos os robôs
    e suas equipes, Identificar a bola, identificar os extremos do campo. Além de tratamento
    de erros.
    
    Além da definição dos módulo, também é definido os objetos que irão funcionar como abstração
    com o mundo real: robôs, bola e campo.
'''
#importando bibliotecas necessárias para o código
import cv2
import numpy as np

#======================|| DEFINIÇÕES DE CLASSES ||======================================#
#Definição da classe que será a 
class Robo:
    def __init__(self, id, equipe="default", posX=0, posY=0, raio=0):
        #Setando atributos necessários para gerar um objeto do tipo robô
        self.id = int(id)                                                 #Identificador do robô
        self.team = str(equipe)                                           #Nome da Equipe
        self.pos = np.array([int(posX), int(posY)])                       #Vetor posição na imagem
        self.vel = np.array([0, 0])                                       #Vetor velocidade na imagem
        self.radio = int(raio)                                            #Raio do circulo envolvente
        self.dir = np.array([0, 0])                                       #Vetor direção na imagem
        self.team_center = np.array([0, 0])                               #Centro da cor da equipe
        self.window = np.array([[0,0], [0, 0], [0,0], [0,0]])             #Coordenadas da janela na imagem original
        self.CV2Perspective = None                                        #Perspectiva do openCV do carro
    
    #Atualizando a posição do robô
    def update_position(self, posX, posY, colorX, colorY):
        self.pos = np.array([int(posX), int(posY)])
        self.team_center = np.array([int(colorX), int(colorY)])
        
        #Atualizando a direção do robô
        #(x,y) é o vetor diferença entre a posição da cor do robô e a posição centrla do robô
        x = abs(posX - colorX)
        y = abs(posY - colorY)

        #Aplicando transformação para definir a direção real do robô
        dirX = (x+y)*np.sqrt(2)/2*5;
        dirY = (-x+y)*np.sqrt(2)/2*5;
        
        #Observação: Aqui é preciso transformar num vetor unitário
        
        #Definindo a direção atual em que o robô se encontra
        self.dir = np.array([int(dirX), int(dirY)])
        
    #Adicionando as informações da perspectiva do OpenCV
    #Informações da perspectiva para o openCV
    def set_cv2Perspective(self, perspective):                              
        self.CV2Perspective = perspective
    
    #Função de debug para imprimir informações do robô
    def infos(self):
        info_str='''
            =======================
            |Informações do robô {}|
            Equipe: {}
            Posição: {}
            Velocidade: {}
            Raio: {}
            =======================
        '''.format(self.id, self.team,self.pos, self.vel, self.radio)
        print(info_str);
    
    #Adicionando a informação da janela na imagem cuja posição está o robô
    def set_window(self, x, y, w, h):
        self.window = np.array([[x, y], [x, y+h], [x+w, y+h], [x+w, y]])
        
        
#classe que identifica a bola
class Bola:
    # atributos
    pos = np.zeros(2, dtype=np.int32)  # posição x e y da bola
    vel = np.zeros(2, dtype=np.float32)  # velocidade x e y da bola
    raio = 0  # raio do círculo envolvente
    
    # construtor
    def __init__(self, posX=0, posY=0, raio=0):
        self.pos[0] = int(posX)
        self.pos[1] = int(posY)
        self.raio = int(raio)
    
    # método para mudar a posição da bola
    def changeCenter(self, posX, posY, raio):
        self.pos[0] = int(posX)
        self.pos[1] = int(posY)
        self.raio = int(raio)


#Definição da classe campo
class Field:

    #Métodos
    def __init__(self,):
        self.window = np.array([[0,0], [0, 0], [0,0], [0,0]])             #Coordenadas da janela na imagem original
    
    #mudar a posição
    def updatePosition(self, ):
        return 0;

#======================|| FUNÇÕES AUXILIARES ||=========================================#
'''
    Obs: Funções auxiliares são funções que realizam tarefas básicas que serão
    repetidas diversas vezes no código. Portanto, utilizando elas, será possível gerar
    funções mais complexas que terão um nível mais alto, facilitando a leitura do código.
'''
#Carregar imagem
def load_image(imagePath):
    return cv2.imread(imagePath);

#Transformar em tons de cinza (que seja inicialmente RGB)
def gray_scale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

#Aplicar o filtro mediana para possíveis ruídos
def median_blur(image, kernelSize=3):
    return cv2.medianBlur(image, kernelSize)

#Binariza a imagem indo de um limiar até 255
def binarize_Up(image, threshold=150):
    _, binarized = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return binarized

#Tratar ruídos da imagem binarizada
def treat_noise(img, it=1):
    #Elemento estruturante
    elementoEstruturante = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    
    #Processando imagem
    imagemProcessada = cv2.erode(img, elementoEstruturante, iterations = it)
    
    return imagemProcessada


#Recuperando o objeto de maior área
def get_object(image):
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours[0]

#Recuperando coordenadas extremas que englobam o maior objeto
def get_perspective(object):
    x,y,w,h = cv2.boundingRect(object)
    return x,y,x+w,y+h
        
#Função para realçar objetos brilhantes na imagem (campo)
def highlight_image(img, dim):
    #Operação de topHat para itensificar contrástes
    elementoEstruturante = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dim,dim))

    imgProcessada = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, elementoEstruturante)

    #ajuste de contraste
    imagemTratada = cv2.add(imgProcessada, imgProcessada)
    imagemTratada = cv2.add(imgProcessada, imgProcessada)
    
    return imagemTratada

#Função que irá reduzir a imagem original para pegar o tamanho do campo
## PROBLEMA NESSA FUNÇÃO, POIS AO REDUZIR SURGE ALGUNS BUGS
def reduce_field(BinImg, Img, d=10):
    #Diminuindo a dimensão da imagem para caber apenas o campo
    cont, hierarquia = cv2.findContours(BinImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    objT = cont[0] #Encontra o objeto maior, nesse caso o campo, e então filtrarei a imagem para esse ponto
    
    if (len(cont)==0):
        print("Ocorreu um problema em reduzir a imagem")
        return bin_Reduce, img_Reduce
    
    try:
        #Obtendo os vértices do retângulo
        x,y,w,h = cv2.boundingRect(objT) #Coordenadas da nova imagem
        
        #Vetoor de coordenadas.
        coorVetor = [x,y,w,h]
        
        pontosIniciais = np.float32([[x-d,y-d],[x+w+d,y-d],[x-d,y+h+d],[x+w+d,y+h+d]])
        novosExtremos = np.float32([[0,0],[w,0],[0,h],[w,h]])
        
        #Matriz de transformação para nova perspectiva
        matrizPerspectiva = cv2.getPerspectiveTransform(pontosIniciais,novosExtremos)

        #revisando nova imagem para processamento
        img_Reduce = cv2.warpPerspective(Img, matrizPerspectiva, (w,h))
        bin_Reduce = cv2.warpPerspective(BinImg, matrizPerspectiva, (w,h))
    except:
        #Se ele não conseguir, retorna a imagem inicial...
        bin_Reduce = BinImg
        img_Reduce = Img
        
    #Retornando a imagem binária e a imagem original já reduzida.
    return bin_Reduce, img_Reduce, coorVetor;

#Essa função a partir de pontos irá reduzir a imagem original nessa reduzida.
def reduce_window(img, coorVetor, d=10):
    try:
        #recuperando dados do vetor coordenada
        x,y,w,h = coorVetor[0],coorVetor[1],coorVetor[2],coorVetor[3];

        pontosIniciais = np.float32([[x-d,y-d],[x+w+d,y-d],[x-d,y+h+d],[x+w+d,y+h+d]])
        novosExtremos = np.float32([[0,0],[w,0],[0,h],[w,h]])

        #Matriz de transformação para nova perspectiva
        matrizPerspectiva = cv2.getPerspectiveTransform(pontosIniciais,novosExtremos)


        #revisando nova imagem para processamento
        img_Reduce = cv2.warpPerspective(img, matrizPerspectiva, (w,h))

        return img_Reduce
    except:
        #Ocorreu um erro, então retorna a janela já inicial
        return img
    
#Função para exibir objetos das classes
def list_players(teamList):
    amount = len(teamList)

    for i in range(amount):
        print(teamList[i].team, teamList[i].id)
        print("Posição: x =", teamList[i].pos[0], " y =", teamList[i].pos[1])
    
    print("====================")

    
#Função para identificar equipe
def find_team(windowsCar, colorTeam, colorEnemy):
    #Irá a partir da imagem descobrir se é ou não um carro aliado e inimigo
    # Verifica a cor, e dependendo disso irá retornar 2 valores:
    # 1 -> Aliado;
    # 0 -> Inimigo;
    # Além disso, retorna o objeto Robô com as informações necessárias.
    
    #Processo de filtragem
    
    return 0
#======================|| FUNÇÕES MODULARES ||=========================#
'''
    Obs: Funções módulares são funções mais complexas construídas com
    funções auxiliares. Essas funções módulares funcionarão como blocos
    de código para exercer uma determinada função no algorítmo principal
    definido na função main().
    
    As funções modulares principais são:
    1. detect_field() - Identificar as bordas do campo, e reduz a imagem;
    2. detect_cars() - Identificar os carros na figura;
    3. detect_ball() - Identificar a bola no campo;
    4. detect_team() - Uma função associada a DetectCars() que irá detectar o time;
    do robô, para então guardar as informações
    5. detect_direction() - Identificar qual o vetor direção do robô.
    
    
'''
#Função para detectar o campo e retornar os pontos extremos dele
'''
    - Essa função deve a partir da imagem inicial, detectar o campo, e quando detectar deve retornar os pontos
    do campo na imagem original, bem como os pontos do menor retângulo que envolve o campo.
    - Executa até encontrar uma área superior a um valor experimental 100000.
    - Retorna então os vértices desse polígono, bem como o retângulo enclausulante.
'''
def detect_field(img, debug, offSetWindow=10, offSetErode=0, binarizeField =245, dimMatImg = 25):
    try:
        #frame original
        frameOrig = img

        #Tomando a imagem em tons de cinza
        gray = gray_scale(frameOrig)

        #Aplica filtro de mediana para diminuir ruídos
        blur = median_blur(gray, 3)
        
        #Realça objetos brilhantes, que nesse caso é o campo
        imagemTratada = highlight_image(blur, dimMatImg)
        
        #Binarizando a imagem num limiar
        binary = binarize_Up(imagemTratada,binarizeField)
        
        #Tratando ruídos da imagem binarizada
        binary_treat = treat_noise(binary,offSetErode)
        #if(debug == True): cv2.imshow("Imagem tratada", binary_treat)
            
        #Reduzindo imagem:
        binary_treat_reduce, frameReduce, coorVetor= reduce_field(binary_treat, frameOrig, offSetWindow)
            
        #Encontra extremos do paralelogramo
        contours, _ = cv2.findContours(binary_treat_reduce, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #Variável para retornar os vértices
        rect_vertices = np.array([0,0,0,0], dtype=np.int32)

        # Loop através dos contornos encontrados
        for contour in contours:
            # Aproximar o contorno para um polígono com poucos vértices
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Se o polígono tem 4 vértices, então é um retângulo
            if len(approx) == 4:
                try:
                    # Extrair os vértices do retângulo
                    rect_vertices = np.array([approx[0][0], approx[1][0], approx[2][0], approx[3][0]], dtype=np.int32)
                        
                    #Vértices reais na imagem real
                    rect_vertices_true =rect_vertices+np.array([[coorVetor[0],coorVetor[1]], [coorVetor[0],coorVetor[1]], [coorVetor[0],coorVetor[1]], [coorVetor[0],coorVetor[1]]], dtype=np.int32)
                    
                    #Sessão de Debug
                    if(debug == True):
                        # Desenhar os vértices do retângulo na imagem original
                        cv2.polylines(img, [rect_vertices_true], True, (0, 0, 255), 4)
                            
                        for vertex in rect_vertices_true:
                            x, y = vertex
                            cv2.circle(img, (x, y), 4, (0, 255, 0), -1)

                except:
                    pass
        # Se chegou até aqui sem erros, retorna os vértices do retângulo
        return binary_treat, frameReduce, rect_vertices_true, coorVetor
    except: #Trata os erros em geral... Provavelmente gerará um bug!
        # Se ocorrer algum erro, incrementa o valor de offSetErode e tenta novamente
        offSetErode += 1
        return binary_treat, img, img, None
