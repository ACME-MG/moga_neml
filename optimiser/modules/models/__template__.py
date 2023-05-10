"""
 Title:         Model Template
 Description:   Follow this structure when creating custom models
 Author:        Janzen Choi

 """

# Libraries
import modules.models.__model__ as model

# Model Class
class Model(model.ModelTemplate):

    # Runs at the start, once
    def prepare(self):
        
        # Define parameter names and bounds
        self.add_param("param_1", 0.0e1, 1.0e0)
        self.add_param("param_2", 0.0e1, 1.0e0)
        self.add_param("param_3", 0.0e1, 1.0e0)
        
        # Define useful arguments
        arg_1 = self.args[0]
        arg_2 = self.args[1]
        print(arg_1, arg_2)
    
