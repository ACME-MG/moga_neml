"""
 Title:         Model Example
 Description:   Follow this structure when creating custom models
 Author:        Janzen Choi

 """

# Libraries
import modules.models.__model__ as model

# Model Class
class Model(model.ModelTemplate):

    # Runs at the start, once (mandatory)
    def prepare(self):
        
        # Define parameter names and bounds (mandatory)
        self.add_param("param_1", 0.0e1, 1.0e0)
        self.add_param("param_2", 0.0e1, 1.0e0)
        self.add_param("param_3", 0.0e1, 1.0e0)
        
        # Define useful arguments (optional)
        self.arg_1 = self.args[0]
        self.arg_2 = self.args[1]
    
    # Gets the predicted curve
    def get_prd_curve(self, exp_curve, param_1, param_2, param_3):

        # Extract important information from experimental curve
        temp = exp_curve["temp"]
        stress = exp_curve["stress"]

        # Derive curve from parameters, experimental curve, and/or useful arguments
        x_list = [self.arg_1, param_2, param_3-stress]
        y_list = [param_1, self.arg_2, temp+param_3]

        # Return curve if valid
        if x_list[0] >= 0:
            return {"x": x_list, "y": y_list}
        
        # Return nothing if invalid (e.g., if error encountered)
        if x_list[0] < 0:
            return None