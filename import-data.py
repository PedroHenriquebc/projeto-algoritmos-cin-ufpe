import psycopg2

def create_tables():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    
    cursor = conn.cursor()
    
    # Criar as tabelas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nodes (
        id BIGSERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        new_id BIGINT
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS edges (
        id SERIAL PRIMARY KEY,
        source INT REFERENCES nodes(id),
        target INT REFERENCES nodes(id),
        weight FLOAT NOT NULL DEFAULT 1.0
    );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def import_data(nodes_file, edges_file):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    
    cursor = conn.cursor()
    
    # Importar nós
    with open(nodes_file, 'r') as f:
        for line in f:
            row = line.strip().split(',')
            if len(row) != 3:
                print(f"Linha inválida em {nodes_file}: {row}")
                continue
            try:
                node_id = int(row[0])
                name = row[1]
                new_id = int(row[2])  # Mudança para BIGINT
                cursor.execute("INSERT INTO nodes (id, name, new_id) VALUES (%s, %s, %s)", (new_id, name, node_id))
            except ValueError:
                print(f"Erro ao converter valores em {nodes_file}: {row}")
    
    # Importar arestas com peso padrão 1.0
    with open(edges_file, 'r') as f:
        for line in f:
            row = line.strip().split(',')
            if len(row) != 2:
                print(f"Linha inválida em {edges_file}: {row}")
                continue
            try:
                source = int(row[0])
                target = int(row[1])
                
                # Verificar se source e target existem na tabela nodes
                cursor.execute("SELECT COUNT(*) FROM nodes WHERE id = %s OR id = %s", (source, target))
                count = cursor.fetchone()[0]
                
                if count == 2:  # Ambos source e target existem na tabela nodes
                    cursor.execute("INSERT INTO edges (source, target, weight) VALUES (%s, %s, %s)", (source, target, 1.0))
                    print(f"Inserido na edges: source={source}, target={target}")
                else:
                    print(f"Nó(s) não encontrado(s) em nodes: source={source}, target={target}")
                    
            except ValueError:
                print(f"Erro ao converter valores em {edges_file}: {row}")
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
    import_data('fb-pages-food.nodes', 'fb-pages-food.edges')
    print("Dados importados com sucesso.")
