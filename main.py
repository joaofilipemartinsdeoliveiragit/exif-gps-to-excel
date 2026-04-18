from functions import extracaoGPS, conversorDMS, coordsGrid, gerarPontosCentro, gridsortomosaico, run
import time

#Configs

_pastaFotosExtração = r'C:\Users\joaof\PycharmProjects\ExtratorDePosiçãoGPS\FotosParaExtração' #Caminho absoluto das fotos
_Ortomosaico = r'C:\Users\joaof\PycharmProjects\ExtratorDePosiçãoGPS\Ortomosaico\Ortomosaico.tif' #Caminho absoluto para o ortomosaico
_SimpleLog = True                                 #True caso você queira que o tempo seja printado na tela, false caso não queira que as informações sejam printadas na tela
_saveExtracao = False                              #salva o Dataframes em formatdo CSV de gerado pela função extracaoGPS
_saveDms = False                                   #salva o Dataframes em formatdo CSV de gerado pela função conversorDMS
_saveGrid = False                                  #salva o Dataframes em formatdo CSV de gerado pela função coordsGrid
_saveCentro = True                                 #salva o Dataframes em formatdo CSV de gerado pela função coordsGrid
_saveOrtomosaico = True                            #salva o Dataframes em formatdo CSV de gerado pela função gridsortomosaico
_aresta  = 25                                      #Tamanho da aresta do quadrado em metros


#-------------------------------------------------------------------------------------------

if _SimpleLog: _start = time.time() #Inicia cronometro
_logReister = []

if _SimpleLog: print(f"inicio etapa 1 'pastas'")
saveAdress = run() #cria a pasta para salvar os arquivos /// Retorna nome da pasta criada
if _SimpleLog: print(f"Tempo Criação de pasta: {time.time()-_start:.2f} segundos") #Printa tempo percorrido

#executa a recursividade e salva a tabela
if _SimpleLog: print(f"inicio etapa 2 'Extração'")
_df = extracaoGPS(_pastaFotosExtração, _saveExtracao, saveAdress) #Resgata todas as imagens
if _SimpleLog: print(f"Tempo Extração: {time.time()-_start:.2f} segundos") #Printa tempo percorrido

#Transforma as coordenadas em Coordenadas Padrão DMS "Minutos e segundos"
if _SimpleLog: print(f"inicio etapa 3 'ConversãoDMS'")
_df = conversorDMS(_df, _saveDms, saveAdress)
if _SimpleLog: print(f"Tempo Conversão: {time.time()-_start:.2f} segundos") #Printa tempo percorrido

#gera as informações para a grid
if _SimpleLog: print(f"inicio etapa 4 'ortomosaico'")
_df = coordsGrid(_df, _aresta, _saveGrid, saveAdress)
if _SimpleLog: print(f"Tempo Processamento Grid: {time.time()-_start:.2f} segundos") #Printa tempo percorrido

#Calculo o centro das grids
if _SimpleLog: print(f"inicio etapa 5 'centro das grids'")
gerarPontosCentro(_df, _aresta, _saveCentro, saveAdress)
if _SimpleLog: print(f"Tempo Processamento centro das grids: {time.time()-_start:.2f} segundos") #Printa tempo percorrido

#aplica o grid no ortomosaico
if _SimpleLog: print(f"inicio etapa 6 'ortomosaico'")
gridsortomosaico(_aresta,_Ortomosaico,_df, _saveOrtomosaico, saveAdress)
if _SimpleLog: print(f"Tempo total de execução: {time.time()-_start:.2f} segundos") #Printa tempo percorrido