import sys; sys.path += ["../.."]
from moga_neml.api import API
 
api = API("chaboche ss", input_path="../data", output_path="../results")
api.define_model("cih")

api.read_data("cyclic/Airbase316.csv")
api.change_data("num_cycles", 1)
api.add_error("area", "time", "strain")
api.add_error("area", "time", "stress")
 
api.set_driver(verbose=True)
api.set_recorder(10, True, True, True, True)
 
moga_generations = 10000
moga_population  = 50
moga_offsprings  = 25
moga_crossover   = 0.60
moga_mutation    = 0.10
api.optimise(moga_generations, moga_population, moga_offsprings, moga_crossover, moga_mutation)