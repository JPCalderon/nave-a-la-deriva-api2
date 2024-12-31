from flask import Flask, request, jsonify

app = Flask(__name__)

# Curva de saturación (ejemplo con valores ficticios)
def calculate_volumes(pressure):
    # Aquí defines la lógica de cálculo basada en la presión
    # Estos son ejemplos arbitrarios; puedes ajustar según tus datos:
    specific_volume_liquid = 0.0035 + (pressure * 0.0001)
    specific_volume_vapor = 0.0035 + (pressure * 0.0002)
    return specific_volume_liquid, specific_volume_vapor

# Ruta principal para el diagrama de cambio de fase
@app.route("/phase-change-diagram", methods=["GET"])
def phase_change_diagram():
    try:
        # Obtener el parámetro 'pressure' de la solicitud
        pressure = float(request.args.get("pressure", 0))
        specific_volume_liquid, specific_volume_vapor = calculate_volumes(pressure)
        
        # Responder con los valores calculados
        return jsonify({
            "specific_volume_liquid": round(specific_volume_liquid, 4),
            "specific_volume_vapor": round(specific_volume_vapor, 4)
        }), 200
    except ValueError:
        return jsonify({"error": "Invalid pressure value. Must be a number."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
