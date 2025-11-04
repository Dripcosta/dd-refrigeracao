import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Substitua 'admin' e '1234' pelo usuário e senha que quiser
c.execute("INSERT INTO admin (usuario, senha) VALUES (?, ?)", ('admin', '1234'))

conn.commit()
conn.close()

print("Administrador criado com sucesso!")