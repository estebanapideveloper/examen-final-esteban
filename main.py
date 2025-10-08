from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = "estudiantes.json"

def leer_datos():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route("/estudiantes", methods=["GET"])
def listar_estudiantes():
    estudiantes = leer_datos()
    return jsonify(estudiantes)

@app.route("/estudiantes/<int:id>", methods=["GET"])
def obtener_estudiante(id):
    estudiantes = leer_datos()
    estudiante = next((e for e in estudiantes if e["id"] == id), None)
    if estudiante:
        return jsonify(estudiante)
    return jsonify({"mensaje": "Estudiante no encontrado"}), 404

@app.route("/estudiantes", methods=["POST"])
def crear_estudiante():
    estudiantes = leer_datos()
    nuevo = request.get_json()
    nuevo["id"] = max([e["id"] for e in estudiantes], default=0) + 1
    estudiantes.append(nuevo)
    guardar_datos(estudiantes)
    return jsonify({"mensaje": "Estudiante agregado correctamente", "estudiante": nuevo}), 201

@app.route("/estudiantes/<int:id>", methods=["PUT"])
def actualizar_estudiante(id):
    estudiantes = leer_datos()
    actualizado = request.get_json()
    for e in estudiantes:
        if e["id"] == id:
            e.update(actualizado)
            guardar_datos(estudiantes)
            return jsonify({"mensaje": "Estudiante actualizado", "estudiante": e})
    return jsonify({"mensaje": "Estudiante no encontrado"}), 404

@app.route("/estudiantes/<int:id>", methods=["DELETE"])
def eliminar_estudiante(id):
    estudiantes = leer_datos()
    nuevos_estudiantes = [e for e in estudiantes if e["id"] != id]
    if len(nuevos_estudiantes) == len(estudiantes):
        return jsonify({"mensaje": "Estudiante no encontrado"}), 404
    guardar_datos(nuevos_estudiantes)
    return jsonify({"mensaje": "Estudiante eliminado correctamente"})

if __name__ == "__main__":
    app.run(debug=True)
