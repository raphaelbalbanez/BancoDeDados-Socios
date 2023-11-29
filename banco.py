import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `socios`;")

cursor.execute("CREATE DATABASE `socios`;")

cursor.execute("USE `socios`;")

# criando tabelas
TABLES = {}

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Raphael Barros", "LUX", "euvouparaalux"),
      ("Renato Santana", "Nagas", "renagol87"),
      ("Joao Augusto", "Burgo", "dogsburgo")
]
cursor.executemany(usuario_sql, usuarios)

# inserindo socios

cursor.executemany()

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
