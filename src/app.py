from flask import Flask, request, jsonify, render_template
import os
import numpy as np
from .buscar_casos import CasosSearchApp

# Configurar rutas base
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Rutas del archivo de datos, modelo y embeddings
data_path = os.path.join(BASE_DIR, 'casos_base_v4.csv')
embeddings_path = os.path.join(BASE_DIR, 'embeddings.npy')
model_path = os.path.join(BASE_DIR, 'models/sentence_transformer')

# Inicializar Flask
app = Flask(__name__)

# Inicializar CasosSearchApp
casos_app = CasosSearchApp(data_path, embeddings_path)

# Guardar el modelo si no existe
if not os.path.exists(model_path):
    print("Guardando modelo...")
    casos_app.search_engine.save_model(model_path)
    print(f"Modelo guardado en: {model_path}")

# Cargar el modelo guardado
print("Cargando modelo desde:", model_path)
casos_app.search_engine.load_model(model_path)
print("Modelo cargado exitosamente.")

# Generar o cargar embeddings
if os.path.exists(embeddings_path):
    casos_app.embeddings = np.load(embeddings_path)
    print("Embeddings cargados correctamente desde:", embeddings_path)
else:
    print("Generando embeddings...")
    casos_app.embeddings = casos_app.search_engine.encode_data(casos_app.df['Descripcion'].tolist())
    np.save(embeddings_path, casos_app.embeddings)
    print(f"Embeddings guardados en: {embeddings_path}")

# Rutas de la API
@app.route('/')
def index():
    return render_template('index.html')  # Renderizar una página principal si existe

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '')
    if not query:
        return jsonify({"error": "No se proporcionó una consulta"}), 400

    # Realizar la búsqueda
    similarities = casos_app.search_engine.find_similarities(query, casos_app.embeddings)
    casos_app.df['similarity'] = similarities
    df_sorted = casos_app.df.sort_values(by='similarity', ascending=False)

    # Seleccionar las columnas relevantes para la respuesta
    results = df_sorted[['Solucion Propuesta', 'Numero de Incidencia', 'Prioridad']].head(5).to_dict(orient='records')
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
