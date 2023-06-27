import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpcvr")
api.define_model("evpcvr")
# api.fix_param("cvr_R_min", 0)

# api.read_file("creep/inl_1/AirBase_800_80_G25.csv", True)
# api.read_file("creep/inl_1/AirBase_800_70_G44.csv", True)
# api.read_file("creep/inl_1/AirBase_800_65_G33.csv", True)
# api.read_file("creep/inl_1/AirBase_800_60_G32.csv", True)
# api.__remove_tertiary_creep__()
# api.add_error("y_area", "creep")
api.read_file("tensile/AirBase_800_D7.csv", True)
api.add_error("y_area", "tensile")

# api = API("evpc 20c", 0)
# api.define_model("evpc")
# api.fix_param("evp_n", 15)
# api.read_file("tensile/AirBase_20_D5.csv", True)
# api.add_error("y_area", "tensile")

api.record(50, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)
# api.plot_results(0.000615469, 1.000297996, 1.793510282, 0.000430129, 339.4786545, 1217.920681, 1.468425915, 3.93296E-11)