# autenticacion

# Api para autorizar
## usa token
## autentifica credencialess

gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app