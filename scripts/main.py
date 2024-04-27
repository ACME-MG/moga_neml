import sys; sys.path += [".."]
from moga_neml.interface import Interface

itf = Interface("", output_here=True)
# itf.define_model("evp")

# itf.read_data("tensile/inl/AirBase_800_D7.csv")
# itf.read_data("tensile/inl/AirBase_900_D10.csv")
itf.read_data("tensile/inl/AirBase_1000_D12.csv")

itf.plot_experimental()
