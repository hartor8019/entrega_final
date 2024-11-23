from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from .auth import router as auth_router
import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()  # Carga las variables del archivo .env

# Configuración de rutas
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models/sentence_transformer")
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "embeddings.npy")
DATA_PATH = os.path.join(BASE_DIR, "casos_base_v3.csv")

# Cargar el modelo y embeddings
print("Cargando modelo...")
model = SentenceTransformer(MODEL_PATH)
print("Modelo cargado correctamente.")

print("Cargando embeddings...")
if not os.path.exists(EMBEDDINGS_PATH):
    raise FileNotFoundError(f"No se encontró el archivo de embeddings en {EMBEDDINGS_PATH}")
embeddings = np.load(EMBEDDINGS_PATH)
print("Embeddings cargados correctamente.")

# Cargar el DataFrame
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo de datos en {DATA_PATH}")
    df = pd.DataFrame()  # DataFrame vacío para evitar errores

# Crear la app
app = FastAPI()

# Incluir el enrutador de autenticación
app.include_router(auth_router)

# Condicionar el montaje de archivos estáticos
if os.getenv("ENV") != "test" and os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
else:
    print("Advertencia: El directorio 'static' no existe o estamos en pruebas. Omitiendo montaje.")

# Modelo de entrada para la API
class QueryInput(BaseModel):
    query: str

# Middleware para autenticación
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Si el usuario intenta acceder a "/" sin autenticarse
    if request.url.path == "/" and "session_token" not in request.cookies:
        return RedirectResponse(url="/login", status_code=307)
    return await call_next(request)

# Ruta principal (protegida, requiere autenticación)
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join(BASE_DIR, "templates/index.html"), "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# Ruta de login (sirve el formulario de login)
@app.get("/login", response_class=HTMLResponse)
async def login_page():
    with open(os.path.join(BASE_DIR, "templates/login.html"), "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# Ruta de logout (cerrar sesión)
@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="session_token")
    return response

# Endpoint de búsqueda (protegido)
@app.post("/search")
async def search_cases(input_data: QueryInput):
    query = input_data.query
    if not query:
        return {"error": "La consulta no puede estar vacía"}

    # Generar embeddings para la consulta
    query_embedding = model.encode(query)

    # Calcular similitudes
    similarities = util.cos_sim(query_embedding, embeddings).flatten()
    df["similarity"] = similarities

    # Ordenar resultados
    df_sorted = df.sort_values(by="similarity", ascending=False)
    results = df_sorted[["Descripcion", "Solucion Propuesta", "Numero de Incidencia"]].head(5).to_dict(orient="records")

    return {"results": results}
