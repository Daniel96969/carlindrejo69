# mock_server.py
# Servidor Flask de prueba para login
# Instalar Flask: pip install flask

from flask import Flask, request, jsonify

app = Flask(__name__)

# Usuarios y contraseñas de ejemplo (solo para pruebas locales)
USERS = {
    "admin": "holamundo",
    "usuario": "secreto123"
}

@app.route("/login", methods=["POST"])
def login():
    data = {}

    if request.is_json:
        data = request.get_json()
    else:
        data['username'] = request.form.get('username')
        data['password'] = request.form.get('password')

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Faltan username/password"}), 400

    expected = USERS.get(username)
    if expected is None:
        return jsonify({"success": False, "message": "Usuario no existe"}), 401

    if password == expected:
        return jsonify({"success": True, "message": "Login exitoso"}), 200
    else:
        return jsonify({"success": False, "message": "Credenciales inválidas"}), 401


if __name__ == "__main__":
    # Ejecuta con: python mock_server.py
    app.run(host="127.0.0.1", port=5000, debug=True)
   

   # client_tester.py
# Cliente que lee contraseñas.txt y prueba contra el servidor local
# Instalar requests: pip install requests

import requests
import time
import sys
import os

CONTRA_FILE = "contraseñas.txt"
LOGIN_URL = "http://127.0.0.1:5000/login"
USERNAME = "admin"  # Usuario a probar
DELAY = 0.5  # segundos entre pruebas

def leer_contrasenas(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No existe el archivo '{path}'")
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return [l for l in lines if l]

def probar_contrasenas(username, contrasenas, url):
    resultados = []
    for pwd in contrasenas:
        payload = {"username": username, "password": pwd}
        try:
            resp = requests.post(url, json=payload, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Falló la conexión: {e}")
            resultados.append((pwd, "error", str(e)))
            continue

        try:
            data = resp.json()
        except ValueError:
            data = {"success": False, "message": f"Respuesta inválida ({resp.status_code})"}

        success = data.get("success", False)
        message = data.get("message", "")
        status = "ok" if success else "fail"

        print(f"Probando '{pwd}': {status} ({message})")
        resultados.append((pwd, status, message))

        if success:
            print(f">>> ¡Contraseña encontrada: '{pwd}' para usuario '{username}'")
            break

        time.sleep(DELAY)
    return resultados

def main():
    try:
        contrasenas = leer_contrasenas(CONTRA_FILE)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    if not contrasenas:
        print("El archivo de contraseñas está vacío.")
        sys.exit(0)

    print(f"Probando {len(contrasenas)} contraseñas para usuario '{USERNAME}'...")
    resultados = probar_contrasenas(USERNAME, contrasenas, LOGIN_URL)

    out_file = "resultado_pruebas.txt"
    try:
        with open(out_file, "w", encoding="utf-8") as f:
            for pwd, status, message in resultados:
                f.write(f"{pwd},{status},{message}\n")
        print(f"Resumen guardado en '{out_file}'")
    except Exception as e:
        print("Error guardando el resultado:", e)

if __name__ == "__main__":
    main()
