"""
 Title:         The surrogate Factory
 Description:   For creating and returning surrogate objects
 Author:        Janzen Choi

"""

# surrogates
from modules.surrogates.ann import ANN

# Creates and return a surrogate
def get_surrogate(surrogate_name, input_size, output_size):
    surrogate_list = (
        ANN(input_size, output_size),
    )
    surrogate = [surrogate for surrogate in surrogate_list if surrogate.get_name() == surrogate_name][0]
    surrogate.prepare()
    return surrogate