import os
import math
import pandas as pd
from PIL import Image

#Recursividade para a extração dos dados
def extracaoGPS(Endereco):
    _ListaDeCoordenadas = []
    #Executa imagem por imagem
    for n in Endereco:
        _info = {'Arquivo':os.path.basename(n),
                 'Latitude':None,
                 'Longitude':None}
        _cords = None
        #verifica se é possivel, E caso não de erro executa todo o processo de resgatar a posicção, caso de erro pula para o except
        try:
            _img = Image.open(n)
            _imgExif = _img._getexif()
            _cords = _imgExif.get(34853)
            if _cords and not math.isnan(_cords[2][0]):
                _info['Latitude'] = _cords[2]
                _info['Longitude'] = _cords[4]
        except:
            pass
        _ListaDeCoordenadas.append(_info)
    return pd.DataFrame(_ListaDeCoordenadas)

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