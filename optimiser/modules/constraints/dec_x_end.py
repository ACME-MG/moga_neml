"""
 Title:         Decreasing X End
 Description:   Constraint for ensuring that creep curves have decreasing rupture times with stress
 Author:        Janzen Choi

"""

# Libraries
import modules.constraints.__constraint__ as constraint

# The DecXEnd Class
class Constraint(constraint.ConstraintTemplate):
    
    # Returns True if passed, and False if not passed
    def get_value(self, prd_curves:list[dict]) -> bool:
        for temp in self.curve_dict.keys():
            curves = [prd_curves[i] for i in self.curve_dict[temp]]
            for i in range(1,len(curves)):
                if self.exp_curves[i]["type"] != self.type:
                    continue
                x_end_diff = curves[i]["x"][-1] - curves[i-1]["x"][-1]
                if x_end_diff > 0:
                    return False
        return True