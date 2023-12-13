import sys; sys.path += [".."]
from moga_neml.api import API

api = API()
api.define_model("evpcd")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.set_custom_driver("creep", smax=36, srate=0.0001, hold=11500.0 * 3600.0, T=900,
                      check_dmg=True, dtol=0.95, nsteps_up=50, nsteps=500, logspace=False)

params_str = """
9.5313	148.61	0.37484	3.9621	1253.9	2014.6	4.3748	8.0504
9.5315	149.26	0.37326	3.9582	1254.6	2014.8	4.3854	8.0511
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
api.get_results(*params_list[0])

api.set_recorder(1, True)
api.optimise(100, 50, 25, 0.8, 0.01)