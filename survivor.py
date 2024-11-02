import math

# Classe para representar um sobrevivente
class Survivor:

    def __init__(self, id: int, position: tuple, initial_life_strength: float) -> None:
        self.id = id
        self.position = position
        self._initial_life_strength = initial_life_strength
        self.isAlive = True
    
    def distanceFrom(self, other_position: tuple):
        return math.dist(self.position, other_position)
    
    def setLifeStrengthAfterDisaster(self, disaster_center: tuple, disaster_dimension: tuple):
        distance_from_disaster = self.distanceFrom(disaster_center)
        l = math.sqrt(disaster_dimension[0] ** 2 + disaster_dimension[1] ** 2) # A diagonal é a maior distancia
        self.life_strength = self._initial_life_strength * min(distance_from_disaster/l, 1)
    
    def setCurrentLife(self, robot_speed: float, last_distance_traveled: float, saving_time: float):
        time_spent = last_distance_traveled / robot_speed + saving_time
        self.life_strength *= math.e ** (-0.0037 * time_spent)
    
    def __str__(self) -> str:
        return f"(ID: {self.id}, Position: {self.position}, Life: {self.life_strength})"