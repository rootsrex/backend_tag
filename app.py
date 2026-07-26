import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/cedula/<cedula>', methods=['GET'])
def consultar_cedula(cedula):
    try:
        url_externa = f"https://app3902.privynote.net/api/v1/civil/citizen/{cedula}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Referer": "https://consultasecuador.com/",
            "Origin": "https://consultasecuador.com",
            "Content-Type": "application/json"
        }
        respuesta = requests.get(url_externa, headers=headers, timeout=10)
        
        if respuesta.status_code != 200:
            return jsonify({
                "status": "exito", 
                "resultados": {
                    "nombre": "REGISTRO CIVIL TEMPORALMENTE OCUPADO", 
                    "cedula": cedula
                }
            })

        datos = respuesta.json()
        # Buscamos en todas las variantes posibles del JSON externo
        nombre = (
            datos.get("nombre") or 
            datos.get("nombreFinal") or 
            datos.get("nombres") or 
            datos.get("data", {}).get("nombre") or 
            datos.get("result", {}).get("nombre") or 
            "CIUDADANO REGISTRADO"
        )
        
        return jsonify({
            "status": "exito", 
            "resultados": {
                "nombre": str(nombre).upper(), 
                "cedula": cedula
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "exito", 
            "resultados": {
                "nombre": "CONSULTA ACTIVA", 
                "cedula": cedula
            }
        })

@app.route('/api/placa/<placa>', methods=['GET'])
def consultar_placa(placa):
    return jsonify({
        "status": "exito",
        "resultados": {
            "nombre": "MÓDULO EN ACTUALIZACIÓN",
            "value": placa.upper()
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)