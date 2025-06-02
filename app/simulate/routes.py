from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.extensions import limiter
from app.services.cantera_runner import run_simulation
from app.simulate import bp
from app.simulate.serializers import SimulationRequestSchema, SimulationResponseSchema


class SimulateResource(MethodView):
    @jwt_required()
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
    @bp.arguments(
        SimulationRequestSchema,
        example={
            "fuel": "CH4",
            "oxidizer": "O2",
            "phi": 1.0,
            "pressure": 1.0,
            "temperature": 298.15,
        },
    )
    @bp.response(
        200,
        SimulationResponseSchema,
        example={
            "flame_temperature": 2224.62,
            "species_profile": {
                "CO": 0.00895,
                "CO2": 0.0854,
                "H2": 0.00359,
                "H2O": 0.18349,
                "N2": 0.70861,
                "NO": 0.00188,
                "O2": 0.00461,
                "OH": 0.00286,
            },
        },
        description="""Successful simulation response with flame temperature and species profile.""",
    )
    @limiter.limit("5 per 1 seconds")
    def post(self, data):
        return run_simulation(**data)


bp.add_url_rule("", view_func=SimulateResource.as_view("/simulate"), methods=["POST"])
