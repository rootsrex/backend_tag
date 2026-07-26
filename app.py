@app.route('/api/placa/<placa>', methods=['GET'])
def consultar_placa(placa):
    try:
        url_externa = f"https://app3902.privynote.net/api/v1/ vehicular/plate/{placa.upper()}" # O la ruta de placas que usabas
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://consultasecuador.com/",
            "Origin": "https://consultasecuador.com"
        }
        respuesta = requests.get(url_externa, headers=headers, timeout=10)
        
        if respuesta.status_code != 200:
            return jsonify({
                "status": "exito",
                "resultados": {
                    "nombre": "VEHÍCULO NO ENCONTRADO",
                    "value": placa.upper()
                }
            })

        datos = respuesta.json()
        propietario = datos.get("propietario") or datos.get("nombre") or datos.get("nombres") or "REGISTRO VEHICULAR DISPONIBLE"
        
        return jsonify({
            "status": "exito",
            "resultados": {
                "nombre": str(propietario).upper(),
                "value": placa.upper()
            }
        })
    except Exception as e:
        return jsonify({
            "status": "exito",
            "resultados": {
                "nombre": "CONSULTA DE PLACA ACTIVA",
                "value": placa.upper()
            }
        })