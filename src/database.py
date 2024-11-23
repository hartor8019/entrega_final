import os
import mysql.connector
from mysql.connector import pooling

# Configuración de conexión a MySQL usando variables de entorno
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),          # Dirección del servidor (por defecto: localhost)
    "user": os.getenv("DB_USER", "root"),              # Usuario de MySQL (por defecto: root)
    "password": os.getenv("DB_PASSWORD", "root"),          # Contraseña de MySQL
    "database": os.getenv("DB_NAME", "casos_search"),  # Base de datos por defecto
    "port": os.getenv("DB_PORT", 3306)                # Puerto (por defecto: 3306)
}

# Inicialización del pool de conexiones a la base de datos
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=int(os.getenv("DB_POOL_SIZE", 5)),  # Tamaño del pool configurable
        **db_config
    )
    print("Conexión a la base de datos configurada correctamente.")
except mysql.connector.Error as err:
    print(f"Error al conectar con la base de datos: {err}")
    connection_pool = None

def get_connection():
    """
    Obtiene una conexión del pool de conexiones.
    Lanza una excepción si el pool no está disponible.
    """
    if connection_pool is None:
        raise Exception("No se pudo inicializar el pool de conexiones a la base de datos.")
    try:
        connection = connection_pool.get_connection()
        return connection
    except mysql.connector.Error as err:
        print(f"Error al obtener una conexión de la base de datos: {err}")
        raise
