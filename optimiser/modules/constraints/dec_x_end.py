"""
 Title:         Decreasing X End
 Description:   Constraint for ensuring that creep curves have decreasing rupture times with stress
 Author:        Janzen Choi

"""

# Libraries
import modules.constraints.__constraint__ as constraint

# The DecXEnd Class
class DecXEnd(constraint.Constraint):

    # Constructor
    def __init__(self, exp_curves):
        super().__init__("dec_x_end", exp_curves)
        self.curve_dict = constraint.get_curve_map(exp_curves)
    
    # Returns the constraint vayue
    def get_value(self, prd_curves):
        constraint_value = 0
        for temp in self.curve_dict.keys():
            curves = [prd_curves[i] for i in self.curve_dict[temp]]
            for i in range(1,len(curves)):
                x_end_diff = curves[i]["x"][-1] - curves[i-1]["x"][-1]
                constraint_value += x_end_diff
        return constraint_value