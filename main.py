import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def fetch_graph_data():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, new_id FROM nodes")
    nodes = cursor.fetchall()
    
    cursor.execute("SELECT source, target, weight FROM edges")
    edges = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return nodes, edges

def build_graph(nodes, edges):
    G = nx.DiGraph()  # DiGraph para um grafo direcionado
    
    for node in nodes:
        G.add_node(node[0], label=node[1])
    
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    
    return G

def draw_graph(G):
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=700, node_color='lightblue', font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.show()

def dijkstra_algorithm(G, start_node, end_node):
    return nx.dijkstra_path(G, start_node, end_node)

if __name__ == "__main__":
    nodes, edges = fetch_graph_data()
    G = build_graph(nodes, edges)
    
    draw_graph(G)
    
    start_node = int(input("Digite o ID do nó inicial: "))
    end_node = int(input("Digite o ID do nó final: "))
    
    shortest_path = dijkstra_algorithm(G, start_node, end_node)
    print(f"O caminho mais curto de {start_node} para {end_node} é: {shortest_path}")
