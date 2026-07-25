from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

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
        
        # Extraemos de forma segura el nombre del propietario en cualquiera de sus variantes
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

import os

if __name__ == '__main__':
<<<<<<< HEAD
    # Railway asigna el puerto mediante la variable de entorno PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
=======
    app.run(host='0.0.0.0', port=5000)
>>>>>>> 0704bbc (Actualizar app.py con extraccion correcta de placa)
