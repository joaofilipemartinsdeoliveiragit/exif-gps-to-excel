from functions import extracaoGPS, conversorDMS, coordsGrid, gridsortomosaico, run
import time

#Configs

_SimpleLog = True #True caso você queira que o tempo seja printado na tela, false caso não queira que as informações sejam printadas na tela
_pastaFotosExtração = r'...\ExtratorDePosiçãoGPS\FotosParaExtração'
_Ortomosaico = r'...\Ortomosaico\Ortomosaico.tif'


#-------------------------------------------------------------------------------------------

if _SimpleLog == True: _start = time.time() #Inicia cronometro

if _SimpleLog == True: print(f"inicio etapa 1 'pastas'")
saveAdress = run() #cria a pasta para salvar os arquivos /// Retorna nome da pasta criada
if _SimpleLog == True: print(f"Tempo Criação de pasta: {time.time()-_start:.2f} segundos") #Printa tempo percorrido

#executa a recursividade e salva a tabela
if _SimpleLog == True: print(f"inicio etapa 2 'Extração'")
_df = extracaoGPS(_pastaFotosExtração, True, saveAdress) #Resgata todas as imagens
if _SimpleLog == True: print(f"Tempo Extração: {time.time()-_start:.2f} segundos") #Printa tempo percorrido

#Transforma as coordenadas em Coordenadas Padrão DMS "Minutos e segundos"
if _SimpleLog == True: print(f"inicio etapa 3 'ConversãoDMS'")
_df = conversorDMS(_df, True, saveAdress)
if _SimpleLog == True: print(f"Tempo Conversão: {time.time()-_start:.2f} segundos") #Printa tempo percorrido

#gera as informações para a grid
if _SimpleLog == True: print(f"inicio etapa 4 'ortomosaico'")
_df = coordsGrid(_df, 50, True, saveAdress)
if _SimpleLog == True: print(f"Tempo Processamento Grid: {time.time()-_start:.2f} segundos") #Printa tempo percorrido

#aplica o grid no ortomosaico
if _SimpleLog == True: print(f"inicio etapa 5 'ortomosaico'")
gridsortomosaico(50,_Ortomosaico,_df, True, saveAdress)
if _SimpleLog == True: print(f"Tempo total de execução: {time.time()-_start:.2f} segundos") #Printa tempo percorrido