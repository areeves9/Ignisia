import cantera as ct


def run_simulation(fuel, oxidizer, phi, pressure, temperature):
    """
    Run an adiabatic, constant-pressure equilibrium combustion simulation.

    Args:
        fuel (str): Fuel species string (e.g., "CH4")
        oxidizer (str): Oxidizer species string (e.g., "O2:1.0, N2:3.76")
        phi (float): Equivalence ratio
        pressure (float): Initial pressure in atm
        temperature (float): Initial temperature in Kelvin

    Returns:
        dict: Dictionary with flame temperature and species mole fractions.
    """
    # Load chemical mechanism (GRI-Mech 3.0)
    gas = ct.Solution("gri30.yaml")

    # Set the gas state: fuel/oxidizer mix at specified T and P
    gas.set_equivalence_ratio(phi, fuel=fuel, oxidizer=oxidizer)
    gas.TP = temperature, pressure * ct.one_atm

    # Equilibrate at constant enthalpy and pressure (adiabatic flame)
    gas.equilibrate("HP")

    # Get adiabatic flame temperature
    flame_temp = gas.T

    # Filter significant species (mole fraction > 0.001)
    species_profile = {
        sp: round(gas[sp].X[0], 5) for sp in gas.species_names if gas[sp].X[0] > 0.001
    }

    return {
        "flame_temperature": round(flame_temp, 2),
        "species_profile": species_profile,
    }
