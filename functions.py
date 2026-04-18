import os
import pandas as pd
from PIL import Image
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#Função para extração do gps/metadados das fotos
def extracaoGPS(Endereco: str, save: bool):
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
    if save == True: df_final.to_csv('GpsCords.txt', sep=',', index=False)
    return pd.DataFrame(_ListaDeCoordenadas)

#Função de calculo utilizado na função conversorDMS
def calculo(df):
    if isinstance(df, tuple) and len(df) == 3:
        _h, _m, _s = df
        return _h + (_m / 60.0) + (_s / 3600.0)
    return df

#Converte as posições gps para o formato DMS
def conversorDMS(df):
    df['Latitude'] = df['Latitude'].apply(calculo)
    df['Longitude'] = df['Longitude'].apply(calculo)
    df.loc[df['N/S'] == 'S', 'Latitude'] *= -1
    df.loc[df['W/E'] == 'W', 'Longitude'] *= -1
    df.to_csv('GpsDmsCords.txt', sep=',', index=False)
    return df

#Gera as informações de grid, o ponto 0,0 de cada quadrante e apaga os quadrados repetidos
def coordsGrid(csv: str ,lado: int):
#Pega as coodenadas inicias ponto 0 , 0 de cada quadrado, e apaga as coordenas que estão no mesmo quadrado
    _info = pd.DataFrame()
    _tamanhoLado = 0.000009 * lado
    df = pd.read_csv(csv) #abre o Dataframe
    df['grid_lat'] = (df['Latitude'] / _tamanhoLado).apply(int) * _tamanhoLado # salva a equação de calcular o quadrado e aplica linha por linha e adiciona em um dicionario
    df['grid_lon'] = (df['Longitude'] / _tamanhoLado).apply(int) * _tamanhoLado #salva a equação de calcular o quadrado e aplica linha por linha e adiciona em um dicionario
    _grids= df.drop_duplicates(subset=['grid_lat', 'grid_lon']) #Apaga todas as grids repetidas
    _grids.to_csv('GpsGrids.txt', sep=',', index = False) #Salva em um csv
    return

#aplica o desenho das grids no ortomosaico
def gridsortomosaico(txt: str, tif: str ,lado: int):
    _grids = pd.read_csv(txt)
    _tamanhoLado = 0.000009 * lado

    with rasterio.open(tif) as src:
        fig, ax = plt.subplots(figsize=(12, 12))
        show(src, ax=ax)

        # --- DESENHANDO ZONA AMARELA (Zona Limite) ---
        lat_min = _grids['grid_lat'].min() - _tamanhoLado
        lon_min = _grids['grid_lon'].min() - _tamanhoLado
        largura = (_grids['grid_lon'].max() + _tamanhoLado) - lon_min
        altura = (_grids['grid_lat'].max() + _tamanhoLado) - lat_min

        rect_amarelo = patches.Rectangle(
            (lon_min, lat_min), largura, altura, linewidth=1, edgecolor='yellow', facecolor='yellow', alpha=0.1, label='Zona Limite'
        )
        ax.add_patch(rect_amarelo)

        # --- DESENHANDO ZONA VERDE (Zona Saudável) ---
        lat_min = _grids['grid_lat'].min()
        lon_min = _grids['grid_lon'].min()
        largura = _grids['grid_lon'].max() - lon_min
        altura = _grids['grid_lat'].max() - lat_min

        rect_verde = patches.Rectangle(
            (lon_min, lat_min), largura, altura,
            linewidth=1, edgecolor='green', facecolor='green', alpha=0.1, label='Zona Saudável'
        )
        ax.add_patch(rect_verde)

        # --- DESENHANDO ZONA VERMELHA (Zonas com Pragas) ---
        for _, n in _grids.iterrows():
            rect_vermelho = patches.Rectangle(
                (n['grid_lon'], n['grid_lat']),  # Início (0, 0)
                _tamanhoLado,  # Largura (Delta Lon)
                _tamanhoLado,  # Altura (Delta Lat)
                linewidth=1.5, edgecolor='red', facecolor='red', alpha=0.3
            )
            ax.add_patch(rect_vermelho)

        plt.title("Mapa de Prescrição sobre Ortomosaico")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.savefig("Mapa de Prescrição sobre Ortomosaico", dpi=300, bbox_inches='tight')
        plt.savefig("Prescricao_Final.pdf")
        plt.show()
    return


