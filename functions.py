import os
import pandas as pd
from PIL import Image

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
            _info['Latitude'] = _cords[2]
            _info['Longitude'] = _cords[4]
        except:
            pass
        _ListaDeCoordenadas.append(_info)
    return pd.DataFrame(_ListaDeCoordenadas)