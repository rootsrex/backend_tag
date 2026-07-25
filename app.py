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
        payload = {"placa": placa.upper().strip()}
        respuesta = requests.post(url_externa, json=payload, headers=headers)

        datos = respuesta.json()
        print("RESPUESTA REAL DE LA API DE PLACAS:", datos) # Esto saldrá en tu terminal de VS Code

        # Buscamos en todas las posibles estructuras que pueda tener
        propietario = (
            datos.get("nombre") or 
            datos.get("propietario") or 
            datos.get("titular") or 
            datos.get("nombres") or 
            datos.get("nombrePropietario") or 
            datos.get("data", {}).get("nombre") or
            datos.get("resultado", {}).get("nombre") or
            str(datos) # Si no encuentra nada, nos mostrará el JSON crudo en la web para verlo
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