from survivor import Survivor
from tools.a_star import a_star
import pandas as pd, random
import numpy as np
from scipy.ndimage import label

class Enviroment:

    def __init__(self, survivors: list[Survivor], disaster_center: tuple, disaster_dimensions: tuple, robot_speed: float, st: float):
        self.survivors = survivors
        self.rescue_path: list[int] = []
        self.disaster_center = disaster_center
        self.disaster_dimensions = disaster_dimensions
        self.robot_speed = robot_speed
        self.st = st
    
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
        linhas, colunas = self.disaster_dimensions
        prob_obstaculo = noise
        np.random.seed(seed)
        mapa = np.random.choice([0.0, 1.0], size=(linhas, colunas), p=[1 - prob_obstaculo, prob_obstaculo])

        mapa = garantir_conectividade(mapa)

        for s in self.survivors:
            mapa[s.position] = 0.5

        self.map = mapa

    # TODO:melhorar esse código
    def initialize_rescue_path(self):
        remaing_survivors = self.survivors.copy()
        with_lowest_life = min(remaing_survivors, key=lambda s: s.life_strength)
        self.rescue_path.append(remaing_survivors.pop(with_lowest_life.id).id)

        result = 0
        while remaing_survivors:
            current_position = self.survivors[self.rescue_path[-1]].position
            closest = min(remaing_survivors, key=lambda rs: rs.distanceFrom(current_position))
            remaing_survivors.remove(closest)

            possible_paths = [self.rescue_path[:i] + [closest.id] + self.rescue_path[i:] for i in range(len(self.rescue_path) + 1)]

            max = 0
            best_path = None
            for path in possible_paths:
                result = self.evaluate_path(path)
                if result > max:
                    max = result
                    best_path = path
            
            self.rescue_path = best_path
            # print(rp)
        return result
    
    def evaluate_path(self, path = None):
        path = path or self.rescue_path

        for i in path:
            self.survivors[i].resetLifeToAfterDisaster()

        last_id = path[0]
        for i, id in enumerate(path[1:]): # O caminho é uma sequencia de IDs representando os sobreviventes
            distance = a_star(self.map, self.survivors[last_id].position, self.survivors[id].position).__len__() - 1
            for j in path[i+1:]:
                self.survivors[j].setCurrentLife(self.robot_speed, distance, self.st)

            last_id = id
        return self.surviorsRescued()
    
    def destroy_and_recreate(self, n_of_points: float = 0.5):
        size = len(self.rescue_path)
        list_a = random.sample(self.rescue_path, int(size * n_of_points))
        list_b = [x for x in self.rescue_path if x not in list_a]

        result = 0
        for point_a in list_a:
            best_path = None
            possible_paths = [list_b[:i] + [point_a] + list_b[i:] for i in range(len(list_b) + 1)]
            max = 0
            for path in possible_paths:
                result = self.evaluate_path(path)
                if result > max:
                    max = result
                    best_path = path
            list_b = best_path
        
        self.rescue_path = list_b
        return result
                


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