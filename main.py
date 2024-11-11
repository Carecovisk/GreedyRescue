from survivor import Survivor
from enviroment import Enviroment
from tools import read_positions
import matplotlib.pyplot as plt, math, random

ST = 5 # Tempo gasto pelo robo para salvar uma pessoa
ROBOT_SPEED = 1 # Velocidade do robo

INITIAL_LIFE = 100 # Nivel de vida antes do desastre
DISASTER_CENTER = (14, 11) # Centro do desastre
LIFE_THRESHOLD = 2 # Vida minima para alguem ser resgatado
DISASTER_DIMENSIONS = (100, 100) # Tamanho da área considerada

LIMIT = 50

# survivors_position = read_positions('r101.txt', head=20)

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

def print_survivors():
    for s in enviroment.survivors:
        print(s)

enviroment.create_map(seed=0)
enviroment.applyDisaster()
enviroment.initialize_rescue_path()
result = enviroment.rescued_on_current_path

best_path = enviroment.rescue_path.copy()
rescued_on_best_path = enviroment.rescued_on_current_path

i = 0
while True:

    if enviroment.rescued_on_current_path == survivors.__len__():
        break

    if i >= LIMIT:
        enviroment.rescue_path = best_path
        break

    rescued_before = enviroment.rescued_on_current_path
    path_before = enviroment.rescue_path.copy()

    enviroment.destroy_and_recreate()
    
    rescued_after = enviroment.local_search()

    if enviroment.rescued_on_current_path > rescued_on_best_path:
        rescued_on_best_path = enviroment.rescued_on_current_path
        best_path = enviroment.rescue_path.copy()

    if rescued_before > rescued_after: # Se a solução piorou
        rescued_difference =  rescued_before - rescued_after
        temperature = rescued_after / 10 * len(survivors)
        probability_of_acceptance = math.e ** (- rescued_difference / temperature)

        if not random.random() < probability_of_acceptance: # Se rejeitar a solução local
            enviroment.rescued_on_current_path = rescued_before
            enviroment.rescue_path = path_before
    i += 1

travel = enviroment.evaluate_path(return_path=True)[1]

y, x = zip(*travel)

print("Survivors:")
print_survivors()
print("Saved:", enviroment.rescued_on_current_path)
print("Rescue order", enviroment.rescue_path)

plt.imshow(enviroment.map, cmap="Greys", origin="upper")

plt.plot(x, y, marker='o', color='r', linestyle='-', linewidth=1, markersize=3)

start_y, start_x = travel[0]
end_y, end_x = travel[-1]

for i, (y, x) in enumerate([enviroment.survivors[x].position for x in enviroment.rescue_path][1:-1]):
    plt.text(x, y, str(i + 1), fontsize=10)

plt.text(start_x, start_y, "Start", fontsize=16, color="gray")
plt.text(end_x, end_y, "End", fontsize=16, color= "gray")
plt.title("Mapa")
plt.show()