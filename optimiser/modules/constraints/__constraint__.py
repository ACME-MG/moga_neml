"""
 Title:         Constraint Template
 Description:   Contains the basic structure for a constraints class
 Author:        Janzen Choi

"""

# Libraries
import importlib, os

# Constants
PATH_TO_CONSTRAINTS = "modules/constraints"
EXCLUSION_LIST = ["__constraint__", "__pycache__"]

# The Constraint Template Class
class ConstraintTemplate:

    # Define main arguments
    def set_vals(self, name:str, type:str, penalty:float, exp_curves:list[dict]) -> None:
        self.name = name
        self.type = type
        self.penalty = penalty
        self.exp_curves = exp_curves

    # Returns the name of the constraint
    def get_name(self) -> str:
        return self.name

    # Returns the type of the constraint
    def get_type(self) -> str:
        return self.type

    # Returns the penalty of the constraint
    def get_penalty(self) -> float:
        return self.penalty

    # Returns the experimental curve
    def get_exp_curves(self) -> list[dict]:
        return self.exp_curves

    # Returns a constraint (placeholder)
    def get_value(self) -> None:
        raise NotImplementedError
    
    # Groups creep curves by temperature and orders them by stress
    def set_curve_map(self, exp_curves:list[dict]) -> None:
        
        # Get unique temperatures
        temp_list = [exp_curve["temp"] for exp_curve in exp_curves if exp_curve["type"] == "creep"]
        temp_list = list(set(temp_list))
        
        # Group curves by temperature
        self.curve_dict = {}
        for temp in temp_list:

            # Sort curves by stress
            curve_list = [exp_curve for exp_curve in exp_curves if exp_curve["type"] == "creep" and exp_curve["temp"] == temp]
            curve_list.sort(key=get_stress)
            
            # Get their indexes and add to map
            index_list = [exp_curves.index(temp_curve) for temp_curve in curve_list]
            self.curve_dict[temp] = index_list

    # Runs at the start, once (optional placeholder)
    def prepare(self):
        pass

# Returns the stress from a curve
def get_stress(curve:dict) -> float:
    return curve["stress"]

# Creates and return a constraint
def get_constraint(constraint_name:str, type:str, penalty:float, exp_curves:list[dict]) -> ConstraintTemplate:

    # Get available constraints in current folder
    files = os.listdir(PATH_TO_CONSTRAINTS)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in EXCLUSION_LIST]
    
    # Raise error if constraint name not in available constraints
    if not constraint_name in files:
        raise NotImplementedError(f"The constraint '{constraint_name}' has not been implemented")

    # Import and prepare constraint
    module = f"{PATH_TO_CONSTRAINTS}/{constraint_name}".replace("/", ".")
    constraint_file = importlib.import_module(module)
    constraint = constraint_file.Constraint()
    constraint.set_vals(constraint_name, type, penalty, exp_curves)
    constraint.set_curve_map(exp_curves)
    constraint.prepare()

    # Return the constraint
    return constraint