"""
 Title:         API for Surrogate Modelling
 Description:   For developing surrogate models
 Author:        Janzen Choi
 
"""

# Libraries
import time, sys
from modules.sampler import Sampler
from modules.surrogate import Surrogate
from modules.trainers.__trainer_factory__ import get_trainer
from modules.trainers.__trainer__ import get_sample_curve

# Helper libraries
sys.path += ["../__common__", "../__models__"]
from progressor import Progressor
from plotter import quick_plot
from general import safe_mkdir
from __model_factory__ import get_model
from __model__ import get_curve

# I/O directories
INPUT_DIR   = "./input"
RESULTS_DIR = "./results"

# API Class
class API:

    # Constructor
    def __init__(self, fancy=False, title="", verbose=False):
        
        # Initialise
        self.prog = Progressor(fancy, title, verbose)
        self.plot_count = 1

        # Set up environment
        title = "" if title == "" else f" ({title})"
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_path = f"{RESULTS_DIR}/{self.output_dir}{title}"
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

    # Defines the conditions of the creep (celcius and MPa)
    def define_conditions(self, temp=800, stress=80):
        self.prog.add(f"Defining conditions at {temp}°C and {stress}MPa")
        self.curve = get_curve([10000], [1], "", "", "creep", stress=stress, temp=temp, test="")

    # Defines the model
    def define_model(self, model_name=""):
        self.prog.add(f"Defining the {model_name} model")
        self.model = get_model(model_name, [self.curve])
        self.l_bounds = self.model.get_param_lower_bounds()
        self.u_bounds = self.model.get_param_upper_bounds()
        self.sampler = Sampler(self.l_bounds, self.u_bounds)

    # Defines the trainer
    def define_trainer(self, trainer_name):
        self.prog.add(f"Defining the '{trainer_name}' trainer")
        self.trainer = get_trainer(trainer_name, self.model)
        input_size, output_size = self.trainer.get_shape()
        self.surrogate = Surrogate(input_size, output_size)

    # Reads input data from a CSV file
    def read_input(self, file, delimiter=","):
        self.prog.add(f"Reading surrogate model input from '{file}'")
        path = f"{INPUT_DIR}/{file}"
        
        # Read input data
        with open(path, "r") as data_file:
            all_lines = data_file.readlines()
        
        # Extract unmapped inputs and calculate outputs
        self.sm_inputs, self.sm_outputs = [], []
        for line in all_lines:
            unmapped_input = [float(v) for v in line.replace("\n", "").split(delimiter)]
            mapped_input, mapped_output = self.trainer.get_io(unmapped_input)
            self.sm_inputs.append(mapped_input)
            self.sm_outputs.append(mapped_output)

    # Writes input and output data to a CSV file
    def write_input_output(self, file, delimiter=","):
        self.prog.add(f"Writing surrogate model input / output to '{file}'")
        
        # Open file for writing
        path = f"{self.output_path}/{file}"
        data_file = open(path, "w+")

        # Unmap input and output and write
        for i in range(len(self.sm_inputs)):
            unmapped_input = self.trainer.unmap_input(self.sm_inputs[i])
            unmapped_output = self.trainer.unmap_output(self.sm_outputs[i])
            data_list = [str(v) for v in unmapped_input+unmapped_output]
            data_line = f"{delimiter.join(data_list)}\n"
            data_file.write(data_line)
        data_file.close()

    # Reads input and output data from a CSV file
    def read_input_output(self, file, delimiter=","):
        self.prog.add(f"Reading surrogate model input / output from '{file}'")
        path = f"{INPUT_DIR}/{file}"
        
        # Read data (unmapped inputs, unmapped outputs)
        with open(path, "r") as data_file:
            all_lines = data_file.readlines()

        # Extract unmapped inputs and outputs
        self.sm_inputs, self.sm_outputs = [], []
        input_size, _ = self.trainer.get_shape()
        for line in all_lines:
            line_list = [float(v) for v in line.replace("\n", "").split(delimiter)]

            # Map
            mapped_input = self.trainer.map_input(line_list[:input_size])
            mapped_output = self.trainer.map_output(line_list[input_size:])
            
            # Add to sample
            self.sm_inputs.append(mapped_input)
            self.sm_outputs.append(mapped_output)

    # Samples the parameter space randomly
    def sample_random(self, size=10):
        self.prog.add(f"Sampling {size} random parameter(s)")
        
        # Continually generate random parameters
        self.sm_inputs, self.sm_outputs = [], []
        while True:

            # Generate random curve and check validity
            params = self.sampler.sample_random()[0]
            mapped_input, mapped_output = self.trainer.get_io(params)
            if mapped_input == None or mapped_output == None:
                print("  FAILURE - redo")
                continue
            
            # If curve is valid, then add to sample space
            print(f"  SUCCESS - {len(self.sm_inputs)+1}/{size}")
            self.sm_inputs.append(mapped_input)
            self.sm_outputs.append(mapped_output)
            if len(self.sm_inputs) == size:
                break

    # Plots the sample
    def plot_sample(self):
        self.prog.add(f"Plotting the curves of {len(self.sm_inputs)} samples")
        for i in range(len(self.sm_inputs)):
            self.trainer.plot(self.sm_inputs[i], self.sm_outputs[i], self.output_path, f"plot_{self.plot_count}_sample")
            self.plot_count += 1

    # Trains the surrogate model
    def train(self, epochs=100, batch_size=32):
        self.prog.add(f"Training the surrogate model")
        self.surrogate.fit(self.sm_inputs, self.sm_outputs, epochs, batch_size)

    # Predicts a curve using the trained surrogate model
    def assess(self):
        self.prog.add(f"Assessing the surrogate model {len(self.sm_inputs)} time(s)")
        for i in range(len(self.sm_inputs)):

            # Get curve from model and surrogate model
            model_curve = self.trainer.restore_curve(self.sm_outputs[i])
            sm_curve = self.surrogate.predict(self.sm_inputs[i])[0]
            sm_curve = self.trainer.restore_curve(sm_curve)

            # Plot the results and print out progress
            quick_plot(model_curve, sm_curve, "Model", "Surrogate", self.output_path, f"plot_{self.plot_count}_test")
            print(f"  {i+1})\tTested - {i+1}/{len(self.sm_inputs)}")
            self.plot_count += 1

    # Tests the trainer scheme
    def __test_trainer__(self):
        self.prog.add(f"Testing the '{self.trainer.get_name()}' trainer")
        sample_curve = get_sample_curve()
        input_size, _ = self.trainer.get_shape()
        _, reduced_curve = self.trainer.__get_io__([0]*input_size, sample_curve)
        restored_curve = self.trainer.restore_curve(reduced_curve)
        quick_plot(sample_curve, restored_curve, "Original", "Restored", self.output_path, f"plot_trainer_test")