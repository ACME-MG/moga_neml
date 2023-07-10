"""
 Title:         The n_cycles objective function
 Description:   The objective function for optimising damage to be closer to 1
 Author:        Janzen Choi

 """

# Libraries
import math
from moga_neml.errors.__error__ import __Error__

# The Error class
class Error(__Error__):
    
    # Runs at the start, once (optional)
    def initialise(self):
        self.model = self.get_model()

    # Computes the error value
    def get_value(self, prd_data:dict) -> float:
        damage_history = prd_data["history"][-1]
        damage = self.model.get_last_calibrated_model().get_damage(damage_history)
        try:
            return math.pow(1 - damage, 2)
        except OverflowError:
            return # math domain error