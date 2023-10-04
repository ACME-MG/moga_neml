"""
 Title:         Constraint Template
 Description:   Contains the basic structure for a constraint class
 Author:        Janzen Choi

"""

# Libraries
import importlib, os, pathlib, sys
from moga_neml.models.__model__ import __Model__

# The Constraint Template Class
class __Constraint__:

    def __init__(self, name:str, curve_list:list) -> None:
        """
        Class for defining a constraint

        Parameters:
        * `name`:       The name of the constraint
        * `curve_list`: The list of curves
        * `model`:      The model
        """
        self.name       = name
        self.curve_list = curve_list

    def get_name(self) -> str:
        """
        Returns the name of the Constraint
        """
        return self.name

    def get_curve_list(self) -> list:
        """
        Gets the list of curves
        """
        return self.curve_list

    def initialise(self) -> None:
        """
        Runs at the start, once (optional placeholder)
        """
        pass

    def get_value(self) -> float:
        """
        Returns an Constraint (must be overridden)
        """
        raise NotImplementedError

# Creates and return a constraint
def get_constraint(constraint_name:str, x_label:str, y_label:str, weight:str,
                   exp_data:dict, model:__Model__, **kwargs) -> __Constraint__:
    """
    Gets an Constraint

    Parameters:
    * `constraint_name`: The name of the Constraint
    * `x_label`:         The label for the x axis
    * `y_label`:         The label for the y axis
    * `weight`:          The weight applied to the Constraint
    * `exp_data`:        The experimental data
    * `model`:           The model

    Returns the Constraint object
    """

    # Get available Constraints in current folder
    constraints_dir = pathlib.Path(__file__).parent.resolve()
    files = os.listdir(constraints_dir)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in ["__Constraint__", "__pycache__"]]
    
    # Raise Constraint if Constraint name not in available Constraints
    if not constraint_name in files:
        raise NotImplementedError(f"The constraint '{constraint_name}' has not been implemented")

    # Prepare dynamic import
    module_path = f"{constraints_dir}/{constraint_name}.py"
    spec = importlib.util.spec_from_file_location("Constraint_file", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    
    # Import, initialise, and return Constraint
    from constraint_file import Constraint
    constraint = Constraint(constraint_name, x_label, y_label, weight, exp_data, model)
    constraint.initialise(**kwargs)
    return constraint