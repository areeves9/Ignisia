from flask import jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.services.cantera_runner import run_simulation
from app.simulate import bp
from app.simulate.serializers import SimulationRequestSchema, SimulationResponseSchema

schema = SimulationRequestSchema()
response_schema = SimulationResponseSchema()


@bp.route("/", methods=["POST"])
@jwt_required()
def simulate():
    data = request.get_json()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    result = run_simulation(**data)

    return response_schema.dump(result), 200
