from buscar_casos import CasosSearchApp
import json

# Inicializar el buscador de casos
casos_app = CasosSearchApp('src/casos_base_v3.csv')

def run(data):
    """
    Recibe datos en formato JSON con el campo "query".
    """
    try:
        # Convertir los datos de entrada en un diccionario
        data_dict = json.loads(data)
        query = data_dict.get("query", "")

        # Verificar si la consulta está presente
        if not query:
            return {"error": "No se proporcionó una consulta"}

        # Buscar similitudes
        similarities = casos_app.search_engine.find_similarities(query, casos_app.embeddings)
        casos_app.df['similarity'] = similarities
        df_sorted = casos_app.df.sort_values(by='similarity', ascending=False)

        # Retornar los primeros 5 resultados
        results = df_sorted[['Solucion Propuesta', 'Numero de Incidencia', 'Prioridad']].head(5).to_dict(orient='records')
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}
