import networkx as nx
import matplotlib.pyplot as plt

def nw(seq1: str, seq2: str, match: int=1, indel: int=0):
    # Funcao que cria o grid
    def create_grid(seq1: str, seq2: str, match: int=1, indel: int=0):
        G = nx.DiGraph()
        k = len(seq1)+1
        u = len(seq2)+1
        for i in range(k):
            for j in range(u):
                G.add_node((i, j))
                if i>0 and j>0:
                    G.add_edge((i-1, j-1), (i, j), weight=match if seq1[i-1] == seq2[j-1] else indel)
                if i > 0:
                    G.add_edge((i-1, j), (i, j), weight=indel)
                if j > 0:
                    G.add_edge((i, j-1), (i, j), weight=indel)
        return G
    # Funcao que calcula o caminho de valor maximo
    def max_path(G:nx.DiGraph, start:tuple, end:tuple):
        max_path = nx.shortest_path(G, source=start, target=end, weight=lambda u, v, d: -d['weight'])
        max_score = sum(G[u][v]['weight'] for u, v in zip(max_path[:-1], max_path[1:]))
        return max_path, max_score
    # Funcao que desenha o caminho maximo entre o inicio e o fim
    def draw_max_path(G:nx.DiGraph, path:list, seq1:str, seq2:str):
        pos = {(i, j): (j, -i) for i, j in G.nodes()}
        nx.draw(G, pos, with_labels=True, node_size=400, node_color="lightblue", font_size=8)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2)
        plt.xticks(range(len(seq2)+1), [""] + list(seq2), fontsize=8)
        plt.yticks(range(-(len(seq1)+1), 0), [""] + list(seq1), fontsize=8)
        plt.title("Caminho de Peso Maximo no Grafo")
        plt.show()
    # Funcao que gera o melhor alinhamento
    def alignment(path):
        aligned_seq1 = []
        aligned_seq2 = []
        for (i1, j1), (i2, j2) in zip(path[:-1], path[1:]):
            if i2 > i1 and j2 > j1:
                aligned_seq1.append(seq1[i1])
                aligned_seq2.append(seq2[j1])
            elif i2 > i1:
                aligned_seq1.append(seq1[i1])
                aligned_seq2.append('-')
            elif j2 > j1:
                aligned_seq1.append('-')
                aligned_seq2.append(seq2[j1])
        return ''.join(aligned_seq1), ''.join(aligned_seq2)

    # Criar o grafo do grid
    G = create_grid(seq1, seq2, match, indel)
    # Definir inicio e fim
    start_node = (0, 0)
    end_node = (len(seq1), len(seq2))
    # Encontrar caminho maximo
    path, score = max_path(G, start_node, end_node)
    # Desenhar o grafo com o caminho maximo
    draw_max_path(G, path, seq1, seq2)
    # Alinhamento
    aligment_seq1, aligment_seq2 = alignment(path)
    # Retorno o caminho e o maximo numero de casamentos (matches)
    return path, score, (aligment_seq1, aligment_seq2)

# Exemplo
seq1 = "AGTCCATC"
seq2 = "GGCATTA"
path, score, alignment = nw(seq1, seq2, match=1, indel=0)
print("Caminho de peso maximo/melhor alinhamento:", path)
print("Pontuacao Maxima/numero de casamentos(caso base):", score)
print("Alinhamento: ")
print("Seq1:", alignment[0])
print("Seq2:", alignment[1])
