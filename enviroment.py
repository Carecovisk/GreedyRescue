from survivor import Survivor
import pandas as pd
import numpy as np
from scipy.ndimage import label

class Enviroment:

    def __init__(self, survivors: list[Survivor], disaster_center: tuple, disaster_dimensions: tuple) -> None:
        self.survivors = survivors
        self.rescue_path: list[int] = []
        self.disaster_center = disaster_center
        self.disaster_dimensions = disaster_dimensions
    
    def surviorsRescued(self):
        sum = 0
        for s in self.survivors:
            if s.isAlive:
                sum += 1
        return sum
    
    def applyDisaster(self):
        for survivor in self.survivors:
            survivor.setLifeStrengthAfterDisaster(self.disaster_center, self.disaster_dimensions)
    

    def create_map(self, noise = 0.325, seed = 1):

        # Parâmetros do mapa
        linhas, colunas = self.disaster_dimensions
        prob_obstaculo = noise

        # Definir a seed para reprodução dos resultados
        np.random.seed(seed)

        # Gerar o mapa inicial com obstáculos
        mapa = np.random.choice([0.0, 1.0], size=(linhas, colunas), p=[1 - prob_obstaculo, prob_obstaculo])

        # Assegurar que o ponto inicial e final estão livres
        mapa[0, 0] = 0
        mapa[-1, -1] = 0

        # Ajustar o mapa para garantir conectividade
        mapa = garantir_conectividade(mapa)

        for s in self.survivors:
            mapa[s.position] = 0.5

        # Visualizar o mapa final
        self.map = mapa
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