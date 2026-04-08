import os
from PIL import Image
from functions import extracaoGPS

#Endereço da pasta com as imagens tem que colocar o endereço entre as aspas simples
_cep = r'...\FotosParaExtração'

#Processo de resgatar as imagens da pasta
_arquivoscep = [
    os.path.join(_cep,f)
    for f in os.listdir(_cep)
]

#executa a recursividade e salva a tabela
tabela = (extracaoGPS(_arquivoscep))

#exporta como planilha de excel
tabela.to_excel('GPSTeste.xlsx', index=False)