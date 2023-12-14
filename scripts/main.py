import sys; sys.path += [".."]
from moga_neml.api import API

api = API()
api.define_model("evpcd")

params_str = """
17.217	179.74	0.61754	4.4166	1783.5
5.6908	66.627	1.9851	4.7723	1621.6
9.3076	32.596	5.8114	4.5263	1775.9
5.8951	36.245	5.3757	4.7311	1598.4
4.1862	84.548	2.1123	4.7752	1574.3
25.038	90.693	0.61002	4.1982	1944.6
27.547	78.081	0.84273	3.8992	2454.8
27.885	124.89	0.65636	3.8874	2390.5
19.2	52.204	1.7579	4.5105	1614.6
8.5923	38.904	5.4829	4.4795	1841
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
api.fix_params(params_list[0])

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.add_error("area", "time", "strain")

api.plot_prediction(3109.8, 4.8245, 6.6364)
api.get_results(3109.8, 4.8245, 6.6364)

# api.set_recorder(interval=1, save_model=True)
# api.optimise(population=10, offspring=5)