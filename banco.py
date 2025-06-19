import sqlite3

def conectar():
    return sqlite3.connect("estoque.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        quantidade INTEGER,
        preco REAL
    )
    """)

    # Tabela de movimentações
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        tipo TEXT,
        quantidade INTEGER,
        observacao TEXT,
        data TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    )
    """)

    # Tabela de usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        nivel TEXT
    )
    """)

    # Cria admin padrão, se não existir
    cursor.execute("SELECT * FROM usuarios WHERE login = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO usuarios (nome, login, senha, nivel) VALUES (?, ?, ?, ?)",
                       ("Administrador", "admin", "123", "Administrador"))

    conn.commit()
    conn.close()

# Executa ao rodar diretamente
if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas com sucesso.")
