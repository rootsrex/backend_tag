@app.route('/api/camara/<codigo>', methods=['GET'])
def consultar_camara(codigo):
    try:
        df = pd.read_excel('camaras.xlsx')
        busqueda = df[df['codigo'].astype(str).str.upper() == codigo.upper()]
        
        if busqueda.empty:
            return jsonify({
                "status": "exito",
                "resultados": [{
                    "nombre": "CÁMARA NO ENCONTRADA",
                    "direccion": "Verifique el código en el sistema"
                }]
            })
            
        nombre_camara = str(busqueda.iloc[0].get('nombre', f"CÁMARA {codigo.upper()}"))
        direccion = str(busqueda.iloc[0].get('direccion', 'DIRECCIÓN NO REGISTRADA'))
        
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
                "nombre": "ERROR AL LEER EL EXCEL",
                "direccion": str(e)
            }]
        })