from flask import Flask, request, jsonify

app = Flask(__name__)

# Curva de saturación (ejemplo con valores ficticios)
def calculate_volumes(pressure, points_liquid = [(0.00105, 0.05), (0.0035, 10)], points_vapor = [(0.0035, 10), (30, 0.05)]):
    """
    Calcula los volúmenes específicos de líquido y vapor en función de la presión.
    
    Parámetros:
        pressure (float): Presión en MPa.
        points_liquid (list): Lista de puntos [(v1, P1), (v2, P2)] para la curva de líquido.
        points_vapor (list): Lista de puntos [(v1, P1), (v2, P2)] para la curva de vapor.

    Retorna:
        (specific_volume_liquid, specific_volume_vapor)
    """

    def calculate_volume(p1, p2, pressure):
        """Calcula v = (P - b) / m para los puntos p1 y p2."""
        v1, p1_y = p1
        v2, p2_y = p2
        m = (p2_y - p1_y) / (v2 - v1)  # Pendiente
        b = p1_y - m * v1              # Intersección
        return (pressure - b) / m

    # Determinar los volúmenes específicos
    specific_volume_liquid = calculate_volume(points_liquid[0], points_liquid[1], pressure)
    specific_volume_vapor = calculate_volume(points_vapor[0], points_vapor[1], pressure)

    return round(specific_volume_liquid,4), round(specific_volume_vapor,4)

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
