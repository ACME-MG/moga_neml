"""
 Title:         Calibration of an EVP model with large strain
 Description:   Interface for calibrating NEML models
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import sys; sys.path += [".."]
from moga_neml.interface import Interface
from moga_neml.drivers.large_strain import ls_tensile_driver

def main():
    """
    Main function
    """
    # Define the interface and model
    itf = Interface("evp", input_path="data", output_here=True, verbose=False)
    itf.define_model("evp")

    # Add short-term creep data
    # itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
    # itf.remove_damage()
    # itf.add_error("area", "time", "strain")

    # itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
    # itf.remove_damage()
    # itf.add_error("area", "time", "strain")

    # Add long-term creep data
    # itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
    # itf.remove_damage(0.1, 0.7)
    # itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
    # itf.remove_damage(0.1, 0.7)

    # Add tensile data
    itf.read_data("tensile/inl/AirBase_800_D7.csv")
    # itf.remove_manual("strain", 0.3)
    # itf.add_error("area", "strain", "stress")
    # itf.add_error("end", "strain")
    # itf.add_error("end", "stress")
    # itf.add_error("yield_point", yield_stress=291)
    
    # Apply driver
    itf.set_custom_driver(
        driver_type = ls_tensile_driver,
        strain_rate = itf.get_data("strain_rate"),
        temperature = itf.get_data("temperature"),
        max_strain  = 1.0
    )

    # Plot simulations
    params_list = [17.217, 179.74, 0.61754, 4.4166, 1783.5]
    itf.plot_simulation(params_list)

# Calls the main function
if __name__ == "__main__":
    main()
