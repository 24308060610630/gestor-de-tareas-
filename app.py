from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from bson import ObjectId

app = Flask(__name__)
bcrypt = Bcrypt(app)

MONGO_URI = "mongodb+srv://1234560:1234560@cluster0.1ic6x0h.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['sistema_usuarios']
usuarios_col = db['cuentas']
tareas_col = db['tareas']

@app.route('/')
def vista_login():
    return render_template('login.html')

@app.route('/todo')
def vista_tareas():
    return render_template('tareas.html')

# --- API (Lógica) ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if usuarios_col.find_one({"email": data.get('email')}):
        return jsonify({"message": "Usuario ya existe"}), 400
    pw_hash = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
    usuarios_col.insert_one({"email": data.get('email'), "password": pw_hash})
    return jsonify({"message": "Registrado correctamente"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = usuarios_col.find_one({"email": data.get('email')})
    if user and bcrypt.check_password_hash(user['password'], data.get('password')):
        return jsonify({"message": "Ok"}), 200
    return jsonify({"message": "Error de credenciales"}), 401

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        tasks = list(tareas_col.find())
        for t in tasks: t['_id'] = str(t['_id'])
        return jsonify(tasks)
    res = tareas_col.insert_one({"texto": request.json.get('texto')})
    return jsonify({"id": str(res.inserted_id)}), 201

@app.route('/api/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    tareas_col.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "eliminada"}), 200

if __name__ == '__main__':
    app.run(debug=True)