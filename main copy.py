from survivor import Survivor
from enviroment import Enviroment
import matplotlib.pyplot as plt

ST = 5 # Tempo gasto pelo robo para salvar uma pessoa
ROBOT_SPEED = 0.8 # Velocidade do robo

INITIAL_LIFE = 100 # Nivel de vida antes do desastre
DISASTER_CENTER = (14, 11) # Centro do desastre
LIFE_THRESHOLD = 2 # Vida minima para alguem ser resgatado
DISASTER_DIMENSIONS = (86, 86) # Tamanho da área considerada

survivors_position = [
    (28, 55),
    (85, 35),
    (32, 30),
    (25, 85),
    (58, 75),
    (38,  5),
    (53, 30),
    (66, 55),
    (45, 70),
    (10, 35),
]
survivors = [Survivor(i, position, INITIAL_LIFE, LIFE_THRESHOLD) for i, position in enumerate(survivors_position)]

enviroment = Enviroment(survivors, DISASTER_CENTER, DISASTER_DIMENSIONS, ROBOT_SPEED, ST)

enviroment.create_map()
enviroment.applyDisaster()
enviroment.initialize_rescue_path()
result = enviroment.destroy_and_recreate()

print(result)
print(enviroment.rescue_path)

for s in enviroment.survivors:
    print(s)

plt.imshow(enviroment.map, cmap="Greys", origin="upper")
plt.colorbar(label="0 = Livre, 1 = Obstáculo")
plt.title("Mapa com Obstáculos e Áreas Conectadas")
plt.xlabel("Colunas")
plt.ylabel("Linhas")
plt.show()