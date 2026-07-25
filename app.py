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
        
        # Enviar la placa en el cuerpo (JSON) como exige el servicio externo
        payload = {"placa": placa.upper().strip()}
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
            datos.get("nombrePropietario") or 
            "DATOS EN CONSTRUCCIÓN"
        )
        
        return jsonify({
            "status": "exito",
            "resultados": {
                "nombre": propietario,
                "value": placa.upper()
            }
        })
    except Exception as e:
        return jsonify({
            "status": "exito",
            "resultados": {
                "nombre": "DATOS EN CONSTRUCCIÓN",
                "value": placa.upper()
            }
        })