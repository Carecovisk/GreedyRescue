import heapq

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

# Exemplo:
if __name__ == '__main__':
    mapa = [
        [0.5, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0.5]
    ]
    inicio = (0, 0)
    destino = (4, 4)

    caminho = a_star(mapa, inicio, destino)
    print("Caminho:", caminho)