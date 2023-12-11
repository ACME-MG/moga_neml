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
DAMAGE_TOL   = 0.95 # 0.95
STRESS_RATE  = 0.0001
CYCLIC_RATIO = -1

# Driver class
class Driver:
    
    def __init__(self, exp_data:dict, model, num_steps:int=500, rel_tol:float=1e-6,
                 abs_tol:float=1e-10, verbose:bool=False) -> None:
        """
        Initialises the driver class
        
        Parameters:
        * `exp_data`:  Dictionary of experimental data
        * `model`:     The model to be run
        * `num_steps`: Number of steps to run
        * `rel_tol`:   Relative error tolerance
        * `abs_tol`:   Absolute error tolerance
        * `verbose`:   Whether to run the driver in verbose mode
        """
        self.exp_data  = exp_data
        self.type      = self.exp_data["type"]
        self.model     = model
        self.num_steps = num_steps
        self.rel_tol   = rel_tol
        self.abs_tol   = abs_tol
        self.verbose   = verbose
        self.conv_dict = NEML_FIELD_CONVERSION[self.type]
    
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
        if self.type == "creep":
            return self.run_creep()
        elif self.type == "tensile":
            return self.run_tensile()
        elif self.type == "cyclic":
            return self.run_cyclic()
        raise ValueError(f"The data type '{self.type}' is not supported")

    def run_creep(self) -> dict:
        """
        Runs the creep driver;
        returns the results
        """
        stress = self.exp_data["stress"]
        results = drivers.creep(self.model, stress, STRESS_RATE, TIME_HOLD, T=self.exp_data["temperature"], verbose=self.verbose,
                                check_dmg=True, dtol=DAMAGE_TOL, nsteps_up=NUM_STEPS_UP, nsteps=self.num_steps, logspace=False)
        results["rtime"] /= 3600
        return results

    def run_tensile(self) -> dict:
        """
        Runs the tensile driver;
        returns the results
        """
        strain_rate = self.exp_data["strain_rate"] / 3600
        results = drivers.uniaxial_test(self.model, erate=strain_rate, T=self.exp_data["temperature"], emax=MAX_STRAIN,
                                        check_dmg=True, dtol=DAMAGE_TOL, nsteps=self.num_steps, verbose=self.verbose, rtol=self.rel_tol, atol=self.abs_tol)
        return results
    
    def run_cyclic(self) -> dict:
        """
        Runs the cyclic driver;
        returns the results
        """
        max_strain = self.exp_data["max_strain"]
        strain_rate = self.exp_data["strain_rate"] / 3600
        num_cycles = int(self.exp_data["num_cycles"])
        results = drivers.strain_cyclic(self.model, T=self.exp_data["temperature"], emax=max_strain, erate=strain_rate,
                                        verbose=self.verbose, R=CYCLIC_RATIO, ncycles=num_cycles, nsteps=self.num_steps)
        results["time"] /= 3600
        return results
