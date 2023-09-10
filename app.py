from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            location TEXT,
            native_language TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pruebas (
            prueba_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            pregunta_a TEXT,
            pregunta_b TEXT,
            pregunta_c TEXT,
            pregunta_d TEXT,
            resultado INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registro_fallas (
            registro_id INTEGER PRIMARY KEY AUTOINCREMENT,
            prueba_id INTEGER,
            user_id INTEGER,
            status TEXT CHECK (status IN ('error')),
            answer TEXT CHECK (answer IN ('enviado', 'solucionado')),
            FOREIGN KEY (prueba_id) REFERENCES pruebas (prueba_id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS administrador (
            administrador_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            registro_id INTEGER,
            status TEXT CHECK (status IN ('error')),
            prueba_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (registro_id) REFERENCES registro_fallas (registro_id),   
            FOREIGN KEY (status) REFERENCES registro_fallas (status),     
            FOREIGN KEY (prueba_id) REFERENCES pruebas (prueba_id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

create_table()

@app.route('/')
def index():
    return "¡Bienvenido a la aplicación de usuarios!"

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        data = request.json

        if 'name' in data and 'email' in data and 'age' in data and 'location' in data and 'native_language' in data:
            name = data['name']
            email = data['email']
            age = data['age']
            location = data['location']
            native_language = data['native_language']

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, email, age, location, native_language)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, age, location, native_language))
            conn.commit()
            conn.close()
            return jsonify({"message": "Usuario agregado exitosamente"})
        else:
            return jsonify({"error": "Datos JSON incompletos o incorrectos"}), 400
        
@app.route('/user_test', methods=['POST'])
def user_test():
    if request.method == 'POST':
        data = request.json

        if 'user_id' in data and 'pregunta_a' in data and 'pregunta_b' in data and 'pregunta_c' in data and 'pregunta_d' in data and 'resultado' in data:
            user_id = data['user_id']
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
            user_exists = cursor.fetchone()
            conn.close()

            if user_exists:
                pregunta_a = data['pregunta_a']
                pregunta_b = data['pregunta_b']
                pregunta_c = data['pregunta_c']
                pregunta_d = data['pregunta_d']
                resultado = data['resultado']

                conn = sqlite3.connect(DATABASE)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO pruebas (user_id, pregunta_a, pregunta_b, pregunta_c, pregunta_d, resultado)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, pregunta_a, pregunta_b, pregunta_c, pregunta_d, resultado))
                conn.commit()
                conn.close()
                return jsonify({"message": "Prueba realizada correctamente"})
            else:
                return jsonify({"error": "No se encuentra un usuario con el user_id especificado"}), 400
        else:
            return jsonify({"error": "Datos JSON incompletos o incorrectos"}), 400

@app.route('/registro_fallas', methods=['POST'])
def registro_fallas():
    if request.method == 'POST':
        data = request.json

        if 'prueba_id' in data and 'user_id' in data and 'status' in data and 'answer' in data:
            prueba_id = data['prueba_id']
            user_id = data['user_id']
            status = data['status']
            answer = data['answer']

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Verificar si el usuario existe
            cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
            user_exists = cursor.fetchone()

            if user_exists:
                # Verificar si la prueba existe y está asociada al usuario
                cursor.execute('SELECT prueba_id FROM pruebas WHERE prueba_id = ? AND user_id = ?', (prueba_id, user_id))
                prueba_exists = cursor.fetchone()

                if prueba_exists:
                    cursor.execute('''
                        INSERT INTO registro_fallas (prueba_id, user_id, status, answer)
                        VALUES (?, ?, ?, ?)
                    ''', (prueba_id, user_id, status, answer))
                    conn.commit()
                    
                    registro_id = cursor.lastrowid
                    cursor.execute('''
                        INSERT INTO administrador (name, email, registro_id, status, prueba_id, user_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', ("administradorabc", "abcadmin@abc.com.co", registro_id, status, prueba_id, user_id))
                    conn.commit()

                    conn.close()

                    return jsonify({"message": "Registro de falla y administrador agregados exitosamente"})
                else:
                    conn.close()
                    return jsonify({"error": "La prueba no existe o no está asociada al usuario"}), 400
            else:
                conn.close()
                return jsonify({"error": "No se encuentra un usuario con el user_id especificado"}), 400
        else:
            return jsonify({"error": "Datos JSON incompletos o incorrectos"}), 400

@app.route('/administrador', methods=['GET'])
def get_administrator_records():
    data = request.json

    admin_id = data.get('administrador_id')
    admin_name = data.get('name')

    if admin_id is None or admin_name is None:
        return jsonify({"error": "Los parámetros 'administrador_id' y 'name' son obligatorios"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM administrador
        WHERE administrador_id = ? AND name = ?
    ''', (admin_id, admin_name))
    
    records = cursor.fetchall()
    conn.close()

    if records:
        return jsonify(records)
    else:
        return jsonify({"message": "No se encontraron registros asociados al administrador especificado"}), 404

# @app.route('/administrador', methods=['POST'])
# def administrador():
#     if request.method == 'POST':
#         data = request.json

#         if 'name' in data and 'email' in data and 'registro_id' in data and 'status' in data and 'prueba_id' in data and 'user_id' in data:
#             name = data['name']
#             email = data['email']
#             registro_id = data['registro_id']
#             status= data['status']
#             prueba_id = data['prueba_id']
#             user_id = data['user_id']

#             conn = sqlite3.connect(DATABASE)
#             cursor = conn.cursor()
#             cursor.execute('''
#                 INSERT INTO administrador (name, email, registro_id, status, prueba_id, user_id)
#                 VALUES (?, ?, ?, ?, ?, ?)
#             ''', (name, email, registro_id, status, prueba_id, user_id))
#             conn.commit()
#             conn.close()

#             return jsonify({"message": "Administrador agregado exitosamente"})
#         else:
#             return jsonify({"error": "Datos JSON incompletos o incorrectos"}), 400
        


