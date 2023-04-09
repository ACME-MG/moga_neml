from modules.api import API
api = API("", 0)
api.add_curve({"type": "creep", "temp": 800, "stress": 80})
api.add_curve({"type": "creep", "temp": 800, "stress": 70})
api.add_curve({"type": "creep", "temp": 800, "stress": 65})
api.add_curve({"type": "creep", "temp": 800, "stress": 60})
api.define_model("evpwd")
# api.isolate_params("wd_n")
api.param_effects([38.99624704,11.71881962,19.2721515,1.902299975,139783.5767,0.233261627,2.779682457,4.593576242], 1, 10)
