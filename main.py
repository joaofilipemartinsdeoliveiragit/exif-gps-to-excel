import os
from PIL import Image
from functions import extracaoGPS, conversorDMS, coordsGrid, fotoPorFoto

#Processo de resgatar as imagens da pasta
#_arquivoscep = fotoPorFoto(r'C:\Users\joaof\PycharmProjects\ExtratorDePosiçãoGPS\FotosParaExtração')

#executa a recursividade e salva a tabela
_df = extracaoGPS(r'C:\Users\joaof\PycharmProjects\ExtratorDePosiçãoGPS\FotosParaExtração') #Resgata todas as imagens

#Transforma as coordenadas em Coordenadas Padrão DMS "Minutos e segundos"
conversorDMS(_df)

#Enviar arquivo CSV das coordenadas
coordsGrid('GpsDmsCords.txt', 50)