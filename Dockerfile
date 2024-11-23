# Usa una imagen ligera de Python
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

# Establece el directorio de trabajo
WORKDIR /app

# Establece el directorio en el PYTHONPATH
ENV PYTHONPATH=/app/src

# Instala las dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip a la última versión
RUN pip install --upgrade pip

# Copia los archivos de dependencias y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --timeout 300

# Copia el resto de los archivos del proyecto al contenedor
COPY src/ ./src/

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
