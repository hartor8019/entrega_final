from fastapi import APIRouter, HTTPException, Form
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from .database import get_connection

router = APIRouter()

# Configuración de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar el usuario en la base de datos
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    db_user = cursor.fetchone()

    if not db_user or not pwd_context.verify(password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Crear una cookie de sesión
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="session_token", value="user_logged_in", httponly=True)
    return response
