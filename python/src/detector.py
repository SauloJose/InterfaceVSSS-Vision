# ==========================================================================================
# MÓDULO DE FUNÇÕES PARA ALGORÍTMO DE DETECÇÃO VSS
# Versão 1.1
# Ultima modificação: 19/05/2023
#===========================================================================================
'''
    Obs: O módulo é divido em três tipos de funções de identificação, em ordem de Hierarquia:
    1- Funções Principais
    2- Funções Modulares
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
        dirX = (x+y)*np.sqrt(2)/2*5
        dirY = (-x+y)*np.sqrt(2)/2*5
        
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
        print(info_str)
    
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
        return 0

#======================|| FUNÇÕES AUXILIARES ||=========================================#
'''
    Obs: Funções auxiliares são funções que realizam tarefas básicas que serão
    repetidas diversas vezes no código. Portanto, utilizando elas, será possível gerar
    funções mais complexas que terão um nível mais alto, facilitando a leitura do código.
'''
#Carregar imagem
def load_image(imagePath):
    return cv2.imread(imagePath)

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
def highlight_image(img, dim=25):
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
    cont, __ = cv2.findContours(BinImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    objT = cont[0] #Encontra o objeto maior, nesse caso o campo, e então filtrarei a imagem para esse ponto
    if (len(cont)==0):
        print("Ocorreu um problema em reduzir a imagem")
        return BinImg, Img, [0,0,0,0]
    
    try:
        #Obtendo os vértices do retângulo
        x,y,w,h = cv2.boundingRect(objT) #Coordenadas da noav imagem
        
        #Vetor das coordenadas
        cooVetor = [x,y,w,h]
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
    return bin_Reduce, img_Reduce, cooVetor

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
    # 1 -> Aliado
    # 0 -> Inimigo
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
    1. detect_field() - Identificar as bordas do campo, e reduz a imagem
    2. detect_cars() - Identificar os carros na figura
    3. detect_ball() - Identificar a bola no campo
    4. detect_team() - Uma função associada a DetectCars() que irá detectar o time
    do robô, para então guardar as informações
    5. detect_direction() - Identificar qual o vetor direção do robô.
    
    
'''

'''
    - Essa função deve a partir da imagem inicial, detectar o campo, e quando detectar deve retornar os pontos
    do campo na imagem original, bem como os pontos do menor retângulo que envolve o campo.
    - Executa até encontrar uma área superior a um valor experimental 100000.
    - Retorna então os vértices desse polígono, bem como o retângulo enclausulante.
'''
#Função para detectar o campo e retornar os pontos extremos dele
def detect_field(img, debug, offSetWindow=10, offSetErode=0, dimMatrix=25, Trashhold = 235):
    while offSetErode <20:
        try:
            #frame original
            frameOrig = img.copy()

            #Tomando a imagem em tons de cinza
            gray = gray_scale(frameOrig)

            #Aplica filtro de mediana para diminuir ruídos
            blur = median_blur(gray, 3)

            #Realça objetos brilhantes, que nesse caso é o campo
            imagemTratada = highlight_image(blur, dimMatrix)

            #Binarizando a imagem num limiar
            binary = binarize_Up(imagemTratada,Trashhold)

            #Tratando ruídos da imagem binarizada
            binary_treat = treat_noise(binary,offSetErode)
            
            #Reduzindo imagem:
            binary_treat_reduce, frame_reduce, coorVetor = reduce_field(binary_treat, frameOrig, offSetWindow)

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
                        # Extrair os vértices do retângulo [1 2 3 4]
                        rect_vertices = np.array([approx[0][0], approx[1][0], approx[2][0], approx[3][0]], dtype=np.int32)
                        
                        # pontosIniciais = np.float32([[x-d,y-d],[x+w+d,y-d],[x-d,y+h+d],[x+w+d,y+h+d]])
                        # novosExtremos = np.float32([[0,0],[w,0],[0,h],[w,h]])
                        #coor vetor: [x,y,w,h]
                        dd = offSetWindow
                        #Vértices reais na imagem real
                        rect_vertices_true =rect_vertices+np.array([[coorVetor[0]-dd,coorVetor[1]-dd], [coorVetor[0]-dd,coorVetor[1]+dd], [coorVetor[0]+dd,coorVetor[1]+dd], [coorVetor[0]+dd,coorVetor[1]-dd]], dtype=np.int32)
                    
                        if(debug == True):
                            # Desenhar os vértices do retângulo na imagem original
                            cv2.polylines(frameOrig, [rect_vertices_true], True, (0, 0, 255), 4)

                            # Desenhar círculos nos vértices do retângulo
                            for vertex in rect_vertices_true:
                                x, y = vertex
                                cv2.circle(frameOrig, (x, y), 4, (0, 255, 0), -1)

                    except:
                        pass
            # Se chegou até aqui sem erros, retorna os vértices do retângulo
            return binary_treat, frameOrig, rect_vertices_true, frame_reduce
        
        except: #Trata os erros em geral... Provavelmente gerará um bug!
            # Se ocorrer algum erro, incrementa o valor de offSetErode e tenta novamente
            offSetErode += 1
            return binary_treat, frameOrig, np.array([-1,-1,-1,-1],dtype=np.int32), img

#Função para detectar bola
def detect_ball(img, color, debug=False):
    #Cor laranja da bola - depois colocar fora da função
    ballDarkColor = color[0]
    ballLightColor = color[1]
    
    #Convertendo para HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Detecção da bola
    binaryBall = cv2.inRange(imgHSV, ballDarkColor, ballLightColor)

    #Elemento estruturante
    structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,8))
    
    #Operação de fechamento
    binaryBall = cv2.morphologyEx(binaryBall, cv2.MORPH_CLOSE, structuringElement)
    
    #Encontrando contornos da bola
    contours, _ = cv2.findContours(binaryBall, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #Inicializando variáveis para não dar erro
    xb = 0 
    yb = 0
    rb = 0
    
    (xb, yb), rb = cv2.minEnclosingCircle(contours[0])
    rb = int(rb)
    xb=int(xb)
    yb=int(yb)

    if (debug == True):
        #Circulando bola na imagem
        cv2.circle(img, (xb, yb), (rb + 2), (0, 0, 255), 2)
    
    #intância da bola
    boll = Bola(xb,yb,rb)
                   
    return img, boll, binaryBall

#Função para detectar carros
def detect_players(img, binaryBall, alliesColor, enemiesColor, debug=False):
    #Imagem para debug
    imgDegub = img

    #Janela dos jogadores
    playersWindows = [0,0,0,0,0,0]
    playersCount = 0
    alliesCount = 0
    enemiesCount = 0

    alliesPlayers = [0,0,0]
    enemiesPlayers = [0,0,0]

    #Cores dos objetos
    objectsDarkColor = np.array([0,120,155])
    objectsLightColor = np.array([255,255,255])

    #Cor dos aliados
    allyDarkColor = alliesColor[0]
    allyLightColor = alliesColor[1]

    #Cor dos inimigos
    enemyDarkColor = enemiesColor[0]
    enemyLightColor = enemiesColor[1]

    #Convertendo para HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #Encontrando objetos nas cores claras, mas não brancas
    objects = cv2.inRange(imgHSV, objectsDarkColor, objectsLightColor)
    binaryPlayers = cv2.subtract(objects, binaryBall)
    
    #Operação de erosão
    structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
    binaryPlayers = cv2.morphologyEx(binaryPlayers, cv2.MORPH_CLOSE, structuringElement)

    #Encontrando contornos dos jogadores
    players, _ = cv2.findContours(binaryPlayers, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #Tratando os objetos/players e reconhecendo se são aliados  e etc.
    for currentPlayer in players:
        #Encontrando posição de cada um dos carros identificados
        (xp,yp), rp = cv2.minEnclosingCircle(currentPlayer)
        
        #Coordenadas encontradas na imagem original, antes de pegar uma perspectiva menor
        xi = int(xp)
        yi = int(yp)
        ri = int(rp)

        #Objetos com raios maiores que certo valor serão considerados como jogadores
        if(ri > 20):
            #Traçando janelas (winSize x winSize)
            winSize = 100 #Tamanho da janela
            initPt = np.float32([[xi-(winSize/2),yi-(winSize/2)],[xi+(winSize/2),yi-(winSize/2)],[xi-(winSize/2),yi+(winSize/2)],[xi+(winSize/2),yi+(winSize/2)]])
            endPt = np.float32([[0,0],[winSize,0],[0,winSize],[winSize,winSize]])

            #Matriz de transformação para nova perspectiva
            perspecMatrix = cv2.getPerspectiveTransform(initPt, endPt)

            #Criando janelas 100px por 100px para cada carro e guardando essas imagens num vetor
            playersWindows[playersCount] = cv2.warpPerspective(img, perspecMatrix, (winSize,winSize)) 

            #ETAPA 1 - Verificação se é aliado ou inimigo
            #Convertendo para HSV
            windowHSV = cv2.cvtColor(playersWindows[playersCount], cv2.COLOR_BGR2HSV)

            binaryTeam = cv2.inRange(windowHSV, allyDarkColor, allyLightColor)
            object, hierarchy = cv2.findContours(binaryTeam, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if(len(object) >= 1):#Verfica se tem algum carro.
                ally = object[0]
                (xa, ya), ra = cv2.minEnclosingCircle(ally)

                if(int(ra) > 10):
                    #Se entrou aqui, então é aliado
                    #Vetor de jogadores aliados recebendo instâncias da classe Robo
                    alliesPlayers[alliesCount] = Robo(alliesCount, "aliado", xi, yi, ri)
                    alliesPlayers[alliesCount].set_cv2Perspective(playersWindows[playersCount])
                    
                    #Buscando posição das cores em relação a imagem reduzida
                    playerCenterX = winSize/2
                    playerCenterY = winSize/2
                    
                    #Transformando posição para coordenada do quadro reduzido
                    xColor = xa + xi - playerCenterX
                    yColor = ya + yi - playerCenterY
                       
                    #Adiciono informações do (x,y) da cor primária do robô
                    alliesPlayers[alliesCount].update_position(xi, yi, xColor, yColor)
                    
                    #Vetor entre o centro e a cor do robô
                    dx = xColor - xi
                    dy = yColor - yi
                    
                    #Vetor direção do robÔ
                    dirX = int((dx + dy)*np.sqrt(2)/2)*5
                    dirY = int((dy - dx)*np.sqrt(2)/2)*5

                    if(debug==True):
                        #Desenhando círculos na imagem de debug
                        cv2.circle(imgDegub, (xi, yi), ri+5, (0,255,0), 2)
                        #Desenhandp círculos no centro da imagem
                        cv2.circle(imgDegub, (xi, yi), 2, (255,0,0), 2)
                        #Desenhandp círculos no centro da cor
                        cv2.circle(imgDegub, (int(xColor), int(yColor)), 2, (255,0,0), 2)
                        cv2.circle(imgDegub, (xi+dirX, yi+dirY), 2, (255,0,0), 2)
                        
                        cv2.putText(imgDegub,str("aliado")+" "+str(alliesCount), (int(xi-24), int(yi+1.8*ri)), cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255), 1)
                        cv2.putText(imgDegub,"Robo", (int(xi-ri+5),int(yi-1.5*ri)), cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255), 1)
            
            
                        #Desenhando vetor de direção
                        cv2.arrowedLine(imgDegub, (xi, yi), (xi+dirX, yi+dirY), (0,255,0), 1)


                    alliesCount += 1
            else:
                #Vetor de jogadores inimigos recebendo instâncias da classe Robo
                enemiesPlayers[enemiesCount] = Robo(enemiesCount, "inimigo", xi, yi, ri)
                if(debug==True):
                    #Desenhando círculos na imagem de debug
                    cv2.circle(imgDegub, (xi, yi), ri+5, (0,0,255), 2)
                    #Desenhandp círculos no centro da imagem
                    cv2.circle(imgDegub, (xi, yi), 2, (255,0,0), 2)
                    cv2.putText(imgDegub,str("Inimigo")+" "+str(alliesCount), (int(xi-24), int(yi+1.8*ri)), cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255), 1)
                    cv2.putText(imgDegub,"Robo", (int(xi-ri+5),int(yi-1.5*ri)), cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255), 1)
            
                enemiesCount += 1

            playersCount += 1

    return imgDegub, binaryPlayers, playersCount, alliesCount, enemiesCount




#======================|| FUNÇÕES PRINCIPAIS ||=========================#
def main():
    debug = True
    
    #Definição de array de cores (dark, light)
    orange = np.array([[4,100,128], [21,255,255]]) #bola
    yellow = np.array([[23,70,120], [30,255,255]]) #aliados
    purple = np.array([[120,100,100], [170,255,255]]) #inimigos
    
    #instância da bola
    try:
        #Carregando imagem da memória e redimensionando
        frame = load_image("src/vision/campo1.jpg")

        frame = cv2.resize(
            frame,  #imagem original
            None,    #variável que receberá a imagem
            fx=0.7,  #fator no eixo x
            fy=0.7,  #fator no eixo y
            interpolation = cv2.INTER_CUBIC) #método de interpolação
        
        try:
            #Aplica detector de bordas após a binarização
            binary_field, img, field_vertices = detect_field(frame,False,10) #Necessário regular o offset
            
            #Plotando figura de debugq
            if(debug==True): 
                cv2.imshow("Imagem Tratada", img)        
                print(field_vertices)

        except Exception as e:
            print("Algum erro na função detect_field\n",e)
        
        try:
            #Função de detectar a bola
            ballFrame = img
            ballImg, ball, binaryBall = detect_ball(ballFrame, orange, False)
                        
            if(debug==True): 
                cv2.imshow("Bola encontrada", binaryBall)
        
        except Exception as e:
            print("Algum erro na função detect_ball\n",e)
        
        try:
            playerFrame = ballFrame
            binaryPlayers, amountOfPlayers, amountOfAllies, amountOfEnemies = detect_players(playerFrame, binaryBall, purple, yellow, debug)
            
            print("Número de jogadores: ", amountOfPlayers)
            print("Número de aliados: ", amountOfAllies)
            print("Número de inimigos: ", amountOfEnemies)

            if(debug==True): cv2.imshow("Jogadores encontrados", binaryPlayers)

        except Exception as e:
            print("Algum erro na função detect_players\n",e)            

        # Desenhar os vértices do retângulo na imagem original
        if(debug==True):
            cv2.polylines(img, [field_vertices], True, (0, 0, 255), 4)
            # Desenhar círculos nos vértices do retângulo
            for vertex in field_vertices:
                x, y = vertex
                print(x,y)
                cv2.circle(frame, (x, y), 4, (0, 255, 0), 1)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print("Provavelmente não foi possível carregar a imagem\n",e)

    return 0
    

#Identificando se o bloco está sendo utilizado como script e não módulo
if  __name__=='__main__':
    print("O módulo está sendo executado como principal")