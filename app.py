from flask import Flask, request, jsonify
import pandas as pd

# Asegúrate de que app esté definida así
app = Flask(__name__)

@app.route('/api/camara/<path:codigo>', methods=['GET'])
def consultar_camara(codigo):
    try:
        df = pd.read_excel('camaras.xlsx')
        busqueda_str = str(codigo).strip().lower()
        
        df_filtrado = df[
            df.astype(str).apply(lambda row: row.str.lower().str.contains(busqueda_str, na=False).any(), axis=1)
        ]
        
        if df_filtrado.empty:
            return jsonify({
                "status": "exito",
                "resultados": [{
                    "nombre": "CÁMARA / DIRECCIÓN NO ENCONTRADA",
                    "direccion": "Verifique los datos e intente nuevamente"
                }]
            })
            
        fila = df_filtrado.iloc[0]
        nombre_camara = str(fila.get('nombre', fila.get('codigo', 'CÁMARA')))
        direccion = str(fila.get('direccion', 'DIRECCIÓN NO REGISTRADA'))
        
        return jsonify({
            "status": "exito",
            "resultados": [{
                "nombre": nombre_camara.upper(),
                "direccion": direccion.upper()
            }]
        })
    except Exception as e:
        return jsonify({
            "status": "exito",
            "resultados": [{
                "nombre": "ERROR EN CONSULTA",
                "direccion": str(e)
            }]
        })