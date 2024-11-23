from passlib.context import CryptContext
import mysql.connector

# Configura Passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de la base de datos
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "casos_search",
    "port": 3306,
}

# Conexión a la base de datos
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Genera un nuevo hash para cdelgado
password = "cdelgado"  # Contraseña original para este usuario
hashed_password = pwd_context.hash(password)

# Actualiza la contraseña en la base de datos
cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password, "cdelgado"))

# Confirmar cambios
connection.commit()
cursor.close()
connection.close()

print("Hash actualizado correctamente para el usuario cdelgado.")
