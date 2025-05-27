import cantera as ct
from marshmallow import Schema, ValidationError, fields, validate, validates
from marshmallow.validate import Range

from app.extensions import ma


def is_fuel_like(species):
    name = species.name.upper()
    elements = species.composition

    # Skip common oxidizers or products
    bad_names = {
        "O",
        "O2",
        "OH",
        "HO2",
        "H2O2",
        "H2O",
        "NO",
        "NO2",
        "N2O",
        "AR",
        "CO2",
        "N2",
    }
    if name in bad_names:
        return False

    # Heuristic: Must have carbon or multiple hydrogens
    has_C = "C" in elements
    has_enough_H = elements.get("H", 0) >= 2

    if not (has_C or has_enough_H):
        return False

    # Skip single-atom species
    if sum(elements.values()) <= 1:
        return False

    return True


gas = ct.Solution("gri30.yaml")
valid_fuels = sorted([s.name for s in gas.species() if is_fuel_like(s)])


class SimulationRequestSchema(ma.Schema):
    fuel = fields.Str(
        required=True,
        validate=validate.OneOf(
            valid_fuels, error=f"Must be one of: {', '.join(sorted(valid_fuels))}"
        ),
        error_messages={
            "required": "Fuel is required.",
            "validator_failed": "Must be one of: " + ", ".join(sorted(valid_fuels)),
        },
        metadata={"description": "Fuel species (e.g., 'CH4', 'H2')"},
    )
    oxidizer = fields.Str(
        required=True,
        metadata={"description": "Oxidizer mixture (e.g., 'O2:1.0, N2:3.76')"},
    )
    phi = fields.Float(
        required=True,
        validate=Range(min=0.1, max=5.0, error="Phi must be between 0.1 and 5.0"),
        metadata={"description": "Equivalence ratio"},
    )
    pressure = fields.Float(
        required=True,
        metadata={"description": "Initial pressure in atm"},
        validate=validate.Range(min=0.1, error="Pressure must be greater than 0"),
        error_messages={"required": "Pressure is required."},
    )
    temperature = fields.Float(
        required=True,
        metadata={"description": "Initial temperature in Kelvin"},
        validate=validate.Range(min=0, error="Temperature must be 0 K or higher"),
        error_messages={"required": "Temperature is required."},
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
