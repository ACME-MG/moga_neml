import sys; sys.path += [".."]
from moga_neml.interface import Interface

itf = Interface("evpwdb 900")
itf.define_model("evpwdb")

itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.read_data("tensile/inl/AirBase_900_D10.csv")
itf.read_data("tensile/inl/AirBase_1000_D12.csv")

itf.plot_experimental()

# itf.reduce_errors("square_average")
# itf.reduce_objectives("square_average")
# # itf.group_errors(name=True, type=False, labels=True)

# itf.set_recorder(1, plot_opt=True, plot_loss=True)
# itf.optimise(10000, 100, 50, 0.8, 0.01)
