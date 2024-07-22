import psycopg2
import networkx as nx
import matplotlib.pyplot as plt

def fetch_graph_data():
    # Conecta ao banco de dados PostgreSQL
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    
    cursor = conn.cursor()
    
    # Executa a consulta SQL para buscar todos os nós
    cursor.execute("SELECT id, name, new_id FROM nodes")
    nodes = cursor.fetchall()  # Obtém todos os nós
    
    # Executa a consulta SQL para buscar todas as arestas
    cursor.execute("SELECT source, target, weight FROM edges")
    edges = cursor.fetchall()  # Obtém todas as arestas
    
    # Fecha o cursor e a conexão com o banco de dados
    cursor.close()
    conn.close()
    
    return nodes, edges  # Retorna os nós e arestas

def build_graph(nodes, edges):
    G = nx.DiGraph()  # Cria um grafo direcionado (DiGraph)
    
    # Adiciona os nós ao grafo
    for node in nodes:
        G.add_node(node[0], label=node[1])  # Adiciona o nó com o id e label
    
    # Adiciona as arestas ao grafo
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])  # Adiciona a aresta com source, target e weight
    
    return G  # Retorna o grafo construído

# def draw_graph(G):
#     pos = nx.spring_layout(G)  # Calcula a posição dos nós usando o layout spring
#     labels = nx.get_node_attributes(G, 'label')  # Obtém os rótulos dos nós
    
#     plt.figure(figsize=(12, 8))  # Define o tamanho da figura
#     nx.draw(G, pos, with_labels=True, labels=labels, node_size=700, node_color='lightblue', font_size=10, font_weight='bold')  # Desenha os nós e arestas
#     edge_labels = nx.get_edge_attributes(G, 'weight')  # Obtém os rótulos das arestas
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  # Desenha os rótulos das arestas
    
#     plt.show()  # Exibe o gráfico

def dijkstra_algorithm(G, start_node, end_node):
    try:
        return nx.dijkstra_path(G, start_node, end_node)  # Calcula o caminho mais curto usando o algoritmo de Dijkstra
    except nx.NetworkXNoPath:
        return None  # Retorna None se não houver caminho

if __name__ == "__main__":
    nodes, edges = fetch_graph_data()  # Busca os dados do grafo
    G = build_graph(nodes, edges)  # Constrói o grafo
    
    draw_graph(G)  # Desenha o grafo
    
    # Solicita ao usuário os nós inicial e final
    start_node = int(input("Digite o ID do nó inicial: "))
    end_node = int(input("Digite o ID do nó final: "))
    
    # Calcula e imprime o caminho mais curto entre os nós fornecidos
    shortest_path = dijkstra_algorithm(G, start_node, end_node)
    if shortest_path is not None:
        print(f"O caminho mais curto de {start_node} para {end_node} é: {shortest_path}")
    else:
        print(f"Não existe caminho entre {start_node} e {end_node}")
