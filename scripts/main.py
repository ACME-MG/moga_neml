import sys; sys.path += [".."]
from moga_neml.interface import Interface

itf = Interface("evp")
itf.define_model("evp")

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.remove_manual("time", 3000000)
itf.add_error("area", "time", "strain")

itf.set_recorder(1, plot_opt=True, plot_loss=True)
itf.optimise(1, 100, 50, 0.8, 0.01)
