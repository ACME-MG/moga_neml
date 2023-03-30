from modules.api import API
api = API("", 0)
api.add_curve({"type": "creep", "temp": 800, "stress": 80})
api.add_curve({"type": "creep", "temp": 800, "stress": 70})
api.add_curve({"type": "creep", "temp": 800, "stress": 65})
api.add_curve({"type": "creep", "temp": 800, "stress": 60})
api.define_model("evpwd")
api.param_effects([10.53847021,41.74347637,15.25155475,2.329254942,40314.56828,0.149840356,2.600235546,1.317962491], 5, 5)