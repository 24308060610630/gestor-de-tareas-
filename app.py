from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

MONGO_URI = "mongodb+srv://1234560:1234560@cluster0.1ic6x0h.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(MONGO_URI)
    db = client['sistema_usuarios'] 
    usuarios_col = db['cuentas']    
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error al conectar: {e}")

@app.route('/')
def registro():
    return render_template('registro.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    
    if usuarios_col.find_one({"email": email}):
        return jsonify({"message": "Este correo ya está registrado"}), 400

    
    password_encriptada = bcrypt.generate_password_hash(password).decode('utf-8')

    
    nuevo_usuario = {
        "email": email,
        "password": password_encriptada
    }
    
    try:
        usuarios_col.insert_one(nuevo_usuario) 
        return jsonify({"message": "Cuenta creada con éxito"}), 201
    except Exception as e:
        return jsonify({"message": "Error al guardar en la base de datos"}), 500

if __name__ == '__main__':
    app.run(debug=True)