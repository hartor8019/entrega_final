import numpy as np
import os
import pandas as pd
from .data_loader import DataLoader
from .semantica import SemanticSearch

class CasosSearchApp:
    def __init__(self, data_file_path: str, embeddings_path: str):
        self.data_loader = DataLoader('D:/Documents/casos search/src/casos_base_v3.csv')
        self.search_engine = SemanticSearch()
        self.df = self.data_loader.load_data()
        
        # Validar y limpiar la columna 'Descripcion'
        if 'Descripcion' not in self.df.columns:
            raise KeyError("La columna 'Descripcion' no está presente en el archivo de datos.")
        
        # Reemplazar valores no válidos
        self.df['Descripcion'] = self.df['Descripcion'].fillna('').astype(str)

        # Cargar o crear embeddings
        if os.path.exists(embeddings_path):
            self.embeddings = np.load(embeddings_path)
            print("Embeddings cargados correctamente.")
        else:
            print("Generando embeddings...")
            self.embeddings = self.search_engine.encode_data(self.df['Descripcion'].tolist())
            np.save(embeddings_path, self.embeddings)
            print(f"Embeddings guardados en: {embeddings_path}")

        # Depuración: Verificar datos después de la limpieza
        print("Datos procesados en 'Descripcion':", self.df['Descripcion'].head())

        # Generar embeddings para las descripciones
        self.embeddings = self.search_engine.encode_data(self.df['Descripcion'].tolist())

    def run(self):
        while True:
            query = input('Ingresa el término de búsqueda (o escribe "salir" para terminar): ')
            if query.lower() == 'salir':
                print("Saliendo del programa. ¡Hasta luego!")
                break

            similarities = self.search_engine.find_similarities(query, self.embeddings)
            self.df['similarity'] = similarities
            df_sorted = self.df.sort_values(by='similarity', ascending=False)
            self._display_results(df_sorted)

    def _display_results(self, df_sorted):
        print("Resultados similares:")
        print(df_sorted[['Solucion Propuesta', 'Numero de Incidencia', 'Prioridad']].head())

if __name__ == '__main__':
    app = CasosSearchApp('D:/Documents/casos search/src/casos_base_v3.csv')
    app.run()