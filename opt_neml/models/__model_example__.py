"""
 Title:         Model Example
 Description:   Follow this structure when creating custom models
 Author:        Janzen Choi

 """

# Libraries
import opt_neml.models.__model__ as model

# Model Class
class Model(model.ModelTemplate):

    # Runs at the start, once (mandatory)
    def prepare(self):
        
        # Define parameter names and bounds (mandatory)
        self.add_param("param_1", 0.0e1, 1.0e0)
        self.add_param("param_2", 0.0e1, 1.0e0)
        self.add_param("param_3", 0.0e1, 1.0e0)
        
        # Define test condition (optional)
        exp_curve = self.get_exp_curve()
        self.temp = exp_curve["temp"]
        self.stress = exp_curve["stress"]

        # Define useful arguments (optional)
        args = self.get_args()
        self.arg_1 = args[0]
        self.arg_2 = args[1]
    
    # Gets the predicted curve
    def get_prd_curve(self, param_1, param_2, param_3):

        # Derive curve from parameters, experimental curve, and/or useful arguments
        x_list = [self.arg_1, param_2, param_3-self.stress]
        y_list = [param_1, self.arg_2, self.temp+param_3]

        # Return curve if valid
        if x_list[0] >= 0:
            return {"x": x_list, "y": y_list}
        
        # Return nothing if invalid (e.g., if error encountered)
        if x_list[0] < 0:
            return None