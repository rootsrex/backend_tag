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
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "es-ES,es;q=0.9",
            "Referer": "https://consultasecuador.com/",
            "Origin": "https://consultasecuador.com",
            "Content-Type": "application/json"
        }

        respuesta = requests.get(url_externa, headers=headers)

        if respuesta.status_code != 200:
            return jsonify({
                "status": "error",
                "mensaje": f"La página externa bloqueó la petición (Código {respuesta.status_code})"
            }), respuesta.status_code

        datos = respuesta.json()
        
        nombre = (
            datos.get("nombre") or 
            datos.get("nombreFinal") or 
            datos.get("nombres") or 
            "DATOS EN CONSTRUCCIÓN"
        )

        return jsonify({
            "status": "exito",
            "resultados": {
                "nombre": nombre,
                "cedula": cedula
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "exito",
            "resultados": {
                "nombre": "DATOS EN CONSTRUCCIÓN",
                "cedula": cedula
            }
        })

@app.route('/api/placa/<placa>', methods=['GET'])
def consultar_placa(placa):
    try:
        url_externa = "https://app3902.privynote.net/api/v1/transit/vehicle-owner"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "es-ES,es;q=0.9",
            "Referer": "https://consultasecuador.com/",
            "Origin": "https://consultasecuador.com",
            "Content-Type": "application/json"
        }

        payload = {
            "placa": placa
        }

        respuesta = requests.post(url_externa, json=payload, headers=headers)

        if respuesta.status_code != 200:
            return jsonify({
                "status": "error",
                "mensaje": f"La página externa bloqueó la petición (Código {respuesta.status_code})"
            }), respuesta.status_code

        datos = respuesta.json()
        
        propietario = (
            datos.get("nombre") or 
            datos.get("propietario") or 
            datos.get("titular") or 
            datos.get("nombres") or 
            "DATOS EN CONSTRUCCIÓN"
        )

        return jsonify({
            "status": "exito",
            "resultados": {
                "nombre": propietario,
                "value": placa
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "exito",
            "resultados": {
                "nombre": "DATOS EN CONSTRUCCIÓN",
                "value": placa
            }
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    