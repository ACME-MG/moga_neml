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
        self.enforce_data_type("creep")
        self.enforce_model("evpwd")
        self.model = self.get_model()

    # Computes the error value
    def get_value(self, prd_data:dict) -> float:
        damage_history = prd_data["damage"][-1]
        damage = self.model.get_last_calibrated_model().get_damage(damage_history)
        # return 1 - math.sqrt(1 - math.pow(1 - damage, 2))
        return math.pow(1 - damage, 2)