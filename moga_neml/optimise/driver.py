"""
 Title:         Driver
 Description:   For running the NEML drivers
 Author:        Janzen Choi

"""

# Libraries
from neml import drivers
from moga_neml.maths.experiment import NEML_FIELD_CONVERSION
from moga_neml.maths.general import BlockPrint

# General Driver Constants
MAX_STRAIN   = 1.0
TIME_HOLD    = 11500.0 * 3600.0
NUM_STEPS_UP = 50
NUM_STEPS    = 1001
REL_TOL      = 1.0E-6 # -6
ABS_TOL      = 1.0E-10 # -10
DAMAGE_TOL   = 0.95
VERBOSE      = False

# Specific Driver Constants
STRESS_RATE  = 0.0001
CYCLIC_RATIO = -1

# Driver class
class Driver:
    
    # Constructor
    def __init__(self, exp_data:dict, model):
        self.exp_data        = exp_data
        self.type            = self.exp_data["type"]
        self.model           = model
        self.conversion_dict = NEML_FIELD_CONVERSION[self.type]
    
    # Runs the driver based on the experimental curve type
    def run(self) -> dict:
        
        # Get the results
        try:
            with BlockPrint():
                results = self.run_selected()
        except: # (MaximumIterations, MaximumSubdivisions):
            return
        
        # Convert results and return
        converted_results = {}
        for field in list(self.conversion_dict.keys()):
            if field in results.keys():
                converted_results[self.conversion_dict[field]] = results[field]
        return converted_results
    
    # Gets the results based on the type
    def run_selected(self):
        if self.type == "creep":
            return self.run_creep()
        elif self.type == "tensile":
            return self.run_tensile()
        elif self.type == "cyclic":
            return self.run_cyclic()
        raise ValueError(f"The data type '{self.type}' is not supported")

    # Runs the creep driver
    def run_creep(self) -> dict:
        stress = self.exp_data["stress"]
        results = drivers.creep(self.model, stress, STRESS_RATE, TIME_HOLD, T=self.exp_data["temperature"], verbose=VERBOSE,
                                check_dmg=False, dtol=DAMAGE_TOL, nsteps_up=NUM_STEPS_UP, nsteps=NUM_STEPS, logspace=False)
        results["rtime"] /= 3600
        return results

    # Runs the tensile driver
    def run_tensile(self) -> dict:
        strain_rate = self.exp_data["strain_rate"] / 3600
        results = drivers.uniaxial_test(self.model, erate=strain_rate, T=self.exp_data["temperature"], emax=MAX_STRAIN,
                                        check_dmg=False, dtol=DAMAGE_TOL, nsteps=NUM_STEPS, verbose=VERBOSE, rtol=REL_TOL, atol=ABS_TOL)
        return results
    
    # Runs the cyclic driver
    def run_cyclic(self) -> dict:
        max_strain = self.exp_data["max_strain"]
        strain_rate = self.exp_data["strain_rate"] / 3600
        num_cycles = int(self.exp_data["num_cycles"])
        results = drivers.strain_cyclic(self.model, T=self.exp_data["temperature"], emax=max_strain, erate=strain_rate,
                                        verbose=VERBOSE, R=CYCLIC_RATIO, ncycles=num_cycles, nsteps=NUM_STEPS,
                                        rtol=REL_TOL, atol=ABS_TOL)
        results["time"] /= 3600
        return results
