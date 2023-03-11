from modules.api import API
api = API("", 0)
# api.add_curve({"type": "creep", "temp": 800, "stress": 80})
# api.define_model("evpwd")
# api.param_effects([28.1824, 33.46547, 28.03622, 2.002145, 56646.89, 39.80115, 277.1375, 1.970471], 0.5, 5)
api.add_curve({"type": "tensile", "temp": 25, "strain_rate": 0.0001})
api.define_model("evp")
api.param_effects([19.08450964, 99.0383612, 161.3614714, 12, 141.2451194], 0.5, 10)