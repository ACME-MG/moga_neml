"""
 Title:         Time-Hardening Kachanov-Rabotnov model coupled with Kachanov-Rabotnov model
 Description:   Predicts all three stages of creep
 Author:        Janzen Choi

"""

# Libraries
import math
import modules.models.__model__ as model
from cmath import inf

# Constants
TIME_STEP = 5
TIME_LIMIT = 10000

# The Time-Hardening Kachanov-Rabotnov Class
class Model(model.ModelTemplate):

    # Runs at the start, once
    def prepare(self):

        # Define parameters
        self.add_param("th_a",   0.0e0, 1.0e0)
        self.add_param("th_n",   0.0e0, 1.0e2)
        self.add_param("th_m",   0.0e0, 1.0e1)
        self.add_param("kr_A",   0.0e0, 1.0e-5)
        self.add_param("kr_n",   0.0e0, 1.0e1)
        self.add_param("kr_M",   0.0e0, 1.0e0)
        self.add_param("kr_phi", 0.0e0, 1.0e2)
        self.add_param("kr_chi", 0.0e0, 1.0e1)

        # Define test conditions
        exp_curve = self.get_exp_curve()
        self.stress = exp_curve["stress"]
        self.type = exp_curve["type"]

    # Gets the predicted curve
    def get_prd_curve(self, th_a, th_n, th_m, kr_A, kr_n, kr_M, kr_phi, kr_chi):

        # If the curve is not a creep curve, return nothing
        if self.type != "creep":
            return

        # Calculate primary strain with TH model
        time_list, strain_list = [], []
        offset_time, offset_strain = 0, 0
        for time in range(0, TIME_LIMIT, TIME_STEP):

            # Calculate, check, and append strain
            th_strain = th_a*self.stress**th_n/(th_m+1)*time**(th_m+1)
            if math.isnan(th_strain) or abs(th_strain) == inf:
                break
            time_list.append(time)
            strain_list.append(th_strain)

            # Start using KR model when strain rate < minimum creep rate
            offset_time, offset_strain = time, th_strain
            if time > 0 and th_a * self.stress**th_n * time**th_m < kr_A*self.stress**kr_n:
                break
        
        # Calculate secondary and tertiary strain with KR model
        for time in range(offset_time, TIME_LIMIT, TIME_STEP):
            kr_time = time - offset_time
            kr_strain = kr_A*self.stress**kr_n*((1-(kr_phi+1)*kr_M*self.stress**kr_chi*kr_time)**((kr_phi+1-kr_n)/(kr_phi+1))-1)/(kr_M*self.stress**kr_chi*(kr_n-kr_phi-1))
            if isinstance(kr_strain, complex) or math.isnan(kr_strain) or abs(kr_strain) == inf:
                break
            time_list.append(time)
            strain_list.append(kr_strain + offset_strain)

        # Return predicted curve
        return {"x": time_list, "y": strain_list}