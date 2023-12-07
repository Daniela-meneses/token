from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import HTTPBasic
from fastapi.responses import JSONResponse
import sqlite3
import hashlib
import secrets
from datetime import datetime

app = FastAPI()

security_basic = HTTPBasic()
security_bearer = HTTPBearer()

def get_db():
    db = sqlite3.connect("sql/usuario.db")
    db.row_factory = sqlite3.Row
    yield db
    db.close()

@app.middleware("http")
async def db_middleware(request, call_next, db: sqlite3.Connection = Depends(get_db)):
    request.state.db = db
    response = await call_next(request)
    return response 

@app.post("/registro")
async def registro(db: sqlite3.Connection = Depends(get_db), datos_usuario: dict = Depends()):
    cursor = db.cursor()

    query = 'INSERT INTO usuario (email, password1, token, timestamp1, estado) VALUES (?, ?, ?, ?, ?)'
    hashed_password = hashlib.md5(datos_usuario.get("password").encode()).hexdigest()
    valores = (datos_usuario.get("email"), hashed_password, secrets.token_urlsafe(12), str(datetime.now()), "activo")
    
    cursor.execute(query, valores)
    db.commit()

    return {"message": "Registro exitoso"}

@app.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(), db: sqlite3.Connection = Depends(get_db)):
    email = credentials.username
    password_hash = hashlib.md5(credentials.password.encode()).hexdigest()

    cursor = db.cursor()
    query = "SELECT * FROM usuario WHERE email = ? AND password1 = ?"
    cursor.execute(query, (email, password_hash))
    user = cursor.fetchone()

    if user:
        new_token = secrets.token_urlsafe(12)
        timestamp = str(datetime.now())

        update_query = "UPDATE usuario SET token = ?, timestamp1 = ? WHERE email = ?"
        cursor.execute(update_query, (new_token, timestamp, email))
        db.commit()

        return {"auth": True, "token": new_token}
    else:
        {"auth": False, "detail": "Invalid credentials"}

@app.get("/")
def index(credentials: HTTPBasicCredentials = Depends(security_basic), db: sqlite3.Connection = Depends(get_db)):
    email = credentials.username
    cursor = db.cursor()
    
    query_basic = "SELECT * FROM usuario WHERE email = ?"
    cursor.execute(query_basic, (email,))
    user = cursor.fetchone()
    
    if user and hashlib.md5(credentials.password.encode()).hexdigest() == user["password1"]:
        new_token = secrets.token_urlsafe(12)
        
        timestamp = str(datetime.now())
        update_query = "UPDATE usuario SET token = ?, timestamp1 = ? WHERE email = ?"
        cursor.execute(update_query, (new_token, timestamp, email))
        db.commit()

        return {"auth": True, "token": new_token}
    
    return JSONResponse(content={"auth": False, "detail": "Invalid credentials"})

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
        return {"error": "Token inválido"}