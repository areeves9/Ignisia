from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.services.cantera_runner import run_simulation
from app.simulate import bp
from app.simulate.serializers import SimulationRequestSchema, SimulationResponseSchema

schema = SimulationRequestSchema()
response_schema = SimulationResponseSchema()


@bp.route("/")
class SimulateResource(MethodView):
    @bp.doc(
        security=[{"BearerAuth": []}],
        parameters=[
            {
                "in": "header",
                "name": "Authorization",
                "schema": {"type": "string"},
                "required": True,
                "description": "Bearer access token, e.g., 'Bearer <JWT>'",
            }
        ],
    )
    @jwt_required()
    @bp.arguments(SimulationRequestSchema)
    @bp.response(200, SimulationResponseSchema)
    def post(self, data):
        return run_simulation(**data)
