from survivor import Survivor
from enviroment import Enviroment
import matplotlib.pyplot as plt, math, random

ST = 5 # Tempo gasto pelo robo para salvar uma pessoa
ROBOT_SPEED = 0.5 # Velocidade do robo

INITIAL_LIFE = 100 # Nivel de vida antes do desastre
DISASTER_CENTER = (14, 11) # Centro do desastre
LIFE_THRESHOLD = 2 # Vida minima para alguem ser resgatado
DISASTER_DIMENSIONS = (100, 100) # Tamanho da área considerada

LIMIT = 50

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
result = enviroment.rescued_on_current_path

print(result)
print(enviroment.rescue_path)
print('-------')

i = 0
while True:

    if enviroment.rescued_on_current_path == survivors.__len__() or i >= LIMIT:
        print('cabouu', i)
        break

    rescued_before = enviroment.rescued_on_current_path
    path_before = enviroment.rescue_path.copy()

    enviroment.destroy_and_recreate()
    
    rescued_after = enviroment.local_search()

    if rescued_before > rescued_after:
        rescued_difference =  rescued_before - rescued_after
        temperature = rescued_after / 10 * len(survivors)
        probability_of_acceptance = math.e ** (- rescued_difference / temperature)

        if not random.random() < probability_of_acceptance:
            enviroment.rescued_on_current_path = rescued_before
            enviroment.rescue_path = path_before
    
    i += 1

enviroment.evaluate_path()
for s in enviroment.survivors:
    print(s)

print("Saved now:", enviroment.rescued_on_current_path)

plt.imshow(enviroment.map, cmap="Greys", origin="upper")
plt.colorbar(label="0 = Livre, 1 = Obstáculo")
plt.title("Mapa com Obstáculos e Áreas Conectadas")
plt.xlabel("Colunas")
plt.ylabel("Linhas")
# plt.show()