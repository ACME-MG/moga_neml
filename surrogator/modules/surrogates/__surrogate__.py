"""
 Title:         Surrogate Template
 Description:   Contains the basic structure for a surrogate class
 Author:        Janzen Choi

"""

# Libraries
import importlib, os

# Constants
PATH_TO_SURROGATES = "modules/surrogates"
EXCLUSION_LIST = ["__surrogate__", "__pycache__"]

# The Surrogate Template Class
class SurrogateTemplate:

    # Sets the name of the surrogate
    def set_val(self, name:str, input_size:int, output_size:int):
        self.name = name
        self.input_size  = input_size
        self.output_size = output_size

    # Returns the name of the surrogate
    def get_name(self):
        return self.name

    # Prepares the model (optional placeholder)
    def prepare(self):
        pass

    # Fits the model (placeholder)
    def fit(self):
        raise NotImplementedError

    # Makes a single prediction (placeholder)
    def predict(self):
        raise NotImplementedError

# Creates and return a surrogate
def get_surrogate(surrogate_name:str, input_size:int, output_size:int) -> SurrogateTemplate:

    # Get available surrogates in current folder
    files = os.listdir(PATH_TO_SURROGATES)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in EXCLUSION_LIST]
    
    # Raise surrogate if surrogate name not in available surrogates
    if not surrogate_name in files:
        raise NotImplementedError(f"The surrogate '{surrogate_name}' has not been implemented")

    # Import and prepare surrogate
    module = f"{PATH_TO_SURROGATES}/{surrogate_name}".replace("/", ".")
    surrogate_file = importlib.import_module(module)
    surrogate = surrogate_file.Surrogate()
    surrogate.set_val(surrogate_name, input_size, output_size)
    surrogate.prepare()

    # Return the surrogate
    return surrogate