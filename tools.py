import heapq
import random
import numpy as np, pandas as pd
from scipy.ndimage import label

from survivor import Survivor

def a_star(mapa, inicio: tuple, destino: tuple):
    linhas, colunas = len(mapa), len(mapa[0])
    
    aberta = []
    heapq.heappush(aberta, (0, inicio))  # (f(n), nó)
    g_score = {inicio: 0}  # Custo acumulado para cada nó
    pais = {inicio: None}  # Para reconstruir o caminho
    
    def heuristica(n, destino):
        return abs(n[0] - destino[0]) + abs(n[1] - destino[1])  # Distância Manhattan
    
    while aberta:
        _, atual = heapq.heappop(aberta)
        
        if atual == destino:
            # Reconstrói o caminho
            caminho = []
            while atual:
                caminho.append(atual)
                atual = pais[atual]
            return caminho[::-1]  # Caminho invertido
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Movimentos possíveis
            vizinho = (atual[0] + dx, atual[1] + dy)
            
            # Verificar se o vizinho é válido
            if 0 <= vizinho[0] < linhas and 0 <= vizinho[1] < colunas and mapa[vizinho[0]][vizinho[1]] != 1:
                novo_g_score = g_score[atual] + 1
                
                if vizinho not in g_score or novo_g_score < g_score[vizinho]:
                    g_score[vizinho] = novo_g_score
                    f_score = novo_g_score + heuristica(vizinho, destino)
                    heapq.heappush(aberta, (f_score, vizinho))
                    pais[vizinho] = atual

    return None  # Retorna None se não houver caminho

# Função para garantir conectividade usando label para detectar regiões conectadas
def garantir_conectividade(mapa):
    # Label das regiões conectadas
    labeled_map, num_features = label(mapa == 0)  # Regiões de células '0'
    
    # Se houver mais de uma região, manter apenas a maior e ajustar as demais
    if num_features > 1:
        # Encontrar a região conectada maior
        sizes = np.bincount(labeled_map.ravel())
        max_region = sizes[1:].argmax() + 1  # Ignora o rótulo '0' e encontra o maior rótulo
        
        # Ajusta o mapa para que somente a maior região seja 0
        mapa[labeled_map != max_region] = 1  # Define as outras regiões como obstáculos
    
    return mapa


def obter_sequencias_continuas_de_tamanho(lista, tamanho):
    sequencias = []
    for i in range(len(lista) - tamanho + 1):  # Garantir que há espaço suficiente para uma sequência de 'tamanho'
        sequencia = lista[i:i + tamanho]
        sequencias.append(sequencia)
    return sequencias

def read_positions(filepath: str, N = 100, head = 20):
    df = pd.read_csv(filepath, delim_whitespace=True, skiprows=9, header=None).iloc[:, 1:3]
    df.columns = ["X", "Y"]
    df = df[(df.X < N) & (df.Y < N)].head(head)

    return [row[1:] for row in df.itertuples()]