import sqlite3

def criar_banco():
    conn = sqlite3.connect('mercado_financeiro.db')
    create_table_sql = """CREATE TABLE IF NOT EXISTS preco_acoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        ticker VARCHAR(10) NOT NULL,
        Price DECIMAL(10, 2),
        SMA_20 DECIMAL(10, 2),
        RSI_14 DECIMAL(10, 2),
        Signal VARCHAR(10)
    )"""
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()
    print("Banco de dados criado com sucesso!")
if __name__ == "__main__":
    criar_banco()