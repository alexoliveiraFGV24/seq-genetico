import networkx as nx
import matplotlib.pyplot as plt

def ford_fulkerson(graph: nx.DiGraph, source: str, sink: str):
    def find_augmenting_path(residual_graph, source, sink, path):
        if source == sink:
            return path
        for neighbor in residual_graph.neighbors(source):
            capacity = residual_graph[source][neighbor]['capacity']
            if capacity > 0 and neighbor not in [node for node, _ in path]:
                result = find_augmenting_path(residual_graph, neighbor, sink, path + [(neighbor, capacity)])
                if result is not None:
                    return result
        return None

    """ criando o gráfico residual para o início"""
    residual_graph = graph.copy()
    for u, v, data in residual_graph.edges(data=True):
        data['flow'] = 0 #começaremos com o fluxo em 0

    max_flow = 0

    while True:
        """ iremos, com isso, encontrar o caminho aumentante"""
        path = find_augmenting_path(residual_graph, source, sink, [(source, float('Inf'))])
        if not path:
            break

        """ determinando a capacidade mínima do caminho aumentante"""
        flow = min(cap for _, cap in path)

        """ atualizar o grafo residual """
        for i in range(len(path) - 1):
            u, _ = path[i]
            v, _ = path[i + 1]
            residual_graph[u][v]['capacity'] -= flow
            residual_graph[u][v]['flow'] += flow
            if residual_graph.has_edge(v, u):
                residual_graph[v][u]['capacity'] += flow
            else:
                residual_graph.add_edge(v, u, capacity=flow, flow=0)

        max_flow += flow

    return max_flow, residual_graph

""" tentarei desenvolver uma linha de código para esboçar o grafo em questão, com o intuito de facilitar a visualização """
def draw_graph(graph: nx.DiGraph):
    pos = nx.spring_layout(graph)  
    edge_labels = { 
        (u, v): f"{data['flow']}/{data['capacity']}" 
        for u, v, data in graph.edges(data=True) 
    }
    nx.draw(graph, pos, with_labels=True, node_size=350, node_color="lightblue")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=12)
    nx.draw_networkx_edges(graph, pos, edge_color="black", arrowstyle="->", arrowsize=15)
    plt.title("Fluxo em Rede")
    plt.show()

""" elaborando um caso genérico """
G = nx.DiGraph()
G.add_edge('F', 'A', capacity=10)
G.add_edge('F', 'B', capacity=5)
G.add_edge('A', 'B', capacity=15)
G.add_edge('B', 'S', capacity=10)
G.add_edge('A', 'S', capacity=10)
fonte = 'F'
sumidouro = 'S'
max_flow, residual_graph = ford_fulkerson(G, fonte, sumidouro)
print(f"Fluxo Máximo: {max_flow}")
print(G.edges())
draw_graph(residual_graph)
