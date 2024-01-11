import sys; sys.path += [".."]
from moga_neml.interface import Interface

itf = Interface(output_here=True)

# itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
# itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
# itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
# itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
# itf.read_data("tensile/inl/AirBase_800_D7.csv")

itf.read_data("creep/inl_1/AirBase_900_36_G22.csv")
itf.read_data("creep/inl_1/AirBase_900_31_G50.csv")
itf.read_data("creep/inl_1/AirBase_900_28_G45.csv")
itf.read_data("creep/inl_1/AirBase_900_26_G59.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_900_26_G59.csv")
itf.remove_oxidation()
itf.read_data("tensile/inl/AirBase_900_D10.csv")

# itf.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
# itf.add_error("dummy")
# itf.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
# itf.remove_oxidation()
# itf.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
# itf.add_error("dummy")
# itf.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
# itf.remove_oxidation(0.1, 0.7)
# itf.read_data("creep/inl_1/AirBase_1000_12_G52.csv")
# itf.add_error("dummy")
# itf.read_data("creep/inl_1/AirBase_1000_12_G52.csv")
# itf.remove_oxidation()
# itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
# itf.add_error("dummy")
# itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
# itf.remove_oxidation(0.1, 0.7)
# itf.read_data("tensile/inl/AirBase_1000_D12.csv")

itf.plot_experimental()
