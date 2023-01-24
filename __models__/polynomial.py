"""
 Title:         Polynomial model (stress/temperature independent)
 Description:   Purely empirical model for testing only
 Author:        Janzen Choi

"""

# Libraries
import __model__ as model

# Constants
TIME_STEP = 5

# The Polynomial Class
class Polynomial(model.Model):

    # Constructor
    def __init__(self, exp_curves):
        super().__init__(
            name = "polynomial",
            param_info = [
                {"name": "x_0",     "min": 0e0,     "max": 1e0},
                {"name": "x_1",     "min": 0e0,     "max": 1e0},
                {"name": "x_2",     "min": 0e0,     "max": 1e0},
                {"name": "x_3",     "min": 0e0,     "max": 1e0},
                {"name": "x_end",   "min": 0e0,     "max": 1e4},
            ],
            exp_curves = exp_curves
        )

    # Prepares the model
    def prepare(self, args):
        pass

    # Gets the predicted curves
    def get_prd_curves(self, x_0, x_1, x_2, x_3, x_end):
        prd_curves = super().get_prd_curves()

        # Get each predicted curve
        for i in range(len(prd_curves)):
            prd_curves[i]["x"] = list(range(0, round(x_end), TIME_STEP))
            if len(prd_curves[i]["x"]) < 10:
                return []
            prd_curves[i]["y"] = [x_0 + x_1*time + x_2*time**2 + x_3*time**3 for time in prd_curves[i]["x"]]

        # Return predicted curves
        return prd_curves