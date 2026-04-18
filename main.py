from functions import extracaoGPS, conversorDMS, coordsGrid, gridsortomosaico
import time

inicio_etapa = time.time() #Cronometro de exec

#executa a recursividade e salva a tabela
_df = extracaoGPS(r'C:\Users\joaof\PycharmProjects\ExtratorDePosiçãoGPS\FotosParaExtração', True) #Resgata todas as imagens
print(f"Tempo Extração: {time.time() - inicio_etapa:.2f} segundos") #Printa tempo percorrido

#Transforma as coordenadas em Coordenadas Padrão DMS "Minutos e segundos"
_df = conversorDMS(_df)
print(f"Tempo Conversão: {time.time() - inicio_etapa:.2f} segundos") #Printa tempo percorrido

#gera as informações para a grid
coordsGrid('GpsDmsCords.txt', 50)
print(f"Tempo Processamento Grid: {time.time() - inicio_etapa:.2f} segundos") #Printa tempo percorrido

#aplica o grid no ortomosaico
gridsortomosaico('GpsGrids.txt',r'C:\Users\joaof\PycharmProjects\ExtratorDePosiçãoGPS\Ortomosaico\Zoolgico-Mogi-Mirim-16-04-2026-High-Res-orthophoto.tif',50)
print(f"Tempo total de execução: {tempo_total:.2f} segundos") #Printa tempo percorrido