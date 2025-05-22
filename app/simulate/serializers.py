from marshmallow import fields, validate

from app.extensions import ma


class SimulationRequestSchema(ma.Schema):
    fuel = fields.Str(
        required=True, metadata={"description": "Fuel species (e.g., 'CH4', 'H2')"}
    )
    oxidizer = fields.Str(
        required=True,
        metadata={"description": "Oxidizer mixture (e.g., 'O2:1.0, N2:3.76')"},
    )
    phi = fields.Float(
        required=True,
        validate=validate.Range(min=0.1, max=5.0),
        metadata={"description": "Equivalence ratio between 0.1 and 5.0"},
    )
    pressure = fields.Float(
        required=True, metadata={"description": "Initial pressure in atm"}
    )
    temperature = fields.Float(
        required=True, metadata={"description": "Initial temperature in Kelvin"}
    )


class SimulationResponseSchema(ma.Schema):
    flame_temperature = fields.Float(
        metadata={"description": "Final adiabatic flame temperature in Kelvin"}
    )
    species_profile = fields.Dict(
        keys=fields.Str(),
        values=fields.Float(),
        metadata={"description": "Mole fractions of major product species"},
    )
