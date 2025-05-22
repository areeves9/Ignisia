from flask import jsonify, request
from flask_jwt_extended import jwt_required

# from app.simulate.serializers import SimulationRequestSchema
from app.services.cantera_runner import run_simulation

# from marshmallow import ValidationError
from app.simulate import bp

# schema = SimulationRequestSchema()


@bp.route("/", methods=["POST"])
@jwt_required()
def simulate():
    data = request.get_json()
    # try:
    #     data = schema.load(request.get_json())
    # except ValidationError as err:
    #     return jsonify({"errors": err.messages}), 400

    result = run_simulation(
        fuel=data["fuel"],
        oxidizer=data["oxidizer"],
        phi=data["phi"],
        pressure=data["pressure"],
        temperature=data["temperature"],
    )

    return jsonify(result)
