import sys; sys.path += [".."]
from moga_neml.api import API

api = API()
api.define_model("evpcd")

params_str = """
17.217	179.74	0.61754	4.4166	1783.5
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
api.fix_params(params_list[0])

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.add_error("area", "time", "strain")

# api.plot_prediction(3109.8, 4.8245, 6.6364)
# api.get_results(3109.8, 4.8245, 6.6364)

api.set_recorder(interval=1, save_model=True)
api.optimise(population=10, offspring=5)
