import os
import pandas as pd
from PIL import Image
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime

#Cria uma pasta nova para cada projeto
def run():
    pastas_existentes = [d for d in os.listdir('.') if os.path.isdir(d) and d.startswith("Results")]
    proximo_numero = len(pastas_existentes) + 1
    nome_final = f"Results ({proximo_numero}) {datetime.now().strftime("%d-%m-%Y")}"
    if not os.path.exists(nome_final):
        os.makedirs(nome_final)
    return nome_final

#Função para extração do gps/metadados das fotos
def extracaoGPS(Endereco: str, save: bool, nome_final: str):
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
    caminho_completo = os.path.join(nome_final, 'GpsCords.txt')
    if save == True: df_final.to_csv(caminho_completo, sep=',', index=False)
    return pd.DataFrame(_ListaDeCoordenadas)

#Função de calculo utilizado na função conversorDMS
def calculo(df):
    if isinstance(df, tuple) and len(df) == 3:
        _h, _m, _s = df
        return _h + (_m / 60.0) + (_s / 3600.0)
    return df

#Converte as posições gps para o formato DMS
def conversorDMS(txt: int , save: bool, nome_final: str):
    txt['Latitude'] = txt['Latitude'].apply(calculo)
    txt['Longitude'] = txt['Longitude'].apply(calculo)
    txt.loc[txt['N/S'] == 'S', 'Latitude'] *= -1
    txt.loc[txt['W/E'] == 'W', 'Longitude'] *= -1
    caminho_completo = os.path.join(nome_final, 'GpsDmsCords.txt')
    if save == True: txt.to_csv(caminho_completo, sep=',', index=False)
    return txt

#Gera as informações de grid, o ponto 0,0 de cada quadrante e apaga os quadrados repetidos
def coordsGrid(df: int ,lado: int, save: bool, nome_final: str):
    _info = pd.DataFrame()
    _tamanhoLado = 0.000009 * lado

    df  #abre o Dataframe
    df['grid_lat'] = (df['Latitude'] / _tamanhoLado).apply(int) * _tamanhoLado # salva a equação de calcular o quadrado e aplica linha por linha e adiciona em um dicionario
    df['grid_lon'] = (df['Longitude'] / _tamanhoLado).apply(int) * _tamanhoLado #salva a equação de calcular o quadrado e aplica linha por linha e adiciona em um dicionario
    _grids= df.drop_duplicates(subset=['grid_lat', 'grid_lon']) #Apaga todas as grids repetidas
    caminho_completo = os.path.join(nome_final, 'GpsGrids.txt')
    if save == True: _grids.to_csv(caminho_completo, sep=',', index = False) #Salva em um csv
    return _grids

#aplica o desenho das grids no ortomosaico
def gridsortomosaico(lado: int,tif: str,_grids: int, save: bool, nome_final: str):

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
        caminho_completo = os.path.join(nome_final, "Prescricao_Final.pdf")
        if save == True: plt.savefig(caminho_completo)
    return