import os
import pandas as pd
from PIL import Image
import folium

def fotoPorFoto(url):
    _arquivoscep = [
        os.path.join(url, f)
        for f in os.listdir(url)
    ]
    return _arquivoscep

def extracaoGPS(Endereco):
    _ListaDeCoordenadas = []
    _arquivoscep = [ os.path.join(Endereco, f) for f in os.listdir(Endereco)]

    for n in _arquivoscep:
        _info = {'Arquivo':os.path.basename(n),
                 'N/S':None,
                 'Latitude':None,
                 'W/E': None,
                 'Longitude':None}

        #verifica se é possivel, E caso não de erro executa todo o processo de resgatar a posicção, caso de erro pula para o except
        try:
            _img = Image.open(n)    #abre a imagem
            _cords = _img.getexif().get_ifd(34853)  #abre todos os metadados em _imgExif
            _info['N/S'] = _cords[1]
            _info['Latitude'] = _cords[2]
            _info['W/E'] = _cords[3]
            _info['Longitude'] = _cords[4]
        except Exception as e:
            print(f"Erro ao processar {os.path.basename(n)}: {e}")

        _ListaDeCoordenadas.append(_info)
    df_final = pd.DataFrame(_ListaDeCoordenadas)
    df_final.to_csv('GpsCords.txt', sep=',', index=False)
    return pd.DataFrame(_ListaDeCoordenadas)

def calculo(df):
    if isinstance(df, tuple) and len(df) == 3:
        _d, _m, _s = df
        return _d + (_m / 60.0) + (_s / 3600.0)
    return df

def conversorDMS(df):
    df['Latitude'] = df['Latitude'].apply(calculo)
    df['Longitude'] = df['Longitude'].apply(calculo)
    df.loc[df['N/S'] == 'S', 'Latitude'] *= -1
    df.loc[df['W/E'] == 'W', 'Longitude'] *= -1
    df.to_csv('GpsDmsCords.txt', sep=',', index=False)
    return df

#
def coordsGrid(csv: str ,lado: int):
    _info = pd.DataFrame()
    _tamanhoLado = 0.000009 * lado
    df = pd.read_csv(csv) #abre o Dataframe
    df['grid_lat'] = (df['Latitude'] / _tamanhoLado).apply(int) * _tamanhoLado # salva a equação de calcular o quadrado e aplica linha por linha e adiciona em um dicionario
    df['grid_lon'] = (df['Longitude'] / _tamanhoLado).apply(int) * _tamanhoLado #salva a equação de calcular o quadrado e aplica linha por linha e adiciona em um dicionario
    _grids= df.drop_duplicates(subset=['grid_lat', 'grid_lon']) #Apaga todas as grids repetidas
    _grids.to_csv('GpsGrids.txt', sep=',', index = False) #Salva em um csv

    m = folium.Map(location=[_grids['grid_lat'].iloc[0], _grids['grid_lon'].iloc[0]], zoom_start=18) #Pega a primeira coordenada ta lista e Seta como inicial

#Desenhando zona Vermelha (Zonas com pragas)

    for _, n in _grids.iterrows(): # Aplica item por item
        _points = [                                              # Define os pontos do quadrado
            [n['grid_lat'], n['grid_lon']],
            [n['grid_lat'] + _tamanhoLado, n['grid_lon']],
            [n['grid_lat'] + _tamanhoLado, n['grid_lon'] + _tamanhoLado],
            [n['grid_lat'], n['grid_lon'] + _tamanhoLado],
            [n['grid_lat'], n['grid_lon']]
        ]
        folium.Polygon(locations=_points, color='red', fill=True, fill_opacity=0.3,weight=2,popup='Zona de Infestação (Aplicação Necessária)').add_to(m)

# Denhando zona amarela (Zona Limite)

    lat_min = _grids['grid_lat'].min() - _tamanhoLado
    lat_max = _grids['grid_lat'].max() + _tamanhoLado
    lon_min = _grids['grid_lon'].min() - _tamanhoLado
    lon_max = _grids['grid_lon'].max() + _tamanhoLado

    _Point = [
        [lat_min, lon_min],  # Sudoeste
        [lat_max, lon_min],  # Noroeste
        [lat_max, lon_max],  # Nordeste
        [lat_min, lon_max],  # Sudeste
        [lat_min, lon_min]
    ]

    folium.Polygon(locations=_Point, color='Yellow', fill=True, fill_opacity=0.2, weight=1, popup='Zona Limite (Sem informações)').add_to(m)

    # Denhando zona verde (Zona Saudavel)

    lat_min = _grids['grid_lat'].min()
    lat_max = _grids['grid_lat'].max()
    lon_min = _grids['grid_lon'].min()
    lon_max = _grids['grid_lon'].max()

    _Point = [
        [lat_min, lon_min],  # Sudoeste
        [lat_max, lon_min],  # Noroeste
        [lat_max, lon_max],  # Nordeste
        [lat_min, lon_max],  # Sudeste
        [lat_min, lon_min]
    ]

    folium.Polygon(locations=_Point, color='Green', fill=True, fill_opacity=0.2, weight=1, popup='Zona Saudável (Área Total)').add_to(m)
    m.save('Mapa_De_Grids.html')
    return

