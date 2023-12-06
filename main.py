from fastapi import FastAPI, Depends, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import sqlite3

app = FastAPI()

security_basic = HTTPBasic()
security_bearer = HTTPBearer()

# Función para abrir y cerrar la conexión en cada solicitud
def get_db():
    db = sqlite3.connect("sql/usuario.db")
    db.row_factory = sqlite3.Row
    yield db
    db.close()

# Middleware para manejar la conexión a la base de datos
@app.middleware("http")
async def db_middleware(request, call_next, db: sqlite3.Connection = Depends(get_db)):
    request.state.db = db
    response = await call_next(request)
    return response

# Endpoint para la autenticación básica y validar token Bearer
@app.get("/")
def index(credentials: HTTPBasicCredentials = Depends(security_basic), db: sqlite3.Connection = Depends(get_db)):
    email = credentials.username
    cursor = db.cursor()
    
    # Lógica para la autenticación básica
    query_basic = "SELECT * FROM usuario WHERE email = ?"
    cursor.execute(query_basic, (email,))
    user = cursor.fetchone()
    
    if user and credentials.password == user["password1"]:
        return {"auth": True, "token": user["token"]}
    
    # Credenciales no válidas
    return JSONResponse(content={"auth": False, "detail": "Invalid credentials"}, status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/token")
def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security_bearer), db: sqlite3.Connection = Depends(get_db)):
    token = credentials.credentials
    cursor = db.cursor()

    query = "SELECT * FROM usuario WHERE token = ?"
    cursor.execute(query, (token,))
    user = cursor.fetchone()

    if user:
        return {"message": "Token válido y autorizado"}
    else:
        return {"error": "Token inválido"}, status.HTTP_401_UNAUTHORIZED
