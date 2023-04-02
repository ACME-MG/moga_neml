from modules.api import API
api = API("", 0)
api.add_curve({"type": "creep", "temp": 800, "stress": 80})
api.add_curve({"type": "creep", "temp": 800, "stress": 70})
api.add_curve({"type": "creep", "temp": 800, "stress": 65})
api.add_curve({"type": "creep", "temp": 800, "stress": 60})
api.define_model("evpwd")
api.param_effects([10.47889692,43.119527,63.15407936,1.798253187,188594.675,0.313285971,3.215294321,2.680277526], 5, 5)
