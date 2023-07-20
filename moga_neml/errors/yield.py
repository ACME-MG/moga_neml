"""
 Title:         The yield objective function
 Description:   The objective function for optimising the yield point of a tensile curve
 Author:        Janzen Choi

 """

# Libraries
import math, numpy as np
import scipy.interpolate as inter
import scipy.optimize as opt
from moga_neml.errors.__error__ import __Error__
from moga_neml._optimise.controller import BIG_VALUE

# The Error class
class Error(__Error__):
    
    # Runs at the start, once (optional)
    def initialise(self, e_stress:float=1.0, offset:float=0.002):
        self.enforce_data_type("tensile")
        exp_data = self.get_exp_data()
        
        # Initialise input variables
        self.e_stress = e_stress
        self.offset = offset
        
        # Get yield point
        self.exp_yield = self.get_yield(exp_data["strain"], exp_data["stress"])
        self.mag_yield = math.sqrt(math.pow(self.exp_yield[0], 2) + math.pow(self.exp_yield[1], 2))

    # Computes the error value
    def get_value(self, prd_data:dict) -> float:
        try:
            prd_yield = self.get_yield(prd_data["strain"], prd_data["stress"])
        except ValueError:
            return BIG_VALUE
        distance = math.sqrt(math.pow(self.exp_yield[0] - prd_yield[0], 2) + math.pow(self.exp_yield[1] - prd_yield[1], 2))
        return distance / self.mag_yield

    # Gets the elastic modulus
    def get_elastic_modulus(self, strain_list:list, stress_list:list) -> float:
        new_strain_list, new_stress_list = [], []
        for i in range(len(strain_list)):
            if stress_list[i] < self.e_stress:
                new_strain_list.append(strain_list[i])
                new_stress_list.append(stress_list[i])
        polynomial = np.polyfit(new_strain_list, new_stress_list, 1)
        return polynomial[0]

    # Gets the yield point
    def get_yield(self, strain_list:list, stress_list:list) -> tuple:
        youngs = self.get_elastic_modulus(strain_list, stress_list)
        sfn = inter.interp1d(strain_list, stress_list, bounds_error=False, fill_value=0)
        tfn = lambda e: youngs * (e - self.offset)
        yield_strain = opt.brentq(lambda e: sfn(e) - tfn(e), 0.0, np.max(strain_list))
        yield_stress = float(tfn(yield_strain))
        print("[{:0.4}], [{:0.4}]".format(yield_strain, yield_stress))
        return yield_strain, yield_stress
