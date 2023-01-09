"""
 Title:         Main file
 Description:   For developing surrogate models
 Author:        Janzen Choi
 
"""

# Libraries
from modules.api import API

# Code
api = API(True)
api.define_conditions(800, 80)
api.define_model("evpwd")
api.define_trainer("strain")

api.__test_trainer__()
exit()


api.read_input("evpwd_i.csv", ",")
api.write_input_output("evpwd_io.csv", ",")

api.sample_random(10)
api.plot_sample()

api.train(epochs=100)
api.sample_random(10)
api.assess()