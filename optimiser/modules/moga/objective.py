"""
 Title:         The Objective class
 Description:   For storing the errors to be minimised
 Author:        Janzen Choi

"""

# Libraries
import math
import numpy as np
from modules.errors.__error__ import ErrorTemplate
from modules.constraints.__constraint__ import ConstraintTemplate
from modules.models.__model__ import ModelTemplate

# Constants
BIG_VALUE = 10000

# The Objective class
class Objective():

    # Constructor
    def __init__(self, model:ModelTemplate, error_list:list[ErrorTemplate], constraint_list:list[ConstraintTemplate]):
        self.model = model
        self.error_list = error_list
        self.constraint_list = constraint_list

    # Returns the model
    def get_model(self) -> ModelTemplate:
        return self.model

    # Returns the objective names
    def get_error_names(self) -> list[str]:
        return [error.get_name() for error in self.error_list]

    # Returns the objective types
    def get_error_types(self) -> list[str]:
        return [error.get_type() for error in self.error_list]

    # Returns the objective weights
    def get_error_weights(self) -> list[float]:
        return [error.get_weight() for error in self.error_list]

    # Gets all the errors
    def get_error_values(self, prd_curves:list[dict]) -> list[float]:
        if prd_curves == []:
            return [BIG_VALUE] * len(self.error_list)
        error_values = [error.get_value(prd_curves)*error.get_weight() for error in self.error_list]
        error_values = [BIG_VALUE if math.isnan(error_value) else error_value for error_value in error_values]
        return error_values
    
    # Returns the constraint names
    def get_constraint_names(self) -> list[str]:
        return [constraint.get_name() for constraint in self.constraint_list]
    
    # Returns the constraint types
    def get_constraint_types(self) -> list[str]:
        return [constraint.get_type() for constraint in self.constraint_list]
    
    # Returns the constraint penalty
    def get_constraint_penalties(self) -> list[float]:
        return [constraint.get_penalty() for constraint in self.constraint_list]

    # Gets all the constraint penalty values
    def get_constraint_values(self, prd_curves:list[dict]) -> list[bool]:
        if prd_curves == []:
            return [False] * len(self.constraint_list)
        constraint_values = [constraint.get_value(prd_curves) for constraint in self.constraint_list]
        return constraint_values
    
    # Gets the penalised error values
    def get_penalised_error_values(self, error_values:list[float], constraint_values:list[bool]) -> list[float]:
        total_penalty = np.prod([self.constraint_list[i].get_penalty() if not constraint_values[i] else 1 for i in range(len(constraint_values))])
        penalised_error_values = [total_penalty * error_value for error_value in error_values]
        return penalised_error_values