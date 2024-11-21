import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def smith_waterman(seq1, seq2):
    # Inicializando a matriz de pontuacao e o grafo
    n, m = len(seq1), len(seq2)
    score_matrix = np.zeros((n + 1, m + 1), dtype=int)
    G = nx.DiGraph()
    # Variaveis para acompanhar o maior score e sua posicao
    max_score = 0
    max_pos = (0, 0)
    # Preenchendo a matriz de pontuacao e construindo o grafo
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Calculando os scores possiveis
            match_score = score_matrix[i - 1, j - 1] + (MATCH if seq1[i - 1] == seq2[j - 1] else MISMATCH)
            delete_score = score_matrix[i - 1, j] + GAP 
            insert_score = score_matrix[i, j - 1] + GAP 
            score_matrix[i, j] = max(0, match_score, delete_score, insert_score)
            # Atualizando o maior score e sua posicao
            if score_matrix[i, j] > max_score:
                max_score = score_matrix[i, j]
                max_pos = (i, j)
            # Adicionando as arestas ao grafo
            if score_matrix[i, j] == match_score:
                G.add_edge((i - 1, j - 1), (i, j), weight=match_score)
            if score_matrix[i, j] == delete_score:
                G.add_edge((i - 1, j), (i, j), weight=delete_score)
            if score_matrix[i, j] == insert_score:
                G.add_edge((i, j - 1), (i, j), weight=insert_score)

    # Realizando o traceback a partir do maior score
    aligned_seq1, aligned_seq2 = "", ""
    i, j = max_pos
    while score_matrix[i, j] > 0:
        if (i - 1, j - 1) in G.pred[(i, j)]:
            aligned_seq1 = seq1[i - 1] + aligned_seq1
            aligned_seq2 = seq2[j - 1] + aligned_seq2
            i, j = i - 1, j - 1
        elif (i - 1, j) in G.pred[(i, j)]:
            aligned_seq1 = seq1[i - 1] + aligned_seq1
            aligned_seq2 = "-" + aligned_seq2
            i, j = i - 1, j
        elif (i, j - 1) in G.pred[(i, j)]:
            aligned_seq1 = "-" + aligned_seq1
            aligned_seq2 = seq2[j - 1] + aligned_seq2
            i, j = i, j - 1
    return aligned_seq1, aligned_seq2, max_score, G

# Exemplo de uso
seq1 = "ACGT"
seq2 = "AGCT"
MATCH = 2
MISMATCH = -1
GAP = -1
aligned_seq1, aligned_seq2, max_score, graph = smith_waterman(seq1, seq2)
print(f"Alinhamento:\n{aligned_seq1}\n{aligned_seq2}")
print(f"Pontuacao maxima: {max_score}")
pos = {node: (node[1], -node[0]) for node in graph.nodes()}  # Organizando os nos em uma grade
nx.draw(graph, pos, with_labels=True, node_size=500, font_size=8, font_color="white", edge_color="gray")
plt.title("Grafo do Algoritmo de Smith-Waterman")
plt.show()
