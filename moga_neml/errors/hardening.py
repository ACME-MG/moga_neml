"""
 Title:         The hardening objective function
 Description:   The objective function for optimising the hardening gradient of a tensile curve
 Author:        Janzen Choi

 """

# Libraries
import numpy as np
from moga_neml.errors.__error__ import __Error__

# The Error class
class Error(__Error__):
    
    # Runs at the start, once (optional)
    def initialise(self, strain_0:float=0.2, strain_1:float=None):
        self.enforce_data_type("tensile")
        exp_data = self.get_exp_data()
        self.strain_0 = strain_0
        self.strain_1 = strain_1 if strain_1 != None else max(exp_data["strain"])
        self.exp_hardening = self.get_hardening(exp_data["strain"], exp_data["stress"])

    # Computes the error value
    def get_value(self, prd_data:dict) -> float:
        prd_hardening = self.get_hardening(prd_data["strain"], prd_data["stress"])
        return abs((self.exp_hardening - prd_hardening) / self.exp_hardening)

    # Gets the elastic modulus
    def get_hardening(self, strain_list:list, stress_list:list):
        new_strain_list, new_stress_list = [], []
        for i in range(len(strain_list)):
            if strain_list[i] >= self.strain_0 and strain_list[i] <= self.strain_1:
                new_strain_list.append(strain_list[i])
                new_stress_list.append(stress_list[i])
        hardening = np.polyfit(new_strain_list, new_stress_list, 1)[0]
        return hardening