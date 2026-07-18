from flask import Flask, jsonify, request
from flask_cors import CORS

from cedula_service import buscar_por_cedula, buscar_por_nombre

app = Flask(__name__)
CORS(app, origins="*")


@app.get("/api/cedula/<cedula>")
def consultar_cedula(cedula):
    resultados = buscar_por_cedula(cedula)
    return jsonify({"resultados": resultados})


@app.get("/api/nombre")
def consultar_nombre():
    nombre = request.args.get("q", "")
    if not nombre:
        return jsonify({"error": "Falta el parámetro 'q'"}), 400
    resultados = buscar_por_nombre(nombre)
    return jsonify({"resultados": resultados})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
