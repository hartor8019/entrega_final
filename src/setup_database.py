import mysql.connector

# Configuración de la conexión a MySQL
config = {
    "host": "localhost",         # Cambia a la IP de tu servidor MySQL si es remoto
    "user": "root",              # Usuario MySQL
    "password": "",  # Contraseña del usuario
}

# Crear conexión
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Crear la base de datos
cursor.execute("CREATE DATABASE IF NOT EXISTS casos_search;")

# Seleccionar la base de datos
cursor.execute("USE casos_search;")

# Crear la tabla de usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);
""")

print("Base de datos y tabla creadas correctamente.")

# Cerrar la conexión
cursor.close()
conn.close()
