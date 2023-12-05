from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

app = FastAPI()
security = HTTPBearer()

@app.get('/')
def read_root(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    if token == "1234":
        return {"auth": True}
    else:
        return {"auth": False}
