"""
 Title:         Driver
 Description:   For running the NEML drivers
 Author:        Janzen Choi

"""

# Libraries
import moga_neml.models.__model__ as __model__
from neml import drivers

# General Driver Constants
MIN_DATA     = 10
TIME_HOLD    = 11500.0 * 3600.0
NUM_STEPS_UP = 50
NUM_STEPS    = 501
REL_TOL      = 1.0E-8 # -6
ABS_TOL      = 1.0E-12 # -!0
VERBOSE      = False

# Specific Driver Constants
STRESS_RATE  = 0.0001
STRAIN_MAX   = 0.7
CYCLIC_RATIO = -1

# Driver class
class Driver:
    
    # Constructor
    def __init__(self, exp_curve:dict, model:__model__.__Model__):
        self.exp_curve = exp_curve
        self.model = model
    
    # Runs the driver based on the experimental curve type
    def run(self) -> dict:
        try:
            if "creep" in self.exp_curve["type"]:
                return self.creep()
            elif "tensile" in self.exp_curve["type"]:
                return self.tensile()
            elif "cyclic" in self.exp_curve["cyclic"]:
                return self.cyclic()
        except:
            return None
    
    # Runs the creep driver
    def creep(self) -> dict:
        stress = self.exp_curve["stress"]
        creep_results = drivers.creep(self.model, stress, STRESS_RATE, TIME_HOLD, T=self.exp_curve["temp"], verbose=VERBOSE,
                                        check_dmg=False, dtol=0.95, nsteps_up=NUM_STEPS_UP, nsteps=NUM_STEPS, logspace=False)
        return {"x": list(creep_results["rtime"] / 3600), "y": list(creep_results["rstrain"])}
    
    # Runs the tensile driver
    def tensile(self) -> dict:
        strain_rate = self.exp_curve["strain_rate"] / 3600
        tensile_results = drivers.uniaxial_test(self.model, erate=strain_rate, T=self.exp_curve["temp"], emax=STRAIN_MAX,
                                                nsteps=NUM_STEPS, verbose=VERBOSE, rtol=REL_TOL, atol=ABS_TOL)
        return {"x": list(tensile_results["strain"]), "y": list(tensile_results["stress"])}
    
    # Runs the cyclic driver
    def cyclic(self) -> dict:
        max_strain = self.exp_curve["max_strain"]
        strain_rate = self.exp_curve["strain_rate"] / 3600
        num_cycles = int(self.exp_curve["num_cycles"])
        cyclic_results = drivers.strain_cyclic(self.model, T=self.exp_curve["temp"], emax=max_strain, erate=strain_rate,
                                               verbose=VERBOSE, R=CYCLIC_RATIO, ncycles=num_cycles, nsteps=NUM_STEPS,
                                               rtol=REL_TOL, atol=ABS_TOL)
        if self.exp_curve["type"] == "cyclic-time-strain":
            return {"x": list(cyclic_results["time"]), "y": list(cyclic_results["strain"])}
        if self.exp_curve["type"] == "cyclic-time-stress":
            return {"x": list(cyclic_results["time"]), "y": list(cyclic_results["stress"])}
        if self.exp_curve["type"] == "cyclic-strain-stress":
            return {"x": list(cyclic_results["strain"]), "y": list(cyclic_results["stress"])}