def obter_sequencias_continuas_de_tamanho(lista, tamanho):

    n_2opt_swap = 0.5
    size = int(len(lista) * n_2opt_swap)
    for i in range(len(lista) - size + 1):
        failed = 0
        for j in range(i, i + size):
            if not self.survivors[lista[j]].isAlive:
                failed += 1
        if failed > 2:
            for j in range(i, i + size):


l = [i for i in range(10)]

obter_sequencias_continuas_de_tamanho(l, int(len(l) * 0.75))
print(l)