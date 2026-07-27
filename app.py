from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# --- TU RUTA DE CÉDULAS / PLACAS EXISTENTE ---
# (Mantén aquí abajo el resto de tus rutas de cédula o placa si ya las tienes)

# --- NUEVA RUTA DE CÁMARAS CONECTADA AL EXCEL CORRECTO ---
@app.route('/api/camara/<path:codigo>', methods=['GET'])
def consultar_camara(codigo):
    try:
        # Leemos el archivo exacto que subiste a GitHub
        df = pd.read_excel('Listado_Camaras_Cuenca-1 (1).xlsx')
        
        busqueda_str = str(codigo).strip().lower()
        
        # Filtra de forma flexible cualquier coincidencia en el Excel
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
        
        # Intentamos extraer las columnas comunes (si tus columnas se llaman diferente, puedes cambiar 'nombre' o 'direccion' por el título exacto de tu Excel)
        nombre_camara = str(fila.iloc[0] if len(fila) > 0 else "CÁMARA")
        direccion = str(fila.iloc[1] if len(fila) > 1 else "DIRECCIÓN NO REGISTRADA")
        
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)