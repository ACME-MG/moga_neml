import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("evp 1000 all", input_path="../data", output_path="../results")

itf.define_model("evp")

itf.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
itf.remove_damage(0.2, 0.8)
itf.add_error("area", "time", "strain")

itf.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
itf.remove_damage(0.2, 0.8)
itf.add_error("area", "time", "strain")

itf.read_data("creep/inl_1/AirBase_1000_12_G52.csv")
itf.remove_damage(0.2, 0.8)
itf.add_error("area", "time", "strain")

itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
itf.remove_damage(0.2, 0.8)
itf.add_error("area", "time", "strain")

itf.reduce_errors("square_average")
itf.reduce_objectives("square_average")

itf.plot_experimental()
itf.set_recorder(10, plot_opt=True, plot_loss=True)
itf.optimise(10000, 100, 50, 0.8, 0.01)
