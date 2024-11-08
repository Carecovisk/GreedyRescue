from survivor import Survivor
from tools import a_star, garantir_conectividade
import random, numpy as np

class Enviroment:

    def __init__(self, survivors: list[Survivor], disaster_center: tuple, disaster_dimensions: tuple, robot_speed: float, st: float):
        self.survivors = survivors
        self.rescue_path: list[int] = []
        self.disaster_center = disaster_center
        self.disaster_dimensions = disaster_dimensions
        self.robot_speed = robot_speed
        self.st = st
        self.rescued_on_current_path = 0
    
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
    
    def evaluate_path(self, path: list[int] = None):
        path = path or self.rescue_path

        for i in path:
            self.survivors[i].resetLifeToAfterDisaster()

        last_id = path[0]
        for i, id in enumerate(path[1:]): # O caminho é uma sequencia de IDs representando os sobreviventes
            distance = a_star(self.map, self.survivors[last_id].position, self.survivors[id].position).__len__() - 1
            for j in path[i+1:]:
                self.survivors[j].setCurrentLife(self.robot_speed, distance, self.st)

            last_id = id
        self.rescued_on_current_path = self.surviorsRescued()
        return self.rescued_on_current_path
    
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
                

    def local_search(self, sequence_2opt_swap: float = 0.75, iterations: int = 10):
        # Operators
        def swap_operator(path: list[int]):
            x = random.choice(path)
            survivor_x_position = self.survivors[x].position
            closest_to_x = min(path, key=lambda s: self.survivors[s].distanceFrom(survivor_x_position))
            i, j = path.index(x), path.index(closest_to_x)
            path[i], path[j] = path[j], path[i]
            self.evaluate_path(path)
        
        def complementary_swap(path: list[int]):
            path_copy = path.copy()
            path_copy.sort(key=lambda x: self.survivors[x].life_strength)

            for i in range(len(path) // 2):
                with_less_life = path_copy[i]
                with_more_life = path_copy[- (i + 1)]
                k, l  = path.index(with_less_life), path.index(with_more_life)
                path[k], path[l] = path[l], path[k]
                
                before = self.rescued_on_current_path
                self.evaluate_path(path)
                if self.rescued_on_current_path > before:
                    break
        
        def swap_2_opt(path: list[int]):
            size = int(len(path) * sequence_2opt_swap)
            for i in range(len(path) - size + 1):
                failed = 0
                for j in range(i, i + size):
                    if not self.survivors[path[j]].isAlive:
                        failed += 1
                if failed > 2:
                    for j in range(i, (i + size) // 2):
                        path[j], path[(2 * i + size - 1) - j] = path[(2 * i + size - 1) - j], path[j]
                    break
            self.evaluate_path(path)

            

        weights = [1/3 for i in range(3)]
        choices = [swap_operator, complementary_swap, swap_2_opt]
        
        for i in range(iterations):
            operator = random.choices(population=choices, weights=weights, k=1)[0]

            rescued_before = self.rescued_on_current_path
            operator(self.rescue_path)
            if self.rescued_on_current_path > rescued_before:
                index = choices.index(operator)
                weights[index] += 0.05
        
        return self.rescued_on_current_path