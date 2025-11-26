import sqlite3
from flask_bcrypt import generate_password_hash

print("Conectando ao SQLite...")

# Conecta ao banco (cria o arquivo se não existir)
conn = sqlite3.connect("jogoteca.db")
cursor = conn.cursor()

# Criar tabelas
TABLES = {}
TABLES['Jogos'] = '''
    CREATE TABLE IF NOT EXISTS jogos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        console TEXT NOT NULL
    );
'''

TABLES['Usuarios'] = '''
    CREATE TABLE IF NOT EXISTS usuarios (
        nickname TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL
    );
'''

for nome, sql_code in TABLES.items():
    try:
        cursor.execute(sql_code)
        print(f"Tabela {nome} criada com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabela {nome}:", e)

# Inserir usuários (evita duplicados usando INSERT OR IGNORE)
usuarios = [
    ("Bruno Divino", "BD", generate_password_hash("alohomora").decode('utf-8')),
    ("Camila Ferreira", "Mila", generate_password_hash("paozinho").decode('utf-8')),
    ("Guilherme Louro", "Cake", generate_password_hash("python_eh_vida").decode('utf-8'))
]
cursor.executemany(
    'INSERT OR IGNORE INTO usuarios (nome, nickname, senha) VALUES (?, ?, ?)',
    usuarios
)

# Mostrar usuários
cursor.execute('SELECT * FROM usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])  # nickname

# Inserir jogos
jogos = [
    ('Tetris', 'Puzzle', 'Atari'),
    ('God of War', 'Hack n Slash', 'PS2'),
    ('Mortal Kombat', 'Luta', 'PS2'),
    ('Valorant', 'FPS', 'PC'),
    ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
    ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(
    'INSERT OR IGNORE INTO jogos (nome, categoria, console) VALUES (?, ?, ?)',
    jogos
)

# Mostrar jogos
cursor.execute('SELECT * FROM jogos')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])  # nome

# Salvar alterações e fechar
conn.commit()
conn.close()
print("Conexão encerrada.")
