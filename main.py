from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

securityBearer = HTTPBearer()

@app.get('/')
def route(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    token = credentials.credentials

    if token == "1234":
        return {"auth": True}
    else:
        return {"auth": False}
