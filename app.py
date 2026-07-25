import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from cedula_service import buscar_por_cedula, buscar_por_nombre

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/cedula/<cedula>', methods=['GET'])
def consultar_cedula(cedula):
    try:
        resultados = buscar_por_cedula(cedula)
        
        if not resultados:
            return jsonify({
                "status": "exito",
                "resultados": {
                    "nombre": "DATOS EN CONSTRUCCIÓN",
                    "cedula": cedula
                }
            })
            
        primer_resultado = resultados[0] if isinstance(resultados, list) else resultados
        nombre = primer_resultado.get("nombre", "DATOS EN CONSTRUCCIÓN")

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
        # Reutilizamos la misma lógica segura apuntando al servicio interno
        resultados = buscar_por_cedula(placa.upper()) # O la función de vehículos que tengas en cedula_service
        
        if not resultados:
            return jsonify({
                "status": "exito",
                "resultados": {
                    "nombre": "DATOS EN CONSTRUCCIÓN",
                    "value": placa
                }
            })
            
        primer_resultado = resultados[0] if isinstance(resultados, list) else resultados
        propietario = primer_resultado.get("nombre", "DATOS EN CONSTRUCCIÓN")

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