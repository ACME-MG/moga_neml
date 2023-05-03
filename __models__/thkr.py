"""
 Title:         Time-Hardening Kachanov-Rabotnov model coupled with Kachanov-Rabotnov model
 Description:   Predicts all three stages of creep
 Author:        Janzen Choi

"""

# Libraries
import math
import __model__ as model
from cmath import inf

# Constants
TIME_STEP = 5
TIME_LIMIT = 10000

# The Time-Hardening Kachanov-Rabotnov Class
class Model(model.ModelTemplate):

    # Constructor
    def __init__(self):
        super().__init__([
            {"name": "th_a",    "min": 1e-50,   "max": 1e0},
            {"name": "th_n",    "min": 1e-50,   "max": 1e2},
            {"name": "th_m",    "min": 1e-50,   "max": 1e1},
            {"name": "kr_A",    "min": 1e-30,   "max": 1e-5},
            {"name": "kr_n",    "min": 1e-50,   "max": 1e1},
            {"name": "kr_M",    "min": 1e-50,   "max": 1e0},
            {"name": "kr_phi",  "min": 1e-50,   "max": 1e2},
            {"name": "kr_chi",  "min": 1e-50,   "max": 1e1},
        ])

    # Prepares the model
    def prepare(self, args):
        pass

    # Gets the predicted curves
    def get_prd_curves(self, th_a, th_n, th_m, kr_A, kr_n, kr_M, kr_phi, kr_chi):
        prd_curves = super().get_prd_curves()

        # Iterate through stress values
        for i in range(len(prd_curves)):
            stress = self.exp_curves[i]["stress"]
            
            # Calculate primary strain with TH model
            offset_time, offset_strain = 0, 0
            for time in range(0, TIME_LIMIT, TIME_STEP):

                # Calculate, check, and append strain
                th_strain = th_a*stress**th_n/(th_m+1)*time**(th_m+1)
                if math.isnan(th_strain) or abs(th_strain) == inf:
                    break
                prd_curves[i]["x"].append(time)
                prd_curves[i]["y"].append(th_strain)

                # Start using KR model when strain rate < minimum creep rate
                offset_time, offset_strain = time, th_strain
                if time > 0 and th_a * stress**th_n * time**th_m < kr_A*stress**kr_n:
                    break
            
            # Calculate secondary and tertiary strain with KR model
            for time in range(offset_time, TIME_LIMIT, TIME_STEP):
                kr_time = time - offset_time
                kr_strain = kr_A*stress**kr_n*((1-(kr_phi+1)*kr_M*stress**kr_chi*kr_time)**((kr_phi+1-kr_n)/(kr_phi+1))-1)/(kr_M*stress**kr_chi*(kr_n-kr_phi-1))
                if isinstance(kr_strain, complex) or math.isnan(kr_strain) or abs(kr_strain) == inf:
                    break
                prd_curves[i]["x"].append(time)
                prd_curves[i]["y"].append(kr_strain + offset_strain)

        # Return list of curves
        return prd_curves