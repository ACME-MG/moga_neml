import sys; sys.path += [".."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True)

itf.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
itf.remove_oxidation()
itf.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
itf.remove_oxidation(0.1, 0.7)
itf.read_data("creep/inl_1/AirBase_1000_12_G48.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_12_G48.csv")
itf.remove_oxidation()
itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
itf.remove_oxidation(0.1, 0.7)

itf.plot_experimental()
