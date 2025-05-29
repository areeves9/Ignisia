import cantera as ct
from marshmallow import Schema, ValidationError, fields, validate, validates
from marshmallow.validate import Range


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


class SimulationRequestSchema(Schema):
    fuel = fields.Str(
        required=True,
        metadata={
            "description": "Fuel species (e.g., 'CH4', 'H2')",
            "example": "CH4",
        },
        error_messages={"required": "Fuel is required."},
    )
    oxidizer = fields.Str(
        required=True,
        metadata={
            "description": "Oxidizer mixture (e.g., 'O2:1.0, N2:3.76')",
            "example": "O2",
        },
        error_messages={"required": "Oxidizer is required."},
    )
    phi = fields.Float(
        required=True,
        metadata={
            "description": "Equivalence ratio",
            "example": "1.0",
        },
        error_messages={"required": "Phi is required."},
    )
    pressure = fields.Float(
        required=True,
        metadata={
            "description": "Initial pressure in atm",
            "example": "1.0",
        },
        error_messages={"required": "Pressure is required."},
    )
    temperature = fields.Float(
        required=True,
        metadata={
            "description": "Initial temperature in Kelvin",
            "example": "300.0",
        },
        error_messages={"required": "Temperature is required."},
    )

    @validates("fuel")
    def validate_fuel(self, value, **kwargs):
        if value not in valid_fuels:
            raise ValidationError(
                f"Invalid fuel '{value}'. Must be one of: {', '.join(sorted(valid_fuels))}"
            )

    @validates("phi")
    def validate_phi(self, value, **kwargs):
        if not (0.1 <= value <= 5.0):
            raise ValidationError("Phi must be between 0.1 and 5.0")

    @validates("pressure")
    def validate_pressure(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("Pressure must be greater than 0.")

    @validates("temperature")
    def validate_temperature(self, value, **kwargs):
        if value < 0:
            raise ValidationError("Temperature must be 0 K or higher")


class SimulationResponseSchema(Schema):
    flame_temperature = fields.Float(
        metadata={
            "description": "Final adiabatic flame temperature in Kelvin",
            "example": 2200.5,
            "title": "Flame Temperature",
        }
    )
    species_profile = fields.Dict(
        keys=fields.Str(),
        values=fields.Float(),
        metadata={
            "description": "Mole fractions of major product species",
            "example": {"CO2": 0.12, "H2O": 0.21, "N2": 0.67},
            "title": "Species Profile",
        },
    )
