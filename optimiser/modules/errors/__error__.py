"""
 Title:         Error
 Description:   Contains the basic structure for an error class
 Author:        Janzen Choi

"""

# The Error Class
class Error:

    # Constructor
    def __init__(self, name:str, type:str, weight:float, exp_curves:list[dict]):
        self.name = name
        self.type = type
        self.weight = weight
        self.exp_curves = exp_curves

    # Returns the name of the error
    def get_name(self) -> str:
        return self.name

    # Returns the type of the error
    def get_type(self) -> str:
        return self.type

    # Returns the weight of the error
    def get_weight(self) -> float:
        return self.weight

    # Returns the experimental curve
    def get_exp_curves(self) -> list[dict]:
        return self.exp_curves

    # Prepares the object for evaluation (placeholder)
    def prepare(self) -> None:
        raise NotImplementedError
    
    # Returns an error (placeholder)
    def get_value(self) -> None:
        raise NotImplementedError