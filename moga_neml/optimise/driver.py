"""
 Title:         Driver
 Description:   For running the NEML drivers
 Author:        Janzen Choi

"""

# Libraries
from neml import drivers
from moga_neml.helper.experiment import NEML_FIELD_CONVERSION
from moga_neml.helper.general import BlockPrint
from moga_neml.optimise.curve import Curve
from moga_neml.models.__model__ import __Model__

# General Driver Constants
TIME_HOLD    = 11500.0 * 3600.0
NUM_STEPS    = 1000
REL_TOL      = 1e-6
ABS_TOL      = 1e-10
MAX_STRAIN   = 1.0
VERBOSE      = False
NUM_STEPS_UP = 50
DAMAGE_TOL   = 0.95 # 0.95
STRESS_RATE  = 0.0001
CYCLIC_RATIO = -1

# Driver class
class Driver:
    
    def __init__(self, curve:Curve, model:__Model__) -> None:
        """
        Initialises the driver class
        
        Parameters:
        * `curve`:      The curve the driver is being used on
        * `model`:      The model to be run
        """
        self.curve      = curve
        self.exp_data   = curve.get_exp_data()
        self.type       = self.exp_data["type"]
        self.model      = model
        self.conv_dict  = NEML_FIELD_CONVERSION[self.type]
    
    def run(self) -> dict:
        """
        Runs the driver based on the experimental curve type;
        returns the results
        """

        # Get the results
        try:
            with BlockPrint():
                results = self.run_selected()
        except:
            return
        
        # Convert results and return
        converted_results = {}
        for field in list(self.conv_dict.keys()):
            if field in results.keys():
                converted_results[self.conv_dict[field]] = results[field]
        return converted_results
    
    def run_selected(self) -> dict:
        """
        Runs the driver depending on the data type;
        returns the results
        """

        # Runs custom driver if it is defined
        custom_driver, custom_driver_kwargs = self.curve.get_custom_driver()
        if custom_driver != None:
            custom_driver = getattr(drivers, custom_driver)
            results = custom_driver(self.model, **custom_driver_kwargs)
            return results

        # Runs driver based on data type
        if self.type == "creep":
            return self.run_creep()
        elif self.type == "tensile":
            return self.run_tensile()
        elif self.type == "cyclic":
            return self.run_cyclic()
        raise ValueError(f"The data type '{self.type}' is not supported; use the 'custom_driver' function to define a custom driver")

    def run_creep(self) -> dict:
        """
        Runs the creep driver;
        returns the results
        """
        results = drivers.creep(self.model, self.exp_data["stress"], STRESS_RATE, TIME_HOLD,
                                T=self.exp_data["temperature"], verbose=VERBOSE, check_dmg=True,
                                dtol=DAMAGE_TOL, nsteps_up=NUM_STEPS_UP, nsteps=NUM_STEPS, logspace=False)
        return results

    def run_tensile(self) -> dict:
        """
        Runs the tensile driver;
        returns the results
        """
        results = drivers.uniaxial_test(self.model, erate=self.exp_data["strain_rate"], T=self.exp_data["temperature"],
                                        emax=MAX_STRAIN, check_dmg=True, dtol=DAMAGE_TOL, nsteps=NUM_STEPS,
                                        verbose=VERBOSE, rtol=REL_TOL, atol=ABS_TOL)
        return results
    
    def run_cyclic(self) -> dict:
        """
        Runs the cyclic driver;
        returns the results
        """
        num_cycles = int(self.exp_data["num_cycles"])
        results = drivers.strain_cyclic(self.model, T=self.exp_data["temperature"], emax=self.exp_data["max_strain"],
                                        erate=self.exp_data["strain_rate"], verbose=VERBOSE, R=CYCLIC_RATIO,
                                        ncycles=num_cycles, nsteps=NUM_STEPS)
        return results
