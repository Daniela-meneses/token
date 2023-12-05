from flask import Flask, jsonify, request
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tuClaveSecreta'  # Clave secreta para firmar el token (cámbiala por una clave segura)

@app.route('/generateToken', methods=['GET'])
def generate_token():
    usuario = request.args.get('usuario')
    contraseña = request.args.get('contraseña')

    # Aquí deberías realizar la lógica de autenticación
    # En este ejemplo, se asume que la autenticación es exitosa siempre
    # Simplemente se generará un token JWT con la información del usuario

    # Simulación de datos de usuario (reemplaza esta lógica con la autenticación real)
    if usuario == 'usuario_ejemplo' and contraseña == 'contraseña_ejemplo':
        token = jwt.encode({'usuario': usuario, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return jsonify({'mensaje': 'Error de autenticación'}), 401

if __name__ == '__main__':
    app.run(debug=True)
