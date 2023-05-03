"""
 Title:         Trainer
 Description:   Contains the basic structure for a trainer class
 Author:        Janzen Choi

"""

# Libraries
import sys, os, importlib
from modules.mapper import MultiMapper

# Helper libraries
sys.path += ["../__common__", "../__models__"]
from plotter import quick_plot_N
from curve import validate_curve
from __model__ import ModelTemplate

# Constants
PATH_TO_TRAINERS = "modules/trainers"
EXCLUSION_LIST = ["__trainer__", "__pycache__"]

# The Trainer Template Class
class TrainerTemplate:

    # Constructor
    def __init__(self, model, name, output_lb, output_ub):

        # Define model and trainer name
        self.model = model
        self.name = name

        # Define input / output variables
        input_lb = self.model.get_param_lower_bounds()
        input_ub = self.model.get_param_upper_bounds()
        self.param_mapper = MultiMapper(input_lb, input_ub)
        self.curve_mapper = MultiMapper(output_lb, output_ub)
        self.input_size = len(input_lb)
        self.output_size = len(output_lb)

    # Returns the name of the trainer
    def get_name(self):
        return self.name

    # Returns the raw curve from the model
    def get_raw_curve(self, unmapped_input):
        curves = self.model.get_prd_curves(*unmapped_input)
        curve = {"x": curves[0]["x"], "y": curves[0]["y"]} if curves != [] else {"x": [], "y": []}
        return curve

    # Maps the input
    def map_input(self, unmapped_input):
        return self.param_mapper.map(unmapped_input)

    # Maps the output
    def map_output(self, unmapped_output):
        return self.curve_mapper.map(unmapped_output)

    # Unmaps the input
    def unmap_input(self, mapped_input):
        return self.param_mapper.unmap(mapped_input)

    # Unmaps the output
    def unmap_output(self, mapped_output):
        return self.curve_mapper.unmap(mapped_output)

    # Returns the input / output size
    def get_shape(self):
        return self.input_size, self.output_size

    # Makes a plot of the raw and restored curves
    def plot(self, mapped_input, mapped_output, path):

        # Unmap input / output
        unmapped_input = self.unmap_input(mapped_input)
        unmapped_output = self.unmap_output(mapped_output)

        # Get raw and restored curve
        raw_curve = self.get_raw_curve(unmapped_input)
        restored_curve = self.restore_curve(unmapped_output)
        
        # Plot
        quick_plot_N(path, [[raw_curve], [restored_curve]], ["Original", "Restored"], ["r", "b'"])

    # Returns the input / output data with validification
    def get_io(self, unmapped_input):
        curve = self.get_raw_curve(unmapped_input)
        if validate_curve(curve):
            return self.__get_io__(unmapped_input, curve)
        return None, None

    # Returns the training input / output data (placeholder)
    def __get_io__(self, unmapped_input, curve):
        raise NotImplementedError

    # Converts the outputs into a curve (placeholder)
    def restore_curve(self, unmapped_output):
        raise NotImplementedError
    
# Creates and return a trainer
def get_trainer(trainer_name:str, model:ModelTemplate) -> TrainerTemplate:

    # Get available trainers in current folder
    files = os.listdir(PATH_TO_TRAINERS)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in EXCLUSION_LIST]
    
    # Raise trainer if trainer name not in available trainers
    if not trainer_name in files:
        raise NotImplementedError(f"The trainer '{trainer_name}' has not been implemented")

    # Import and prepare trainer
    module = f"{PATH_TO_TRAINERS}/{trainer_name}".replace("/", ".")
    trainer_file = importlib.import_module(module)
    trainer = trainer_file.Trainer(model)

    # Return the trainer
    return trainer