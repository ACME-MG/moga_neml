"""
 Title:         Surrogate
 Description:   Contains the basic structure for a surrogate class
 Author:        Janzen Choi

"""

# The Surrogate Class
class Surrogate:

    # Constructor
    def __init__(self, name, input_size, output_size):
        self.name        = name
        self.input_size  = input_size
        self.output_size = output_size

    # Returns the name of the trainer
    def get_name(self):
        return self.name

    # Prepares the model (placeholder)
    def prepare(self):
        raise NotImplementedError

    # Fits the model (placeholder)
    def fit(self):
        raise NotImplementedError

    # Makes a single prediction (placeholder)
    def predict(self):
        raise NotImplementedError